from fastapi import APIRouter, File, UploadFile
from app.service import extrairDados

router = APIRouter()

@router.post("/extract/")
def extract(arquivo: UploadFile = File(...)):
    from app.service import extrairDados
    data = extrairDados(arquivo)
    return {"Arquivo": data}