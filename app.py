import os
from flask import Flask, request, render_template
from google import genai
from google.genai import types

app = Flask(__name__)

# 1. Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Specialized EnergyTag context with strict scope
ENERGYTAG_CONTEXT = (
    "You are the EnergyTag AI Assistant. "
    "You must ONLY answer questions related to the EnergyTag standard, hourly energy certificates, "
    "carbon accounting, renewable energy tracking, and related policy/audit contexts. "
    "If asked about anything else, politely respond: 'I can only answer questions about the EnergyTag standard.'"
)

# Allowed topics for input pre-filter
ALLOWED_TOPICS = ["energytag", "certificate", "carbon", "renewable", "audit", "policy"]

def is_on_topic(user_input):
    return any(topic in user_input.lower() for topic in ALLOWED_TOPICS)

def get_bot_reply(user_input):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=ENERGYTAG_CONTEXT,
                temperature=0.3  # lower temperature for focus
            )
        )
        reply = response.text

        # Guardrail: enforce EnergyTag scope in output
        keywords = ["energytag", "certificate", "carbon", "renewable", "audit", "policy"]
        if not any(word in reply.lower() for word in keywords):
            return "I can only answer questions about the EnergyTag standard."
        return reply

    except Exception as e:
        print(f"Gemini Error: {e}")
        return f"Wait, the bot is thinking too hard! (Error: {str(e)})"

@app.route("/", methods=["GET", "POST"])
def index():
    bot_reply = None
    user_input = None
    if request.method == "POST":
        user_input = request.form.get("message")
        if user_input:
            if is_on_topic(user_input):
                bot_reply = get_bot_reply(user_input)
            else:
                bot_reply = "I can only answer questions about the EnergyTag standard."
    return render_template("index.html", user_input=user_input, bot_reply=bot_reply)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
