import json
from datetime import datetime
from os import getenv
from queue import Queue

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
                username = getenv("DEFAULT_USERNAME")
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
        prev_msg = all_msg[i-1].get("text", None)

        if curr_user != prev_user and not user_changed:
            ret.append(format_message_obj(all_msg[i].get("user"), "123456789", curr_msg))
            user_changed = True

        if user_changed:
            ret.append(format_message_obj(all_msg[i].get("user"), "123456789", curr_msg))
    
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

        # if len(all_msg) == 1:
        #     ret.append(all_msg[0])
        #     break

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


def format_jsonl(filepath:str, prompting_user:str) -> str:
    """returns a jsonl formatted string of all messages in the file. Replaces usernames with prompt and response.

    Args:
        filepath (str): path of the file to be formatted

    Returns:
        str: formatted jsonl string
    """
    ret = ""
    all_msg = extract_all_messages(filepath)

    for i in range(len(all_msg)):
        if all_msg[i].get("user") == prompting_user:
            ret += '{'
            ret += f'"prompt": "{all_msg[i].get("text")}"'
            ret += '}\n'
        else:
            ret += '{'
            ret += f'"response": "{all_msg[i].get("text")}"'
            ret += '}\n'
        # "timestamp": {all_msg[i].get('time')}:

    return ret
