from http.client import HTTPException
import requests
from scipy import stats
from app.helper.buildUrlHelper import urlBuild

def obterListaProdutos() -> list[dict]:
    response = requests.get(urlBuild("produto"))
    
    if response.status_code == 200:
        resposta = response.json()
        return [{"id": produto['id'], "name": produto['nome']} for produto in resposta]
    else:
        raise Exception("Falha ao buscar produtos: status code " + str(response.status_code))

def buscarIdProdutoPorNome(nomeProduto: str, listaProdutos: list[dict]) -> int:
    for produto in listaProdutos:
        if produto['name'].lower().strip() == nomeProduto.lower().strip():
            return produto['id']
        
    raise HTTPException(
        status_code=stats.HTTP_404_NOT_FOUND,
        detail=f"Produto '{nomeProduto}' não encontrado na lista de produtos"
    )
