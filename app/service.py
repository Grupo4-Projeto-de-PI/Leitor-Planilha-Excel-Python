from fastapi import UploadFile, status, HTTPException
import pandas as pd
import io
from requests import RequestException
from app.dto.transacaoDto import TransacaoDto
from app.client.transacaoClient import postarDados
from app.client.produtoClient import obterListaProdutos, buscarIdProdutoPorNome
import os
from datetime import datetime
import tempfile

def verificar(arquivo: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(arquivo.file.read())
        temp_path = temp_file.name

    estatisticas = os.stat(temp_path)
    data_criacao = datetime.fromtimestamp(estatisticas.st_ctime)
    data_str = data_criacao.strftime('%Y-%m-%d %H:%M:%S')

    arquivo_duplicidade = './arqDuplicidade'
    if os.path.exists(arquivo_duplicidade):
        with open(arquivo_duplicidade, 'r') as f:
            if data_str in f.read():
                os.remove(temp_path)
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Arquivo com essa data já foi registrado. Ação bloqueada."
                )

    with open(arquivo_duplicidade, 'a') as f:
        f.write(data_str + '\n')

    os.remove(temp_path)
    print("Arquivo registrado com sucesso.")
    return True

def extrairDadosPlanilha(arquivo: UploadFile, nomePlanilha: str, coluna2: int, tipoOperacao: int, tipoCategoria: int, nrows: int) -> str:  
    try:
        conteudo = arquivo.file.read()
        verificar(arquivo)
    
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
                    # Formata a data para ISO 8601 com hora
                    if isinstance(data, pd.Timestamp):
                        data_formatada = data.strftime("%Y-%m-%dT00:00:00")
                    else:
                        # Se for string, tenta converter e formatar
                        data_formatada = str(data).replace(" ", "T") if "T" not in str(data) else str(data)
                        if len(data_formatada) == 10:  # Apenas data YYYY-MM-DD
                            data_formatada += "T00:00:00"
                    
                    dto = TransacaoDto(
                        fkProduto=idProduto,
                        categoria=tipoCategoria,
                        peso=float(peso),
                        valorTotal=float(valor),
                        tipoOperacao=tipoOperacao,
                        fkParceiroComercial=None,
                        fkUsuario=None,
                        data=data_formatada
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
