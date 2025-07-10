from fastapi import APIRouter
from app.service import get_greeting

router = APIRouter()

@router.get("/greet/{name}")
def greet(name: str):
    message = get_greeting(name)
    return {"message": message}

@router.get("/test")
def test():
    from app.service import testeChamda
    data = testeChamda()
    return {"dados": data}