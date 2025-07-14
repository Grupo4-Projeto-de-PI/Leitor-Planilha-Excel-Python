from fastapi import APIRouter, File, UploadFile

import app

router = APIRouter()

@router.post("/granel/")
def extrairGranel(arquivo: UploadFile = File(...)):
    from app.service import extrairDadosGranel
    data = extrairDadosGranel(arquivo)
    return data

# @router.post("/material-separado/")
# def extrairMaterialSeparado(arquivo: UploadFile = File(...)):
#     from app.service import extrairDados
#     data = extrairDados(arquivo)
#     return data

# @router.post("/saida/")
# def extrairSaida(arquivo: UploadFile = File(...)):
#     from app.service import extrairDados
#     data = extrairDados(arquivo)
#     return data
