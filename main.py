from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller import router

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens. Para produção, especifique os domínios: ["http://localhost:3000", "https://seudominio.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

app.include_router(router)
