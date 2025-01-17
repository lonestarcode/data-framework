from functools import wraps
from flask import request, jsonify
from typing import List, Callable
from src.database.models.user import UserRole

def require_auth(roles: List[UserRole] = None) -> Callable:
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "No valid token provided"}), 401

            token = auth_header.split(' ')[1]
            payload = auth_service.verify_token(token)
            
            if not payload:
                return jsonify({"error": "Invalid token"}), 401

            if roles and UserRole(payload["role"]) not in roles:
                return jsonify({"error": "Insufficient permissions"}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator 