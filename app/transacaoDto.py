from pydantic import BaseModel
from typing import Optional, List

class TransacaoDto(BaseModel):
     fkProduto: int
     categoria: int
     peso: float
     valorTotal: float
     tipoOperacao: int
     fkParceiroComercial: int = 0
     fkUsuario: int = 0
     data: str
