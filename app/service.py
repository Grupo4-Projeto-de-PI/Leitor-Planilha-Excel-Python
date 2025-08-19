from fastapi import UploadFile, status, HTTPException
import pandas as pd
import io
from requests import RequestException
from app.dto.transacaoDto import TransacaoDto
from app.client.transacaoClient import postarDados
from app.client.produtoClient import obterListaProdutos, buscarIdProdutoPorNome

def extrairDadosPlanilha(arquivo: UploadFile, nomePlanilha: str, coluna2: int, tipoOperacao: int, tipoCategoria: int, nrows: int) -> str:
    try:
        conteudo = arquivo.file.read()
        
        # Cria um objeto BytesIO para que o pandas possa ler
        arquivo_excel = io.BytesIO(conteudo)
        
        # Lendo o arquivo e pegando a planilha "Compra a Granel"
        df = pd.read_excel(arquivo_excel, sheet_name=f'{nomePlanilha}', skiprows=1, nrows=nrows)

        QtdDadosExtraidos = 0
        primeiraColuna = 0
        segundaColuna = coluna2
        totalColunas = df.shape[1]
        listaProdutos = obterListaProdutos()
        
        while primeiraColuna < totalColunas:
            bloco_df = df.iloc[1:min(32, len(df)), primeiraColuna:segundaColuna]
            bloco_df = bloco_df.dropna(how="all").reset_index(drop=True)
            bloco_df = bloco_df[~bloco_df.iloc[:, 0].astype(str).str.contains("Valor total", na=False)]
    
            if bloco_df.empty or bloco_df.shape[1] < 3:
                primeiraColuna += 4
                segundaColuna += 4
                continue

            nomeProduto = bloco_df.columns[0]
            idProduto = buscarIdProdutoPorNome(nomeProduto, listaProdutos)
            if idProduto is None:
                print(f"Produto {nomeProduto} não encontrado, pulando.")
                primeiraColuna += 4
                segundaColuna += 4
                continue

            # Categoria 0 sempre será "GR" (Granel), Categoria 1 sempre será "MS" (Material Separado) 
            # Tipo de operação 0 sempre será "Entrada", Tipo de Operação 1 sempre será "Saida"
            for index, row in bloco_df.iterrows():
                data, peso, valor = row.iloc[0], row.iloc[1], row.iloc[2]
                if pd.notna(peso) and pd.notna(valor) and peso != 0 and valor != 0:
                    dto = TransacaoDto(
                        fkProduto=idProduto,
                        categoria=tipoCategoria,
                        peso=float(peso),
                        valorTotal=float(valor),
                        tipoOperacao=tipoOperacao,
                        fkParceiroComercial=None,
                        fkUsuario=None,
                        data=data.strftime("%Y-%m-%d") if isinstance(data, pd.Timestamp) else str(data)
                    )
                    postarDados(dto)
                    QtdDadosExtraidos += 1

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
