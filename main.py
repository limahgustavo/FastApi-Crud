from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from models import Produto
from database import engine, Base, get_db
from repositories import ProdutoRepository
from schemas import ProdutoRequest, ProdutoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def create(request: ProdutoRequest, db: Session = Depends(get_db)):
    produto = ProdutoRepository.save(db, Produto(**request.dict()))
    return ProdutoResponse.from_orm(produto)

@app.get("/api/produtos", response_model=list[ProdutoResponse])
def find_all(db: Session = Depends(get_db)):
    protudos = ProdutoRepository.find_all(db)
    return [ProdutoResponse.from_orm(protudo) for protudo in protudos]

@app.get("/api/produtos/{id}", response_model=ProdutoResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    protudo = ProdutoRepository.find_by_id(db, id)
    if not protudo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Protudo não encontrado"
        )
    return ProdutoResponse.from_orm(protudo)

@app.delete("/api/produtos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not ProdutoRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Protudo não encontrado"
        )
    ProdutoRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/api/produtos/{id}", response_model=ProdutoResponse)
def update(id: int, request: ProdutoRequest, db: Session = Depends(get_db)):
    if not ProdutoRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Protudo não encontrado"
        )
    protudo = ProdutoRepository.save(db, Produto(id=id, **request.dict()))
    return ProdutoResponse.from_orm(protudo)
