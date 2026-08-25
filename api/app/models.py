"""
Definição das tabelas do banco, seguindo o schema especificado na
Seção 6.2.6.8 da metodologia do TCC (usuarios, estufas, leituras_sensores,
deteccoes, alertas).
"""
import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class PapelUsuario(str, enum.Enum):
    produtor = "produtor"
    agronomo = "agronomo"
    admin = "admin"


class ClasseDeteccao(str, enum.Enum):
    saudavel = "saudavel"
    bacteriano = "bacteriano"
    fungico = "fungico"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    papel = Column(Enum(PapelUsuario), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    estufas = relationship("Estufa", back_populates="usuario")


class Estufa(Base):
    __tablename__ = "estufas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    localizacao = Column(String(200), nullable=True)

    usuario = relationship("Usuario", back_populates="estufas")
    leituras = relationship("LeituraSensor", back_populates="estufa")
    deteccoes = relationship("Deteccao", back_populates="estufa")


class LeituraSensor(Base):
    __tablename__ = "leituras_sensores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    estufa_id = Column(Integer, ForeignKey("estufas.id"))
    temperatura = Column(Numeric(5, 2))
    umidade = Column(Numeric(5, 2))
    luminosidade = Column(Integer)
    registrado_em = Column(DateTime(timezone=True), server_default=func.now())

    estufa = relationship("Estufa", back_populates="leituras")


class Deteccao(Base):
    __tablename__ = "deteccoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    estufa_id = Column(Integer, ForeignKey("estufas.id"))
    classe = Column(Enum(ClasseDeteccao), nullable=False)
    confianca = Column(Numeric(4, 3))
    # Campos de bounding box mantidos por compatibilidade com o schema
    # original da tese, mas opcionais: como o modelo está em modo
    # classificação (ver decisão sobre o dataset), eles ficam nulos por
    # enquanto — dá pra preencher futuramente se migrarem para detecção.
    bbox_x = Column(Numeric(6, 4), nullable=True)
    bbox_y = Column(Numeric(6, 4), nullable=True)
    bbox_w = Column(Numeric(6, 4), nullable=True)
    bbox_h = Column(Numeric(6, 4), nullable=True)
    imagem_url = Column(Text)
    detectado_em = Column(DateTime(timezone=True), server_default=func.now())

    estufa = relationship("Estufa", back_populates="deteccoes")
    alertas = relationship("Alerta", back_populates="deteccao")


class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deteccao_id = Column(Integer, ForeignKey("deteccoes.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    enviado_em = Column(DateTime(timezone=True), server_default=func.now())
    lido = Column(Boolean, default=False)

    deteccao = relationship("Deteccao", back_populates="alertas")