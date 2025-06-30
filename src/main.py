import os
from os import getenv
from dotenv import load_dotenv
from loaders import ChatLoader
from llms import OllamaGraph
import asyncio
from langchain_core.messages import HumanMessage, AIMessage
from vectorstore import VectorStore
from langchain import hub
from prompts import rag_prompt

load_dotenv()
OLLAMA_MODEL = getenv(key="OLLAMA_MODEL", default="")
OLLAMA_URL = getenv(key="OLLAMA_URL", default="")
TG_SENDER = getenv(key="TG_SENDER", default="")
data_path = "./data"

run_mode = "rag"

if __name__ == "__main__":
    if run_mode == "rag":
        app = OllamaGraph(
            ollama_model=OLLAMA_MODEL,
            ollama_url=OLLAMA_URL,
        )

        store = VectorStore("./faiss_index", "nomic-embed-text")
        if not os.path.exists("./faiss_index"):
            print("Directory 'faiss_index' not found. Creating vector store...")
            docs = store.load_tg(f"{data_path}/tg/result.json")
            # print(docs)
            store.add(docs)
            store.save()
        else:
            print("Directory 'faiss_index' found. Loading store...")

        store.load()
        print("Store loaded")

        config = {"configurable": {"thread_id": "1"}}

        async def chat_loop():
            while True:
                query = input("you: ")
                context = store.retrieve(query)
                input_messages = rag_prompt(query, context)

                assert len(input_messages) == 1
                print(input_messages[0].content)

                for chunk, metadata in app.graph.stream(
                    {"messages": input_messages},
                    config,
                    stream_mode="messages",
                ):
                    if isinstance(chunk, AIMessage):
                        print(chunk.content, end="", flush=True)
                print("\n")

        asyncio.run(chat_loop())

    elif run_mode == "memory":
        app = OllamaGraph(
            ollama_model=OLLAMA_MODEL,
            ollama_url=OLLAMA_URL,
        )

        tg_loader = ChatLoader(path=f"{data_path}/tg_chat.json", sender=TG_SENDER)
        input_messages = tg_loader.tg_from_json_to_messages()

        config = {"configurable": {"thread_id": "1"}}
        output = app.graph.invoke({"messages": input_messages}, config)

        async def chat_loop():
            while True:
                query = input("you: ")
                input_messages = [HumanMessage(query)]
                for chunk, metadata in app.graph.stream(
                    {"messages": input_messages},
                    config,
                    stream_mode="messages",
                ):
                    if isinstance(chunk, AIMessage):
                        print(chunk.content, end="", flush=True)
                print("\n")

        asyncio.run(chat_loop())
    else:
        print("run_mode not set")