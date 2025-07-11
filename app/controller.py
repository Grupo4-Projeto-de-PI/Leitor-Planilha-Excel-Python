from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/extract/")
def extract(arquivo: UploadFile = File(...)):
    from app.service import extrairDados
    data = extrairDados(arquivo)
    return data

@router.get("/produtos/")
def get_produtos():
    from app.service import buscarProdutos
    produtos = buscarProdutos()
    return produtos