from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# Load API key from environment (already set in Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

ENERGYTAG_CONTEXT = """
EnergyTag is a non-profit initiative defining a standard for hourly energy certificates.
It enables accurate carbon accounting, supports storage and flexibility, and builds trust
by linking actual renewable production to consumption in real time.
See more at energytag.org.
"""

def get_bot_reply(user_input):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # lightweight model
        messages=[
            {"role": "system", "content": "You are an expert on the EnergyTag Standard. Use the context provided to answer clearly."},
            {"role": "system", "content": ENERGYTAG_CONTEXT},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["message"]
        bot_reply = get_bot_reply(user_input)
        return render_template("index.html", user_input=user_input, bot_reply=bot_reply)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
