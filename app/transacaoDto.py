from pydantic import BaseModel
from typing import Optional, List

class TransacaoDto(BaseModel):
     fkProduto: str
     categoria: str = "granel"
     peso: str
     valorTotal: str
     tipoOperacao: str = "entrada"
     fkParceiroComercial: int = 0
     fkUsuario: int = 0
     data: str
