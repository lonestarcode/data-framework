from flask import Blueprint, request, jsonify
from src.auth.auth_service import AuthService
from src.database.models.user import User, UserRole

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService(secret_key="your-secret-key")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400
        
    user = User(
        email=data['email'],
        password_hash=auth_service.get_password_hash(data['password']),
        role=UserRole.USER
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not auth_service.verify_password(
        data['password'], user.password_hash
    ):
        return jsonify({"error": "Invalid credentials"}), 401
        
    token = auth_service.create_access_token(user)
    return jsonify({"access_token": token, "token_type": "bearer"}) 