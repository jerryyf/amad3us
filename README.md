# fr3nd-ai

LLM terminal-based chatbot framework leveraging LangChain and Ollama backend for ingesting chat logs and various other text data - privately.

## Ollama setup

```sh
curl -fsSL https://ollama.com/install.sh | sh
```

## Use cases

- Behavioural psychoanalysis leveraging retrieval augmented generation
- Pattern recognition from personal data
- Behavioural simulation
- Message prediction
- AI assisted self reflection

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

Contents of the env file:

```
OLLAMA_MODEL="llama3.2:3b"
OLLAMA_URL="localhost:11434"
TG_SENDER="Deleted Account"
```

Run the CLI app - default run_mode is set to `rag` - can be changed to `memory` (version 1.0.1).

```sh
cd src
python3 main.py
```

## App configuration

FAISS vector store creation time can vary greatly depending on your CPU. You may wish to adjust parameters `trim_size`, `chunk_size` and `chunk_overlap` from their default values depending on your hardware.

## Testing

TODO

## Data integrations

- Telegram chats

## Roadmap

- [x] Basic local CLI chat interface with memory of extracted message data
- [x] RAG to improve performance and larger context window
- [x] Modularity
- [ ] Chatbot API
- [ ] Agents for web assistance
- [ ] Finetuning
- [ ] Support for majority of text data types