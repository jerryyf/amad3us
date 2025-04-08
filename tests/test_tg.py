from ingestion.tg import format_jsonl, extract_all_messages
from os import getenv

message_list = extract_all_messages("ingestion/sample.json")

print(format_jsonl("ingestion/sample.json", "username"))
