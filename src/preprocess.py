import json
import os
from loaders import ChatLoader

config_path = "./data/config.json"
sources: dict

class PreProcessor:

    def __init__(self) -> None:
        super().__init__()

    def construct(data_path):

        try:
            for filename in os.listdir(data_path):
                # Construct the full file path
                filepath = os.path.join(data_path, filename)

                # Check if it's a file or directory
                if os.path.isfile(filepath):
                    print(f"File: {filepath}")
                    ret += filepath
                elif os.path.isdir(filepath):
                    print(f"Directory: {filepath}")
                    # You could recursively loop through subdirectories here, if needed
                else:
                    print(f"Unknown: {filepath}")
        except FileNotFoundError:
            print(f"Directory not found: {directory_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # with open(config_path, "r") as f:
    #     sources = json.load(f)

    # _ = ChatLoader(path="./data")

    # for source in sources:
    #     if not os.path.exists(f"./faiss_index-{str(source)}"):
    #         print(f"faiss_index-{str(source)} not found. Creating vector store...")
    #         store = VectorStore(f"./faiss_index-{str(source)}", "nomic-text-embeddings")
    #         docs = store.load_tg(f"{data_path}/tg/{str(source)}/result.json")
    #         # print(docs)
    #         store.add(docs)
    #         store.save()
    #     else:
    #         print(f"faiss_index{str(source)} found. Loading store...")
