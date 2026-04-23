"""
app.py
------
Flask REST API for the School Rule-Based Chatbot.
Exposes a single /chat endpoint that accepts POST requests
and returns JSON chatbot responses.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from chatbot import get_bot_response

# ── App setup ─────────────────────────────────────────────────────────────────
app = Flask(__name__)

# Allow all origins during development (restrict in production)
CORS(app)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    """Health-check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "SchoolBot API is running. POST to /chat to talk."
    })


@app.route("/chat", methods=["POST"])
def chat():
    """
    Chat endpoint.

    Expects JSON body:
        { "message": "<user text>" }

    Returns JSON:
        {
            "response"  : "<bot reply>",
            "intent"    : "<matched intent | unknown>",
            "confidence": "<matched | fallback>"
        }
    """
    data = request.get_json(silent=True)

    # ── Input validation ───────────────────────────────────────────────────
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Field 'message' is required and cannot be empty."}), 400

    if len(user_message) > 500:
        return jsonify({"error": "Message is too long. Max 500 characters."}), 400

    # ── Core logic ─────────────────────────────────────────────────────────
    result = get_bot_response(user_message)

    return jsonify(result), 200


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  🎓 SchoolBot API starting...")
    print("  📡 Listening at http://127.0.0.1:5000")
    print("  POST /chat  →  { \"message\": \"your question\" }")
    print("=" * 55)
    app.run(debug=True, port=5000)



