from langchain_core.documents.base import Document
from typing import Iterator, Sequence
from langchain_core.messages.base import BaseMessage
from langchain_community.chat_loaders.telegram import TelegramChatLoader
from langchain_community.chat_loaders.utils import map_ai_messages, merge_chat_runs
from langchain_core.chat_sessions import ChatSession
from langchain_community.document_loaders.telegram import TelegramChatFileLoader, TelegramChatApiLoader
from langchain_community.document_loaders import JSONLoader

class ChatLoader:
    def __init__(self, sender: str = None, path: str = None, integration: str = "tg") -> None:
        self.sender = sender
        self.path = path
        self.integration = integration

    def tg_from_json_to_messages(self) -> Sequence[BaseMessage] | None:
        loader = TelegramChatLoader(path=self.path)
        merged_messages = merge_chat_runs(chat_sessions=loader.lazy_load())
        messages = list(map_ai_messages(chat_sessions=merged_messages, sender=self.sender))
        return messages[0].get("messages")

    def tg_from_json_to_documents(self) -> list[Document]:
        loader = TelegramChatFileLoader(path=self.path)
        documents = loader.load()
        return documents

    def load_messenger_chat_from_json(self):
        # stub
        return

    def json_generic_to_documents(self, jq_schema: str = ".messages[].content"):
        loader = JSONLoader(
            file_path=self.path,
            jq_schema=jq_schema,
            text_content=False,
        )
        documents = loader.load()
        return documents