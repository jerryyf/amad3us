import json
from datetime import datetime
from os import getenv
from dotenv import load_dotenv
from queue import Queue

load_dotenv("../.env")
DEBUG = True

def format_prompt_obj(prompt:str, response:str, context:str) -> dict:
    try:
        return {
            "prompt": prompt,
            "response": response,
            "context": context
        }
    except Exception as e:
        print("error formatting prompt_obj")
        if DEBUG:
            print(e)
        exit(1)

def format_message_obj(from_id:str, timestamp:str, text_value:str) -> dict:
    try:
        dt = datetime.fromtimestamp(float(timestamp))
        return {
            "user": from_id,
            "time": dt.strftime("%d-%m-%Y, %H:%M"),
            "text": text_value
        }
    except Exception as e:
        print("error formatting message_obj")
        if DEBUG:
            print(e)
        exit(1)


def extract_all_messages(filepath:str) -> list:
    """returns list of dict containing message_obj.

    message_obj keys: user, time, text

    """
    ret = []

    with open(filepath, "r") as file:

        jsonfile = json.load(file)
        messages = (jsonfile.get("messages", None))

        for msg in messages:
            # check if it is of type message
            if msg.get("type", None) != "message":
                continue
            text_value = msg.get("text", None)
            # check if text_value is null
            # if it is then put empty string
            if text_value == None:
                text_value = ""
            timestamp = msg.get("date_unixtime", None)
            # from_id = msg.get("from_id", None)
            username = msg.get("from", None)
            # check if `from` field is not null - this can be the case when user has deleted their account
            # if it is then use default username
            if username == None:
                username = getenv("TG_OTHER_USERNAME")
                message_obj = format_message_obj(username, timestamp, text_value)
            else:
                message_obj = format_message_obj(username, timestamp, text_value)
            ret.append(message_obj)

    return ret

def flush_msg_buf(buf:Queue) -> str:
    ret = ""
    while not buf.empty():
        ret += f"{buf.get()}\n"
    return ret

def handle_user_order(all_msg:list) -> list:
    ret = []
    user_changed = False
    for i in range(1, len(all_msg)):
        curr_user = all_msg[i].get("user", None)
        prev_user = all_msg[i-1].get("user", None)
        curr_msg = all_msg[i].get("text", None)

        if curr_user != prev_user and not user_changed:
            ret.append(all_msg[i])
            user_changed = True

        elif user_changed:
            ret.append(all_msg[i])
    
    return ret


def combine_messages(all_msg:list, llm_user:str) -> list:
    # cat consecutive messages from the same user into one message. return a list of dict

    ret = []
    prompt_buf = Queue()
    response_buf = Queue()

    user_changed = 0
    user_changed_internal = 0
    prompt = ""
    response = ""
    context = ""

    # for i in range(len(all_msg)):
    for i in range(1, len(all_msg)):

        # if only 1 message
        if len(all_msg) == 1:
            ret.append(all_msg[0])
            break

        curr_user = all_msg[i].get("user", None)
        prev_user = all_msg[i-1].get("user", None)
        curr_msg = all_msg[i].get("text", None)

        # assume starts with non-llm user and len > 2
        if curr_user != llm_user and user_changed_internal < 1:
            continue
        else:
            user_changed_internal = 1
        
        if curr_user != prev_user:
            user_changed += 1

        # check if llm user or not and put in respective buffers
        if curr_user == llm_user:
            prompt_buf.put(curr_msg)
        else:
            response_buf.put(curr_msg)


        # if user has changed an even number of times, append previous and start a new object
        # if user changed at least once and is even, append pboject and start new object
        if user_changed % 2 == 0 and user_changed > 0 and curr_user != prev_user:
            print(user_changed)
            prompt = flush_msg_buf(prompt_buf)
            response = flush_msg_buf(response_buf)
            print(response)
            ret.append(format_prompt_obj(prompt, response, context))
            prompt = ""
            response = ""
            context = ""
        
    return ret


def format_jsonl(preprocessed: list) -> str:
    """
    Converts a list of preprocessed conversation objects into a JSONL formatted string.

    Args:
        preprocessed (list): List of dicts with keys 'prompt', 'response', and 'context'.

    Returns:
        str: JSONL formatted string.
    """
    ret = ""

    for conversation in preprocessed:
        try:
            # Convert each conversation dict to a JSON string and append it with a newline
            ret += json.dumps(conversation) + "\n"
        except Exception as e:
            print("Error serializing conversation to JSONL")
            if DEBUG:
                print(e)
            exit(1)

    return ret