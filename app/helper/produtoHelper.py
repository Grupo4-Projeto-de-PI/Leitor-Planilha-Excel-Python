import requests
from app.helper.buildUrlHelper import urlBuild

def buscarProdutos() -> str:
    response = requests.get(urlBuild("produto"))
    
    if response.status_code == 200:
        resposta = response.json()
        produtosName = []    
        
        for produto in resposta: 
            produtosName.append({"id": produto['id'], "name": produto['nome']})
            
        return produtosName
    else:
        return {"error": "Falha ao buscar produtos"}