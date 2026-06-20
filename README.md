# OpenClaw Study Assistant

A beginner-friendly Flask app that lets users paste text, choose a study mode, and see a real response from the local OpenClaw gateway.

## Features

- Paste lecture notes, code, or questions
- Choose one of three modes:
  - Summarise
  - Generate Quiz
  - Explain Code
- Uses `call_openclaw(prompt)` to send requests to the local OpenClaw chat completions endpoint

## Run It

1. Make sure the local OpenClaw gateway is running and chat completions are enabled.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python app.py
```

4. Open your browser at:

```text
http://127.0.0.1:5000
```

## Using `.env`

You can store your settings in a `.env` file in the project root. The app loads it automatically at startup.

1. Create a file named `.env`
2. Put your settings in it, for example:

```env
OPENCLAW_GATEWAY_URL=http://127.0.0.1:18789/v1
OPENCLAW_GATEWAY_TOKEN=your_real_token_here
OPENCLAW_MODEL=openclaw/default
```

3. Restart the Flask app after changing `.env`

## Environment Variables

These are optional, but useful if you want to point the app at a different gateway or model:

- `OPENCLAW_GATEWAY_URL`: Base URL for the local gateway, for example `http://127.0.0.1:18789/v1`
- `OPENCLAW_GATEWAY_PORT`: Port to use when `OPENCLAW_GATEWAY_URL` is not set
- `OPENCLAW_GATEWAY_TOKEN`: Bearer token for the gateway
- `OPENCLAW_MODEL`: Model name exposed by the gateway, default: `openclaw/default`

## Project Structure

- `app.py`: Flask backend, route handler, prompt builder, and real OpenClaw API call
- `.env`: Local secret settings loaded at startup, not meant to be committed
- `.env.example`: Safe example file you can copy to `.env`
- `templates/index.html`: Main HTML page
- `static/style.css`: Page styling
- `static/script.js`: Small frontend behavior for the mode buttons
- `requirements.txt`: Python dependency list
- `README.md`: Run instructions and file overview

## How It Works

1. The user pastes text into the textarea.
2. The user clicks one of the three buttons.
3. Flask receives the form submission.
4. `build_prompt(user_text, mode)` creates a mode-specific prompt.
5. `call_openclaw(prompt)` sends a chat completion request to the local OpenClaw gateway and returns the model reply.
6. The response is rendered back onto the page.
