import requests
from fastapi import UploadFile
import pandas as pd
import io
from app.transacaoDto import TransacaoDto

def postarDados(transacaoDto: TransacaoDto) -> str:
    response = requests.post(
        "http://localhost:8080/transacoes",
        json=transacaoDto.model_dump())
    
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
        df = pd.read_excel(arquivo_excel, sheet_name='Compra a Granel  ', skiprows=1, nrows=32)
        # Pegando as 4 primeiras colunas do data frame
        df = df.iloc[1:32, 0:4]
        print(df)
        
        # Não sei o que essa linha faz, mas estava no código original
        df = df.dropna(how='all').reset_index(drop=True)
        transacoes = []
        
        # Reseta o ponteiro do arquivo para reutilização se necessário
        arquivo.file.seek(0)
        
        for index, row in df.iterrows():
            data = row.iloc[0]
            peso = row.iloc[1]
            valor = row.iloc[2]
            
            dto = TransacaoDto(
                fkProduto=1,
                categoria=0,
                peso=float(peso),
                valorTotal=float(valor),
                tipoOperacao=1,
                fkParceiroComercial=1,
                fkUsuario=1,
                data=data.strftime("%Y-%m-%d") if isinstance(data, pd.Timestamp) else str(data)
            )
            transacoes.append(dto)
            
        print(transacoes[1])
        postarDados(transacoes[1])
        
    except Exception as e:
        return f"Erro ao processar arquivo: {str(e)}"
