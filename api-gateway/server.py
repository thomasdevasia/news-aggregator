from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging
import requests

AUTH_SERVICE_URL = "http://auth-service:8001"

app = FastAPI()

origins = [
    "http://0.0.0.0:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"info": "api-gateway service"}

security = HTTPBasic()

@app.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):

    # Forward the request to the auth service
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/login", auth=(credentials.username, credentials.password))
    
    res = response.json()
    res["status_code"] = response.status_code
    return res

@app.post("/signup")
async def signup(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/createUser", json=body)
    
    res = response.json()
    res["status_code"] = response.status_code
    return res

# verify token . Bearer token authentication
@app.post("/validate")
async def validate(request: Request):
    token = request.headers.get("Authorization")
    print(token)

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/validate", headers={"Authorization": token})
    
    if response.status_code == 200:
        res = response.json()
        return res
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
