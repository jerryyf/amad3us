from langchain_community.document_loaders import TelegramChatLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4

class VectorStore:

    class State(TypedDict):
        question: str
        context: List[Document]
        answer: str

    def __init__(self, index_path: str, model: str) -> None:
        self.index_path = index_path
        self.model = model
        self.embeddings = OllamaEmbeddings(model=self.model)
        index = faiss.IndexFlatL2(len(self.embeddings.embed_query("hello world")))
        self.vector_store = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
    
    def get_vectorstore(self) -> FAISS:
        return self.vector_store

    def load_tg(
        self,
        data_path: str,
        chunk_size: int = 2000,
        chunk_overlap: int = 100,
        *trim_size: int,
    ) -> list[Document]:
        loader = TelegramChatLoader(data_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        all_splits = text_splitter.split_documents(documents)
        print(f"Split into {len(all_splits)} sub-documents.")

        if trim_size:
            trimmed = all_splits[:trim_size]
            print(f"Trimmed into {len(trimmed)} sub-documents.")
            return trimmed
        else:
            return all_splits

    def add(self, documents: list[Document]) -> None:
        _ = self.vector_store.add_documents(documents=documents)
        print(f"Added {len(documents)} to vectorstore.")

    def save(self):
        _ = self.vector_store.save_local(self.index_path)

    def load(self):
        self.vector_store = FAISS.load_local(
            self.index_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

    def retrieve(self, query: str, k: int = 4) -> dict:
        retriever = self.vector_store.as_retriever(search_type="mmr", search_kwargs={"k": k})
        retrieved_docs = retriever.invoke(query)
        return {"context": retrieved_docs}
    
    def search(self, query: str, k: int) -> list[Document]:
        results = self.vector_store.similarity_search(
            query=query,
            k=k,
        )
        return results

