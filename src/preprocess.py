import json
import os
from loaders import ChatLoader

config_path = "./data/config.json"
sources: dict

with open(config_path, "r") as f:
    sources = json.load(f)

_ = ChatLoader(path="./data")

for source in sources:
    if not os.path.exists(f"./faiss_index-{str(source)}"):
        print(f"faiss_index-{str(source)} not found. Creating vector store...")
        store = VectorStore(f"./faiss_index-{str(source)}", "nomic-text-embeddings")
        docs = store.load_tg(f"{data_path}/tg/{str(source)}/result.json")
        # print(docs)
        store.add(docs)
        store.save()
    else:
        print(f"faiss_index{str(source)} found. Loading store...")
