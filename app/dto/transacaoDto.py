from pydantic import BaseModel
from typing import Optional, List

class TransacaoDto(BaseModel):
     fkProduto: int
     categoria: int
     peso: float
     valorTotal: float
     tipoOperacao: int
     fkParceiroComercial: Optional[int] = None
     fkUsuario: Optional[int] = None
     data: str
