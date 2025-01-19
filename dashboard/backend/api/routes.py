from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import random

api_bp = Blueprint('api', __name__)

@api_bp.route('/analytics/data', methods=['GET'])
def get_analytics():
    time_range = request.args.get('timeRange', '24h')
    hours = int(time_range.replace('h', ''))
    
    # Mock data generation
    data = []
    now = datetime.now()
    for i in range(hours):
        data.append({
            "id": str(i + 1),
            "timestamp": (now - timedelta(hours=i)).isoformat(),
            "scrapeCount": random.randint(80, 200),
            "filterPassRate": round(random.uniform(0.75, 0.95), 2),
            "avgQualityScore": round(random.uniform(0.85, 0.98), 2),
            "avgProcessingTime": random.randint(100, 200)
        })
    return jsonify(data)

@api_bp.route('/filters', methods=['GET'])
def get_filters():
    filters = [
        {
            "id": "1",
            "name": "Quality Filter",
            "type": "number",
            "field": "quality",
            "operator": "greaterThan",
            "value": 0.8
        }
    ]
    return jsonify(filters)

@api_bp.route('/chat/message', methods=['POST'])
def send_message():
    data = request.json
    response = {
        "message": f"Received: {data.get('message')}",
        "timestamp": datetime.now().isoformat()
    }
    return jsonify(response)
