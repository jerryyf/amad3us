import json
from datetime import datetime
from os import getenv

DEBUG = True

def format_prompt_obj(prompt:str, response:str, context:str) -> dict:
    """creates a dict from message parameters, also formats the timestamp to a human readable format

    Args:
        from_id (str): user id
        timestamp (str): unix timestamp
        text_value (str): message content

    Returns:
        dict: dict containing parameters
    """
    try:
        return {
            "prompt": prompt,
            "context": context,
            "response": response
        }
    except Exception as e:
        print("error formatting prompt_obj")
        if DEBUG:
            print(e)
        exit(1)

def format_message_obj(from_id:str, timestamp:str, text_value:str) -> dict:
    """creates a dict from message parameters, also formats the timestamp to a human readable format

    Args:
        from_id (str): user id
        timestamp (str): unix timestamp
        text_value (str): message content

    Returns:
        dict: dict containing parameters
    """
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
    """preprocess a DM export

    Args:
        filepath (str): path of file
        prompting_user (str): username of the user that should be considered as the one sending prompts

    Returns:
        list: list of message objects
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
                username = getenv("DEFAULT_USERNAME")
                message_obj = format_message_obj(username, timestamp, text_value)
            else:
                message_obj = format_message_obj(username, timestamp, text_value)
            ret.append(message_obj)

    return ret

def get_combined_messages_by_user(all_msg:list, user:str) -> list:
    None


def combine_messages(all_msg:list, llm_user:str) -> list:
    # cat consecutive messages from the same user into one message. return a list of dict
    ret = []

    data = {
        "prompt": "",
        "context": "",
        "response": ""
    }

    for i in range(len(all_msg)):
        # break on last msg
        if i == len(all_msg) - 1:
            break

        curr_user = all_msg[i].get("user", None)
        next_user = all_msg[i+1].get("user", None)
        curr_msg = all_msg[i].get("text", None)
        next_msg = all_msg[i+1].get("text", None)


        # if current msg is from the llm user it goes in prompt.
        if curr_user == llm_user:
            if data["prompt"] == "":
                data["prompt"] += str(curr_msg)

            # check if the next message is also from llm user. if so add it to the prompt
            if next_user == llm_user:
                data["prompt"] += "\\n" + str(next_msg)
            # if it not it must be from the other user.
            else:
                ret.append(data)
                data = {
                    "prompt": "",
                    "context": "",
                    "response": ""
                }
                continue



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
