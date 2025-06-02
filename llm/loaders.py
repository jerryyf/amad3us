from langchain_community.chat_loaders.telegram import TelegramChatLoader
from typing import List
from langchain_community.chat_loaders.utils import (
    map_ai_messages,
    merge_chat_runs,
)
from langchain_core.chat_sessions import ChatSession

def load_tg_chat_from_json(path:str, sender:str):
    loader = TelegramChatLoader(path)
    raw_messages = loader.lazy_load()
    merged_messages = merge_chat_runs(raw_messages)
    messages: List[ChatSession] = list(
        map_ai_messages(merged_messages, sender=sender)
    )
    return messages[0]["messages"]

