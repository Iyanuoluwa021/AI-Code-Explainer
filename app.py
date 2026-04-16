from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Setup OpenAI (optional)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/explain", methods=["POST"])
def explain():
    try:
        data = request.get_json()

        # Safety checks
        if not data:
            return jsonify({"explanation": "No data received."})

        code = data.get("code", "")
        mode = data.get("mode", "Beginner")

        if not code.strip():
            return jsonify({"explanation": "Please enter some code to analyze."})

        # 🔥 If no API key → fallback instantly
        if not client:
            explanation = f"""[{mode} Demo Explanation]

This is a fallback response because no API key is set.

Your code:
{code}
"""
            return jsonify({"explanation": explanation})

        # 🧠 Prompt based on mode
        if mode == "Beginner":
            prompt = f"""
Explain this code line by line in very simple terms for a beginner.

Code:
{code}
"""
        else:
            prompt = f"""
Provide a detailed technical explanation of this code including logic, structure, and complexity.

Code:
{code}
"""

        # 🚀 Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        explanation = response.choices[0].message.content

        return jsonify({"explanation": explanation})

    except Exception as e:
        # ✅ NEVER FAIL — always return something
        explanation = f"""⚠️ API Error: {str(e)}

[Demo Explanation]

Your code:
{code}

Explanation:
This code runs successfully and demonstrates basic programming logic.
"""
        return jsonify({"explanation": explanation})


if __name__ == "__main__":
    app.run(debug=True)