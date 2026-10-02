from typing import TypeVar, Generic, Type
T = TypeVar("T")

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import bcrypt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))
TOKEN_EXPIRE_MINUTES = str(os.getenv("TOKEN_EXPIRE_MINUTES"))


class AuthService:
    def __init__(self, database: Session, model: Type[T]):
        # self.database = database
        self.model = model(database)


    @staticmethod
    def _hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(
            password_bytes,
            bcrypt.gensalt(rounds=12),
        )
        return hashed_bytes.decode("utf-8")

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash.encode("utf-8"),
        )

    @staticmethod
    def create_token(user_id: int, token_duration=timedelta(minutes=int(TOKEN_EXPIRE_MINUTES)),
                     token_type="access") -> str:
        token_date_expires = datetime.now(timezone.utc) + token_duration
        token_json = {
            "sub": str(user_id),
            "type": token_type,
            "exp": token_date_expires,
            "iat": datetime.now(timezone.utc),
            # 'extra_logs': user_log
            # "role": user.user_type,
        }
        return jwt.encode(token_json, SECRET_KEY, ALGORITHM)

    def verify_token(self, token: str, expected_type: str = "access"):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != expected_type:
                raise ValueError
            user_id = int(str(payload.get("sub")))

            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token without user ID")

            # user_id = int(user_id)

        except (JWTError, TypeError, ValueError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired")

        # user = self.dao.find_by_id(user_id)
        user = self.model.find_by_id(user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token user not found")
        return user
