import pandas as pd
import database.configBD as bd
from dotenv import load_dotenv, set_key

load_dotenv()

def main():
    planilha = pd.ExcelFile('C:/Users/lucas/Downloads/Documentacoes_M.C-Plasticos/Artefatos de Regra de Negócio/CE_M.C-Plasticos_ControleEstoqueAtual.xlsx')

    compraAGranel = pd.read_excel(planilha, sheet_name='Compra a Granel  ', skiprows=1, nrows=34)
    porProduto = compraAGranel.iloc[:, 0:4]

    print(porProduto)


if __name__ == "__main__":
    main()