"""
Funções auxiliares de autenticação: hash de senha e geração/validação
de token de acesso (RF09).
"""
import os
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

# Em produção isso deveria vir de uma variável de ambiente/segredo real.
# Para o TCC, um valor fixo já atende — mas nunca reutilize esse valor
# em um sistema de verdade fora do escopo acadêmico.
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "tcc-estufa-inteligente-dev-secret")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 dia


def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))


def criar_token(email: str) -> str:
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expira_em}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def validar_token(token: str) -> str | None:
    """Retorna o email do usuário se o token for válido, senão None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None