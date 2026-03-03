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
        # UPDATED MODEL ID: 'gemini-2.0-flash' is the stable 2026 free-tier workhorse.
        # If this still 404s, 'gemini-1.5-flash' is the guaranteed fallback.
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=ENERGYTAG_CONTEXT,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        # This logs the specific error to Render so we can see it
        print(f"Gemini Error: {e}")
        return f"Error: {str(e)}" # Temporarily show the error on screen to debug

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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
