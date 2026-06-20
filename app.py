import json
import os
import urllib.error
import urllib.request

from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_openclaw_base_url():
    """Return the local OpenClaw gateway base URL."""
    return os.getenv(
        "OPENCLAW_GATEWAY_URL",
        f"http://127.0.0.1:{os.getenv('OPENCLAW_GATEWAY_PORT', '18789')}/v1",
    )


def get_openclaw_model():
    """Return the model name exposed by the local gateway."""
    return os.getenv("OPENCLAW_MODEL", "openclaw/default")


def build_prompt(user_text, mode):
    """Create a different prompt for each study mode."""
    if mode == "summarise":
        return (
            "Summarise the following notes in a clear beginner-friendly way:\n\n"
            f"{user_text}"
        )
    if mode == "quiz":
        return (
            "Generate a short quiz with questions and answers based on these notes:\n\n"
            f"{user_text}"
        )
    if mode == "explain":
        return (
            "Explain the code below in simple language, step by step:\n\n"
            f"{user_text}"
        )
    return f"Process this text:\n\n{user_text}"


def call_openclaw(prompt):
    """Send the prompt to the local OpenClaw gateway and return the reply."""
    url = f"{get_openclaw_base_url().rstrip('/')}/chat/completions"
    token = os.getenv("OPENCLAW_GATEWAY_TOKEN", "")

    payload = {
        "model": get_openclaw_model(),
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are OpenClaw Study Assistant. "
                    "Answer clearly, briefly, and in a beginner-friendly way."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    headers = {
        "Content-Type": "application/json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request_data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=request_data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", "replace")
        return f"OpenClaw request failed ({error.code}).\n\n{error_body}"
    except urllib.error.URLError as error:
        return f"Could not reach OpenClaw at {url}.\n\n{error.reason}"

    try:
        data = json.loads(body)
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, json.JSONDecodeError):
        return f"OpenClaw returned an unexpected response:\n\n{body}"


@app.route("/", methods=["GET", "POST"])
def index():
    user_text = ""
    selected_mode = "summarise"
    ai_response = None

    if request.method == "POST":
        user_text = request.form.get("user_text", "").strip()
        selected_mode = request.form.get("mode", "summarise")

        if user_text:
            prompt = build_prompt(user_text, selected_mode)
            ai_response = call_openclaw(prompt)
        else:
            ai_response = "Please paste some text before choosing a mode."

    return render_template(
        "index.html",
        user_text=user_text,
        selected_mode=selected_mode,
        ai_response=ai_response,
    )


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
    )
