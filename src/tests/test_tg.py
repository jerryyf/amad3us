from ingestion.tg import format_jsonl, extract_all_messages, combine_messages, handle_user_order
from os import getenv
from dotenv import load_dotenv

# init tests
load_dotenv("../.env")
tg_username = getenv("TG_USERNAME")

# test extracted messages output

# test handle user order output

# test combine messages output
message_list = handle_user_order(extract_all_messages("ingestion/sample.json"))

cat_msg = combine_messages(message_list, tg_username)
print(cat_msg)