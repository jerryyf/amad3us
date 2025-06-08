from os import getenv
from dotenv import load_dotenv
from loaders import ChatLoader
from llms import OllamaGraph
import asyncio
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()
OLLAMA_MODEL = getenv(key="OLLAMA_MODEL", default="")
OLLAMA_URL = getenv(key="OLLAMA_URL", default="")
TG_SENDER = getenv(key="TG_SENDER", default="")
data_path = "./data"

if __name__ == "__main__":
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