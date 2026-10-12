from fastapi import HTTPException, status
from jose import jwt, JWTError
import bcrypt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))
TOKEN_EXPIRE_MINUTES = str(os.getenv("TOKEN_EXPIRE_MINUTES"))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não foi configurada.")


class AuthService:
    def __init__(self, database, dao_class):
        # dao_class deve ser um DAO, por exemplo UserEmployeeDAO
        self.dao = dao_class(database)

    @staticmethod
    def hash_password(password: str) -> str:
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
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido, expirado ou utilizador inexistente.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != expected_type:
                raise credentials_exception

            user_id = int(str(payload.get("sub")))

        except (JWTError, TypeError, ValueError):
            raise credentials_exception

        user = self.dao.find_by_id(user_id)

        if not user:
            raise credentials_exception

            # Ajusta esta regra se o campo status não for booleano.
        if not user.status:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Utilizador desactivado."
            )

        return user
