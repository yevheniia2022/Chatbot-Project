import os
from flask import Flask, request, render_template
from google import genai
from google.genai import types

app = Flask(__name__)

# 1. Initialize Gemini Client
# It automatically reads GEMINI_API_KEY from your Render Environment Variables
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Define your specialized context
ENERGYTAG_CONTEXT = (
    "You are an expert on the EnergyTag Standard. "
    "EnergyTag is a non-profit initiative defining a standard for hourly energy certificates. "
    "It enables accurate carbon accounting and links renewable production to consumption in real time."
)

def get_bot_reply(user_input):
    try:
        # Using the March 2026 stable model ID
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=ENERGYTAG_CONTEXT,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        # This will show the real error in your Render Logs for debugging
        print(f"Gemini Error: {e}")
        return "The bot is resting. Please try again in a moment."

@app.route("/", methods=["GET", "POST"])
def index():
    bot_reply = None
    user_input = None
    if request.method == "POST":
        user_input = request.form.get("message")
        if user_input:
            bot_reply = get_bot_reply(user_input)
    
    return render_template("index.html", user_input=user_input, bot_reply=bot_reply)

if __name__ == "__main__":
    # Render provides the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
