from src.ingestion.tg import format_jsonl, extract_all_messages, combine_messages
from os import getenv
from dotenv import load_dotenv

# init tests
load_dotenv("../.env")
tg_username = getenv("TG_USERNAME")

# test extracted messages output
class TestExtractedMessages(unittest.TestCase):
    def test_message_extraction_contains_single(self):
        message_list = extract_all_messages("src/tests/test_logs_tg/basic_receive_message.json")
        # check if the list is not empty
        self.assertTrue(len(message_list) > 0)
        # check if the first message is of type dict
        self.assertIsInstance(message_list[0], dict)
    def test_basic_interaction(self):
        message_list = extract_all_messages("src/tests/test_logs_tg/basic_response.json")
        self.assertTrue(len(message_list) == 2)

        self.assertTrue(message_list[0]['user'] == "User1")
        self.assertTrue(message_list[0]['text'] == "Hello user 2")
        self.assertTrue(message_list[0]['time'] == "08-07-2023, 00:16")

        self.assertTrue(message_list[1]['user'] == "User2")
        self.assertTrue(message_list[1]['text'] == "Hi user 1")
        self.assertTrue(message_list[1]['time'] == "08-07-2023, 00:16")

    def test_output_one_hundred_messages(self):
        message_list = extract_all_messages("src/tests/test_logs_tg/one_hundred_messages.json")
        self.assertTrue(len(message_list) == 100)

        self.assertTrue(message_list[0]['user'] == "User1")

        self.assertTrue(message_list[99]['user'] == "User2")

    def test_sample_conversation(self):
        message_list = extract_all_messages("src/tests/test_logs_tg/sample_conversation.json")
        print(message_list)
        # Should skip photo message
        self.assertTrue(message_list[0] == "220c per L but paid 179c per L")

        self.assertTrue(message_list[0]['user'] == "UserA")
        self.assertTrue(message_list[1]['user'] == "UserA")
        self.assertTrue(message_list[2]['user'] == "UserB")
# test handle user order output

# test combine messages output
message_list = handle_user_order(extract_all_messages("ingestion/sample.json"))

cat_msg = combine_messages(message_list, tg_username)
print(cat_msg)