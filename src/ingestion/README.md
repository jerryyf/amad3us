# ingestion

Chat log ingestion service.

## Prerequisites

- python 3.13
- virtualenv

## Development setup

Add your exported sample.json file under the ingestion directory.

Next create virtualenv in the root directory of this project:

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

Create .env file:

```sh
echo TG_USERNAME="your-username" > .env
```

## Running tests

Run in src directory:

```sh
python3 -m tests.test_tg
```

## Supported ingestion formats

- Telegram DM chats exported as json

## Output format

```
[{'prompt': 'hi\nhows ur day', 'context': '', 'response': 'good thanks!\nhows urs'}]
```

```
{'prompt': 'hi\nhows ur day', 'context': '', 'response': 'good thanks!\nhows urs'}
{'prompt': 'mines good\nwyd today', 'context': '', 'response': 'im cleaning my room'}
```

## Environment variables reference

- `CHAT_INGESTION_DEFAULT_USERNAME`: set a preferred username for cases where the other user has deleted their account which when exported contains a null `from` field