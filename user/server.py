from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
AUTH_SERVICE_URL = "http://auth-service:8001"

app = FastAPI()

@app.middleware("http")
async def auth_middleware(request, call_next):
    print("auth middleware")

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/validate", headers=request.headers)
        
    if response.status_code == 200:
        payload = response.json()['payload']
        print(payload)
        request.state.username = payload["username"]
        response = await call_next(request)
        return response
    else:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

@app.get("/")
def read_root(request: Request):
    return {"Info": "user service", "username": request.state.username}


