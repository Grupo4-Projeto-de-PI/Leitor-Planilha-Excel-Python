import requests
from fastapi import UploadFile
import pandas as pd
import io

from app.transacaoDto import TransacaoDto

def testeChamda():
    response = requests.get("http://localhost:8080/produto")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
    
def extrairDados(arquivo: UploadFile) -> str:
    try:
        # Lê o conteúdo do arquivo em bytes
        conteudo = arquivo.file.read()
        
        # Cria um objeto BytesIO para que o pandas possa ler
        arquivo_excel = io.BytesIO(conteudo)
        
        # Lê o arquivo Excel usando pandas
        df = pd.read_excel(arquivo_excel, sheet_name='Compra a Granel  ', skiprows=1, nrows=34)
        df = df.iloc[:, 0:4]
        df = df.dropna(how='all').reset_index(drop=True)
        transacoes = []
        
        # Reseta o ponteiro do arquivo para reutilização se necessário
        arquivo.file.seek(0)
        
        for index, row in df.iterrows():
            data = row[0]
            peso = row[1]
            valor = row[2]
            
            dto = TransacaoDto(
                fkProduto="qualquer_valor",    # você irá aplicar lógica depois
                categoria="granel",
                peso=str(peso),
                valorTotal=str(valor),
                tipoOperacao="entrada",
                fkParceiroComercial=0,
                fkUsuario=0,
                data=data.strftime("%Y-%m-%d") if isinstance(data, pd.Timestamp) else str(data)
            )
            
            transacoes.append(dto)
            
        return transacoes
        
    except Exception as e:
        return f"Erro ao processar arquivo: {str(e)}"
