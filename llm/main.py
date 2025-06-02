from os import getenv
from dotenv import load_dotenv
import loaders
import asyncio
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()
ollama_model = getenv("OLLAMA_MODEL")
ollama_base_url = getenv("OLLAMA_BASE_URL")
tg_sender = getenv("TG_SENDER")

if __name__ == "__main__":
    model = ChatOllama(model=ollama_model, base_url=ollama_base_url)

    workflow = StateGraph(state_schema=MessagesState)

    def call_model(state: MessagesState):
        response = model.invoke(state["messages"])
        return {"messages": response}

    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": "abc123"}}

    input_messages = loaders.load_tg_chat_from_json("./data/tg_chat.json", tg_sender)
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()

    async def chat_loop():
        while True:
            query = input("Your message: ")
            input_messages = [HumanMessage(query)]
            for chunk, metadata in app.stream(
                {"messages": input_messages}, config,
                stream_mode="messages",
            ):
                if isinstance(chunk, AIMessage):
                    print(chunk.content, end="")

            output = await app.ainvoke({"messages": input_messages}, config)
            print("\n")
            output["messages"][-1].pretty_print()
            print("\n")

    asyncio.run(chat_loop())