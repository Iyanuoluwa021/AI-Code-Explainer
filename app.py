from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None
    print("Warning: OPENAI_API_KEY not set. Responses will be mocked.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/explain", methods=["POST"])
def explain():
    data = request.json
    code = data.get("code")
    mode = data.get("mode", "Beginner")

    if not code:
        return jsonify({"explanation": "Please enter some code to analyze."})

    # If API key missing or quota issue, return mock response
    if client is None:
        explanation = f"[{mode} explanation]\nYour code is:\n{code}"
        return jsonify({"explanation": explanation})

    # Set prompt based on mode
    if mode == "Beginner":
        prompt = f"""
You are a programming teacher explaining code to a beginner.
Explain the following code line by line in simple terms.
Avoid jargon and provide clear examples.

Code:
{code}
"""
    else:
        prompt = f"""
You are an expert software engineer.
Analyze the following code in detail.
Explain the logic, structure, algorithms, possible optimizations, and time/space complexity.

Code:
{code}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        explanation = response.choices[0].message.content
        return jsonify({"explanation": explanation})

    except Exception as e:
        # Fallback: always return explanation for demo
        explanation = f"Server error: {str(e)}\n[Demo explanation]\nYour code is:\n{code}"
        return jsonify({"explanation": explanation})

if __name__ == "__main__":
    app.run(debug=True)