import os
from flask import Flask, request, render_template
from google import genai

app = Flask(__name__)

# Initialize Google Gemini Client
# It will automatically look for GEMINI_API_KEY in your Render environment variables
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = (
    "You are an expert on the EnergyTag Standard. "
    "EnergyTag is a non-profit initiative defining a standard for hourly energy certificates. "
    "It enables accurate carbon accounting and links renewable production to consumption in real time."
)

def get_bot_reply(user_input):
    try:
        # Using Gemini 3 Flash (The latest free model in March 2026)
        response = client.models.generate_content(
            model="gemini-3-flash",
            contents=[SYSTEM_PROMPT, user_input]
        )
        return response.text
    except Exception as e:
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
