from sqlalchemy import Column, Integer, String

from database import Base

class Produto(Base):
    __tablename__ = "produto"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(100), nullable=False)
    descricao: str = Column(String(255), nullable=False)
