# A4-JDAM

Flask app that interprets dreams with the OpenAI Responses API and generates a symbolic image with the OpenAI Images API.

## Entry Point

- Main application file: `app.py`
- Flask app object: `app`
- Local run entry point: `if __name__ == "__main__": app.run(debug=True)`

## Requirements

- Python 3.10+
- OpenAI API key

## Setup

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install flask openai python-dotenv pillow pytest
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask openai python-dotenv pillow pytest
```

## Environment Variables

Create a `.env` file in the repo root:

```env
OPENAI_API_KEY=your_api_key_here
```

## Run the App

From the repo root:

```bash
python app.py
```

Then open `http://127.0.0.1:5000/` in your browser.

## Tests

There is no `tests/` directory or test suite in this repository yet.

To run tests once they exist:

```bash
python -m pytest
```

With the current codebase, `pytest` should report that no tests were collected.

## Suggested Next Step

Add a basic Flask route test (for `/`) and a mocked OpenAI client test so `pytest` becomes meaningful for CI.
