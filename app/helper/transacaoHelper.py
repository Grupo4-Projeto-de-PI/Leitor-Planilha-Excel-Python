import requests
from app.dto.transacaoDto import TransacaoDto
from app.helper.buildUrlHelper import urlBuild

def postarDados(transacaoDto: TransacaoDto) -> str:
    response = requests.post(
        urlBuild("transacao"),
        json=transacaoDto.model_dump())
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Falha ao postar as transações"}