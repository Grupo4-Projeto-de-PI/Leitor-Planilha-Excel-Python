from fastapi import UploadFile
import pandas as pd
import io
from app.dto.transacaoDto import TransacaoDto
from app.helper.transacaoHelper import postarDados
from app.helper.produtoHelper import obterListaProdutos, buscarIdProdutoPorNome
    
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
            # print("Dados extraídos e postados com sucesso \n Quantidade de dados extraídos da Planilha de Granel: " + str(QtdDadosExtraidos))
                
    except Exception as e:
        return f"Erro ao processar arquivo: {str(e)}"
