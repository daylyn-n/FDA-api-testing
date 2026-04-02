# FDA API Testing

A lightweight test suite for the [openFDA Drug Adverse Events API](https://open.fda.gov/apis/drug/event/).

## Purpose

Validates that the openFDA `/drug/event` endpoint remains stable over time — checking HTTP status, response structure, field presence, and field types against a known-good snapshot.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install pytest requests
```

## Run tests

```bash
pytest tests/
```

Requires an internet connection (tests hit the live API).
