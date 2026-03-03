import os
from flask import Flask, request, render_template
from openai import OpenAI

app = Flask(__name__)

# Initialize client - Ensure OPENAI_API_KEY is set in Render Environment Variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Combined context for better model performance
SYSTEM_PROMPT = (
    "You are an expert on the EnergyTag Standard. "
    "EnergyTag is a non-profit initiative defining a standard for hourly energy certificates. "
    "It enables accurate carbon accounting, supports storage and flexibility, and builds trust "
    "by linking actual renewable production to consumption in real time."
)

def get_bot_reply(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        # Log the error to the console for debugging
        print(f"OpenAI Error: {e}")
        return "Sorry, I encountered an error processing your request."

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
    # Use the PORT provided by the environment, default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
