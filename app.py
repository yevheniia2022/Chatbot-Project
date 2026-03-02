from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Load your API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

ENERGYTAG_CONTEXT = """
EnergyTag is a non-profit initiative defining a standard for hourly energy certificates.
It enables accurate carbon accounting, supports storage and flexibility, and builds trust
by linking actual renewable production to consumption in real time.
See more at energytag.org.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert on the EnergyTag Standard."},
            {"role": "system", "content": ENERGYTAG_CONTEXT},
            {"role": "user", "content": user_input}
        ]
    )

    answer = response["choices"][0]["message"]["content"]
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
