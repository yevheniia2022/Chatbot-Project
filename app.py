import os
from flask import Flask, request, render_template
from openai import OpenAI

app = Flask(__name__)

# Initialize the OpenAI client using the Environment Variable from Render
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

ENERGYTAG_CONTEXT = """
EnergyTag is a non-profit initiative defining a standard for hourly energy certificates.
It enables accurate carbon accounting, supports storage and flexibility, and builds trust
by linking actual renewable production to consumption in real time.
See more at energytag.org.
"""

def get_bot_reply(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert on the EnergyTag Standard. Use the context provided to answer clearly."},
                {"role": "system", "content": ENERGYTAG_CONTEXT},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to OpenAI: {str(e)}"

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
    # Standard Flask port for local testing; Render uses Gunicorn in production
    app.run(host="0.0.0.0", port=5000)
