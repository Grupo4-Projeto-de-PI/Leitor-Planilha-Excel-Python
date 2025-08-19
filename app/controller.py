from fastapi import APIRouter, File, UploadFile

import app

router = APIRouter()

@router.post("/granel/")
def extrairGranel(arquivo: UploadFile = File(...)):
    from app.service import extrairDadosPlanilha
    resposta = extrairDadosPlanilha(arquivo, 'Compra a Granel  ', 4, 0, 0, 32)
    return resposta

@router.post("/material-separado/")
def extrairMaterialSeparado(arquivo: UploadFile = File(...)):
    from app.service import extrairDadosPlanilha
    data = extrairDadosPlanilha(arquivo, 'Compra Material Separado', 4, 0, 1, 16)
    return data

@router.post("/saida/")
def extrairSaida(arquivo: UploadFile = File(...)):
    from app.service import extrairDadosPlanilha
    data = extrairDadosPlanilha(arquivo, ' Saída', 4, 1, 1, 16)
    return data
