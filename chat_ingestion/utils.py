import json
import datetime

DEBUG = True

def create_message_obj(from_id, timestamp, text_value) -> dict:
    try:
        return {
            "user": from_id,
            "time": timestamp,
            "message": text_value
        }
    except Exception as e:
        print("error formatting message_obj")
        if DEBUG:
            print(e)


def extract_by_id(from_id:str, filepath:str):
    extracted_texts = []
    with open(filepath, 'r') as file:

        text_data = json.load(file)
        messages = (text_data.get("messages", None))

        for msg in messages:
            # check if obj is a message
            if msg.get("type", None) != "message":
                continue
            # else we want to extract the text and timestamp
            text_value = msg.get("text", None)
            timestamp = text_data.get("date_unixtime", None)
            if text_value != None:
                message_obj = create_message_obj(from_id, timestamp, text_value)
                extracted_texts.append(message_obj)

    return extracted_texts


def extract_all_messages(filepath:str) -> list:
    extracted_texts = []
    with open(filepath, 'r') as file:

        jsonfile = json.load(file)
        messages = (jsonfile.get("messages", None))

        for msg in messages:
            # check if it is of type message
            if msg.get("type", None) != "message":
                continue
            # else we want to extract the text field
            text_value = msg.get("text", None)
            timestamp = msg.get("date_unixtime", None)
            from_id = msg.get("from_id", None)
            if text_value != None:
                message_obj = create_message_obj(from_id, timestamp, text_value)
                extracted_texts.append(message_obj)

    return extracted_texts

def format_output(filepath:str) -> str:
    ret = ""
    all_msg = extract_all_messages(filepath)
    for i in range(len(all_msg)):
        ret += f"{all_msg[i].get('user')} at {all_msg[i].get('time')}: {all_msg[i].get('message')}\n"
    return ret
