"""
Schemas Pydantic: definem o formato JSON que a API recebe e devolve.
Os nomes dos campos aqui são os mesmos que o dashboard Streamlit já espera
(ver api_client.py do projeto webapp) — se mudar algo aqui, ajustar lá também.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LeituraSensorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    estufa_id: int
    temperatura: float
    umidade: float
    luminosidade: int
    registrado_em: datetime


class LeituraSensorIn(BaseModel):
    estufa_id: int
    temperatura: float
    umidade: float
    luminosidade: int


class DeteccaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    estufa_id: int
    classe: str
    confianca: float
    imagem_url: str | None = None
    detectado_em: datetime


class AlertaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    deteccao_id: int
    classe: str
    enviado_em: datetime
    lido: bool
    

class UsuarioRegistro(BaseModel):
    nome: str
    email: str
    senha: str
    papel: str = "produtor"


class UsuarioLogin(BaseModel):
    email: str
    senha: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    papel: str