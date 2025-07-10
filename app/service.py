import requests

def get_greeting(name: str) -> str:
    return f"Olá, {name}! Seja bem-vindo à nossa API."

def testeChamda():
    response = requests.get("http://localhost:8080/usuario")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}