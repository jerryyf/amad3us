from langchain_core.documents.base import Document
from typing import Iterator, Sequence
from langchain_core.messages.base import BaseMessage
from langchain_community.chat_loaders.telegram import TelegramChatLoader
from langchain_community.chat_loaders.utils import map_ai_messages, merge_chat_runs
from langchain_core.chat_sessions import ChatSession
from langchain_community.document_loaders.telegram import TelegramChatFileLoader, TelegramChatApiLoader

class ChatLoader:
    def __init__(self, sender: str = None, path: str = None) -> None:
        self.sender = sender
        self.path = path

    def tg_from_json_to_messages(self) -> Sequence[BaseMessage] | None:
        loader: TelegramChatLoader = TelegramChatLoader(path=self.path)
        merged_messages: Iterator[ChatSession] = merge_chat_runs(chat_sessions=loader.lazy_load())
        messages: list[ChatSession] = list(map_ai_messages(chat_sessions=merged_messages, sender=self.sender))
        return messages[0].get("messages")

    def tg_from_json_to_documents(self) -> list[Document]:
        loader: TelegramChatFileLoader = TelegramChatFileLoader(path=self.path)
        documents: List[Document] = loader.load()
        return documents

    def load_messenger_chat_from_json(self):
        # stub
        return
