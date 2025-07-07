# opus

Open LLM framework built on top of LangChain and Ollama backend for processing sensitive personal data such as chat logs.

## Ollama setup

```sh
curl -fsSL https://ollama.com/install.sh | sh
```

## Use cases

- Behavioural psychoanalysis leveraging retrieval augmented generation
- Pattern recognition from personal data
- Behavioural simulation
- Message prediction
- Perspective from a virtual third party
- Self introspection

## Development setup

Create virtualenv in the root directory of this project:

```sh
python3 -m venv ./.venv
```

Activate virtualenv:

```sh
source .venv/bin/activate
```

Install requirements:

```sh
pip install -r requirements.txt
```

Create .env file in src/:

```sh
cd src
touch .env
```

## Configuration

Configuration is specified through environment variables. Example:

```
OLLAMA_MODEL="deepseek-r1"
OLLAMA_URL="localhost:11434"
TG_SENDER="Deleted Account"
APP_RUN_MODE="rag"
```

## Adding data

The app looks for data files under `src/data`. To add exported Telegram chat logs for example, create the directory `src/data/tg/` and add JSON files there.

## Usage

Run the CLI app - default run_mode is set to `rag` - can be changed to `memory` for message prediction/behaviour simulation.

```sh
python3 main.py
```

## Tuning

FAISS vector store creation time can vary greatly depending on your CPU. You may wish to adjust parameters `trim_size`, `chunk_size` and `chunk_overlap` from their default values depending on your hardware.

## Testing

TODO

## Data integrations

- Telegram chats
- JSON

## Roadmap

- [x] Basic local CLI chat interface with memory of extracted message data
- [x] RAG to improve performance and larger context window
- [x] Modularity
- [ ] Chatbot API
- [ ] Agents for web assistance
- [ ] Finetuning
- [ ] Support for majority of text data types
- [ ] True persistent memory
