from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
import httpx
# import logging
# import requests

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
        response = await client.get(f"{AUTH_SERVICE_URL}/validate", headers={"Authorization": token})

    if response.status_code == 200:
        res = response.json()
        return res
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


async def validate_token(token):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTH_SERVICE_URL}/validate", headers={"Authorization": token})
        if response.status_code == 200:
            return response.json()
        else:
            return False


@app.api_route("/user/{user_path:path}", methods=["GET", "POST"])
async def user(request: Request, user_path: str):
    token = request.headers.get("Authorization")
    is_valid = await validate_token(token)
    user_name = is_valid['payload']['username']
    if request.method == "GET":
        if is_valid:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{USER_SERVICE_URL}/{user_name}/{user_path}", headers={"Authorization": token}, follow_redirects=True)
            except Exception:
                raise HTTPException(status_code=500, detail="Internal server error")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    if request.method == "POST":
        body = await request.json()
        if is_valid:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{USER_SERVICE_URL}/{user_name}/{user_path}", headers={"Authorization": token}, json=body, follow_redirects=True)
            except Exception:
                raise HTTPException(status_code=500, detail="Internal server error")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized")
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="Page not found")
    else:
        raise HTTPException(status_code=500, detail="Internal server error")

# @api.route("/news", methods=["GET","POST"])
#     token = request.headers.get("Authorization")
#     is_valid = await validate_token(token)
#     user_name = is_valid['payload']['username']
#     if is_valid:
#         if request.method == "GET":
#             try:
#                 async with httpx.AsyncClient() as client:
#                 response = await client.get(f"{USER_SERVICE_URL}/{}", headers={"Authorization": token}, follow_redirects=True)
