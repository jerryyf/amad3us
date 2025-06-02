# fr3nd-ai

LLM chatbot using ollama that mimics human chat behaviour, given existing chat log dumps.

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

Create `.env` file in `llm` directory:

```sh
echo TG_USERNAME="your-username" > llm/.env
```

## Testing

In project root directory:

```sh
python3 -m unittest tests.test_tg
```

## Integrations

- Telegram

## Roadmap

- [x] Basic local CLI chat interface with memory of extracted message data
- [ ] RAG to improve performance and larger context window
- [ ] Direct access to Telegram API
- [ ] Modularity
- [ ] Chatbot API
- [ ] Timezone awareness
- [ ] Finetuning
- [ ] Other data types