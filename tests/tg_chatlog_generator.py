import json
from datetime import datetime, timedelta

filename = "filename"

chat = {
    "name": "User1",
    "type": "personal_chat",
    "id": 2032847485,
    "messages": []
}

base_time = datetime(2024, 1, 1, 10, 0)
for i in range(1, 101):
    sender = "User1" if i % 2 else "User2"
    chat["messages"].append({
        "id": i,
        "type": "message",
        "date": (base_time + timedelta(minutes=i*2)).strftime("%Y-%m-%dT%H:%M:%S"),
        "date_unixtime": str(int((base_time + timedelta(minutes=i*2)).timestamp())),
        "from": sender,
        "from_id": sender.lower(),
        "text": f"Message {i} from {sender}",
        "text_entities": [{"type": "plain", "text": f"Message {i} from {sender}"}]
    })

with open(f"{filename}.json", "w") as f:
    json.dump(chat, f, indent=2)

