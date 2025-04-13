from src.ingestion.tg import format_jsonl, extract_all_messages, combine_messages
from os import getenv

message_list = extract_all_messages("src/ingestion/sample.json")

# print(format_jsonl("ingestion/sample.json", "username"))

cat_msg = combine_messages(message_list, "Danny")
print(cat_msg)