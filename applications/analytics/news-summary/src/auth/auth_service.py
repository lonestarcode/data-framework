from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
from passlib.context import CryptContext
from src.database.models.user import User, UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, secret_key: str, token_expire_minutes: int = 30):
        self.secret_key = secret_key
        self.token_expire_minutes = token_expire_minutes

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, user: User) -> str:
        expires_delta = timedelta(minutes=self.token_expire_minutes)
        expire = datetime.utcnow() + expires_delta
        
        to_encode = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "exp": expire
        }
        return jwt.encode(to_encode, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.PyJWTError:
            return None 