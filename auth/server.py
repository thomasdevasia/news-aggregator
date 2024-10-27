from datetime import timedelta, datetime
import hashlib
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from pydantic import BaseModel
import psycopg2
import os
import jwt



DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

def hash_password(password):
    h = hashlib.new('sha256')
    h.update(password.encode())
    return h.hexdigest()

def create_jwt_token(data):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now() + timedelta(minutes=60)})
    to_encode.update({"iat": datetime.now()})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

app = FastAPI()

@app.get("/")
def read_root():
    return {"Info": "auth service"}

security = HTTPBasic()


@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    password = hash_password(password)

    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        user = cursor.fetchone()

        cursor.close()
        conn.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to login")
    
    # successful login 200 else 401
    if user:
        token = create_jwt_token({"username": username})
        return {"message": "Login successful", "token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

class CreateUser(BaseModel):
    username: str
    password: str
    email: str
    name: str

@app.post("/createUser")
def create_user(data: CreateUser):

    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = conn.cursor()

        passwordHash = hash_password(data.password)

        cursor.execute(f"INSERT INTO users (username, password, email, name) VALUES ('{data.username}', '{passwordHash}', '{data.email}', '{data.name}')")
        conn.commit()

        cursor.close()
        conn.close()

        token = create_jwt_token({"username": data.username})
        return {"message": "User created successfully", "token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create user")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.post("/validate")
def validate(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {"message": "Token is valid", "payload": payload}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    
