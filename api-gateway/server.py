from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging
import requests

AUTH_SERVICE_URL = "http://auth-service:8001"
USER_SERVICE_URL = "http://user-service:8002"

app = FastAPI()

origins = [
    "http://0.0.0.0:3000",
    "http://localhost:3000",
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

# def validate_token(token):
#     response = requests.post(f"{AUTH_SERVICE_URL}/validate", headers={"Authorization": token})
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return False

@app.get("/user/{user_path:path}")
async def user(request: Request, user_path: str):
    token = request.headers.get("Authorization")

    try:
        body = await request.json()
    except:
        body = None

    # is_valid = validate_token(token)
    try: 
        async with httpx.AsyncClient() as client:
            if body:
                response = await client.get(f"{USER_SERVICE_URL}/{user_path}", headers={"Authorization": token}, json=body)
            else:
                response = await client.get(f"{USER_SERVICE_URL}/{user_path}", headers={"Authorization": token})
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized")
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="Page not found")
    else:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/user/{user_path:path}")
async def user(request: Request, user_path: str):
    token = request.headers.get("Authorization")

    try:
        body = await request.json()
    except:
        body = None

    # is_valid = validate_token(token)
    try: 
        async with httpx.AsyncClient() as client:
            if body:
                response = await client.post(f"{USER_SERVICE_URL}/{user_path}", headers={"Authorization": token}, json=body)
            else:
                response = await client.post(f"{USER_SERVICE_URL}/{user_path}", headers={"Authorization": token})
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    #
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized")
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="Page not found")
    else:
        raise HTTPException(status_code=500, detail="Internal server error")
