from fastapi import APIRouter, File, UploadFile
from app.service import extrairDados

router = APIRouter()

@router.post("/extract/")
def extract(arquivo: UploadFile = File(...)):
    from app.service import extrairDados
    data = extrairDados(arquivo)
    print(data)
    return {"Arquivo": data}

@router.get("/test/")
def test():
    from app.service import testeChamda
    data = testeChamda()
    print(data)
    return {"Teste": data}