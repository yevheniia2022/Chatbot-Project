from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    # Replace this with your chatbot logic
    return jsonify({"response": f"You said: {user_input}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
