"""
Endpoints de autenticação (RF09 da tese).

POST /auth/register  -> cadastra um novo usuário
POST /auth/login      -> autentica e devolve um token de acesso
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth_utils import criar_token, hash_senha, verificar_senha
from app.database import get_db
from app.models import Usuario
from app.schemas import TokenOut, UsuarioLogin, UsuarioOut, UsuarioRegistro

router = APIRouter(prefix="/auth", tags=["autenticacao"])


@router.post("/register", response_model=UsuarioOut, status_code=201)
def register(dados: UsuarioRegistro, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    novo_usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
        papel=dados.papel,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@router.post("/login", response_model=TokenOut)
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

    token = criar_token(usuario.email)
    return TokenOut(access_token=token)