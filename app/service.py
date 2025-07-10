import requests
from fastapi import UploadFile
import pandas as pd

def testeChamda():
    response = requests.get("http://localhost:8080/usuario")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
    
def extrairDados(arquivo: UploadFile) -> str:
    return {
        "filename": arquivo.filename,
    }