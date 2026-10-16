# Support FAQ Bot

A framework-agnostic FAQ engine with fuzzy matching (stdlib `difflib` + word overlap), a tiny CLI, and a Flask `POST /ask` endpoint. Fully unit-tested with pytest.

## Features
- Plug-in engine (`faq_engine.FAQEngine`) usable from any bot framework
- Typo-tolerant matching with configurable threshold, ranked suggestions
- CLI (interactive or one-shot) and JSON web API

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python cli.py "how long does delivry take"
python app.py           # http://localhost:5000
pytest -q
```

## Environment variables
| Variable | Default | Description |
|---|---|---|
| `FAQ_PATH` | `faq.json` | FAQ file |
| `FAQ_THRESHOLD` | `0.5` | Min score (0–1) |
| `PORT` | `5000` | Flask port |

## Example
```
$ python cli.py
> how do i reset my pasword
Click 'Forgot password' on the login page.  (matched: 'How do I reset my password?', score 0.83)

$ curl -s -X POST localhost:5000/ask -H 'Content-Type: application/json' -d '{"question":"refund?"}'
{"answer":"Contact support within 14 days of purchase for a full refund.","matched":true,...}
```
MIT licensed.
