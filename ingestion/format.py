import json

def get_broken_messages(filepath:str) -> bool:
    ret = []
    with open(filepath, "r") as file:
        jsonfile = json.load(file)
        messages = (jsonfile.get("messages", None))
        for message in messages:
            if isinstance(message.get("text", None), list):
                for obj in message.content:
                    text = ""
                    if isinstance(obj, dict):
                        text += obj.get("text")
                    else:
                        text += obj
                message.content = text
    return ret
