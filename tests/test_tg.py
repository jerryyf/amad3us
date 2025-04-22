from ingestion.tg import format_jsonl, extract_all_messages, combine_messages, handle_user_order
import os
from dotenv import load_dotenv
import unittest

# init env
load_dotenv("../env")
tg_username = os.getenv("TG_USERNAME")

# init paths
testdir = os.path.dirname(__file__)
sampledir = os.path.join(testdir, 'test_logs_tg')

# test extracted messages output
class TestExtractedMessages(unittest.TestCase):
    def test_message_extraction_contains_single(self):
        message_list = extract_all_messages(f"{sampledir}/basic_receive_message.json")
        # check if the list is not empty
        self.assertTrue(len(message_list) > 0)
        # check if the first message is of type dict
        self.assertIsInstance(message_list[0], dict)
    def test_basic_interaction(self):
        message_list = extract_all_messages(f"{sampledir}/basic_response.json")
        self.assertTrue(len(message_list) == 2)

        self.assertTrue(message_list[0]['user'] == "User1")
        self.assertTrue(message_list[0]['text'] == "Hello user 2")
        self.assertTrue(message_list[0]['time'] == "08-07-2023, 00:16")

        self.assertTrue(message_list[1]['user'] == "User2")
        self.assertTrue(message_list[1]['text'] == "Hi user 1")
        self.assertTrue(message_list[1]['time'] == "08-07-2023, 00:16")

    def test_output_one_hundred_messages(self):
        message_list = extract_all_messages(f"{sampledir}/one_hundred_messages.json")
        self.assertTrue(len(message_list) == 100)

        self.assertTrue(message_list[0]['user'] == "User1")

        self.assertTrue(message_list[99]['user'] == "User2")

    def test_sample_conversation(self):
        message_list = extract_all_messages(f"{sampledir}/sample_conversation.json")
        print(message_list)
        # Should skip photo message
        self.assertTrue(message_list[0] == "220c per L but paid 179c per L")

        self.assertTrue(message_list[0]['user'] == "UserA")
        self.assertTrue(message_list[1]['user'] == "UserA")
        self.assertTrue(message_list[2]['user'] == "UserB")

# test handle user order output

# test combine messages output


if __name__ == "__main__":
    unittest.main()
