from pydantic import BaseModel

class ProdutoBase(BaseModel):
    nome: str
    descricao: str


class ProdutoRequest(ProdutoBase):
    ...

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
