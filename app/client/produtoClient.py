import requests
from app.helper.buildUrlHelper import urlBuild

def obterListaProdutos() -> list[dict]:
    response = requests.get(urlBuild("produto"))
    
    resposta = response.json()
    response.raise_for_status() # Levanta um erro se a requisição falhar
    return [{"id": produto['id'], "name": produto['nome']} for produto in resposta]
    
def buscarIdProdutoPorNome(nomeProduto: str, listaProdutos: list[dict]) -> int:
    for produto in listaProdutos:
        if produto['name'].lower().strip() == nomeProduto.lower().strip():
            return produto['id']
