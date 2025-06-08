from langchain_ollama.chat_models import ChatOllama
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.checkpoint.memory import MemorySaver, InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.vectorstores import FAISS
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore

class OllamaGraph:
    def __init__(self, ollama_model: str, ollama_url: str, persistent_memory: bool = True) -> None:
        self.ollama_model = ollama_model
        self.ollama_url = ollama_url
        self.persistent_memory = persistent_memory
        self.model = ChatOllama(model=self.ollama_model, base_url=self.ollama_url)
        self.checkpointer = MemorySaver() if self.persistent_memory else None
        self.graph = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        def call_model(state: MessagesState):
            response = self.model.invoke(
                state["messages"]
            )
            return {"messages": response}

        workflow = StateGraph(MessagesState)
        workflow.add_node(call_model)
        workflow.add_edge(START, "call_model")

        return workflow.compile(checkpointer=self.checkpointer)
