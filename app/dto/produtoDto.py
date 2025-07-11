from pydantic import BaseModel

class produtoDto(BaseModel):
     id: int
     nome: str
