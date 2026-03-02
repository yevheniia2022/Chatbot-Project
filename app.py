from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def search_energytag(query):
    # Example: integrate Bing or other search API
    response = requests.get("https://api.bing.microsoft.com/v7.0/search",
                            headers={"Ocp-Apim-Subscription-Key": "YOUR_KEY"},
                            params={"q": query})
    results = response.json()
    return results["webPages"]["value"][0]["snippet"]

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message").lower()
    
    if "standard" in user_input:
        answer = "EnergyTag’s Granular Certificate Scheme Standard defines how renewable energy certificates are issued hourly. More at http://www.energytag.org."
    elif "publication" in user_input or "report" in user_input:
        answer = "EnergyTag publishes reports like 'European Power – How Clean, How Cheap' and 'Response to Call for Evidence on Barriers to PPAs'. See http://www.energytag.org/publications."
    elif "case study" in user_input:
        answer = "Example: Tata Power Renewables + Flexidao delivered India’s first hourly carbon-free electricity solution in 2025. More case studies at http://www.energytag.org/case-studies."
    elif "event" in user_input:
        answer = "Recent events include Eurelectric Power Summit (June 2026), European Sustainable Energy Week (July 2026), and REM Asia (April 2026)."
    elif "latest" in user_input:
        answer = search_energytag("EnergyTag updates 2026")
    else:
        answer = "EnergyTag develops standards for granular energy certificates, enabling 24/7 clean energy tracking. Learn more at http://www.energytag.org."
    
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
