from fastapi import HTTPException, status
import requests
from requests.exceptions import RequestException
from app.dto.transacaoDto import TransacaoDto
from app.helper.buildUrlHelper import urlBuild

def postarDados(transacaoDto: TransacaoDto) -> str:   
        response = requests.post(
            urlBuild("transacoes"),
            json=transacaoDto.model_dump())
        
        response.raise_for_status()  # Levanta um erro se a requisição falhar
        return response
    