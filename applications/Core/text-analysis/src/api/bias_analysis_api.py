# src/api/bias_analysis_api.py
from flask import Flask, jsonify, request
from models.bias_analysis.bias_detection import analyze_bias

app = Flask(__name__)

@app.route('/analyze_bias', methods=['POST'])
def analyze_bias_endpoint():
    texts = request.json.get('texts', [])
    results = analyze_bias(texts)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)