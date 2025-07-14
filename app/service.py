from fastapi import UploadFile, status, HTTPException
import pandas as pd
import io
from requests import RequestException
from app.dto.transacaoDto import TransacaoDto
from app.client.transacaoClient import postarDados
from app.client.produtoClient import obterListaProdutos, buscarIdProdutoPorNome
    
def extrairDadosGranel(arquivo: UploadFile) -> str:
    try:
        conteudo = arquivo.file.read()
        
        # Cria um objeto BytesIO para que o pandas possa ler
        arquivo_excel = io.BytesIO(conteudo)
        
        # Lendo o arquivo e pegando a planilha "Compra a Granel"
        df = pd.read_excel(arquivo_excel, sheet_name='Compra a Granel  ', skiprows=1, nrows=32)

        QtdDadosExtraidos = 0
        primeiraColuna = 0
        segundaColuna = 4
        totalColunas = df.shape[1]
        listaProdutos = obterListaProdutos()
        
        while primeiraColuna < totalColunas:
            bloco_df = df.iloc[1:32, primeiraColuna:segundaColuna]
            bloco_df = bloco_df.dropna(how='all').reset_index(drop=True)
    
            nomeProduto = bloco_df.columns[0]
            idProduto = buscarIdProdutoPorNome(nomeProduto, listaProdutos)

            if(nomeProduto != "Unnamed"):
                print(f"\nProcessando produto: {nomeProduto}")
            
                for index, row in bloco_df.iterrows():
                        
                        data = row.iloc[0]
                        peso = row.iloc[1]
                        valor = row.iloc[2]
                        
                        if(peso != 0 and valor != 0):
                            QtdDadosExtraidos += 1
                            
                            # Categoria 0 sempre será "GR" (Granel) por padrão
                            # Tipo de operação 0 sempre será "Entrada" por padrão
                            dto = TransacaoDto(
                                fkProduto=idProduto,
                                categoria=0,
                                peso=float(peso),
                                valorTotal=float(valor),
                                tipoOperacao=0,
                                fkParceiroComercial=1,
                                fkUsuario=1,
                                data=data.strftime("%Y-%m-%d") if isinstance(data, pd.Timestamp) else str(data)
                            )
                            postarDados(dto)
            primeiraColuna += 4
            segundaColuna += 4
        
        return {
            "message": "Dados extraídos com sucesso!",
            "qtdDadosExtraidos": QtdDadosExtraidos
        }
        
    except RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro de comunicação com o serviço de transações: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao processar a transação: {str(e)}"
        )
