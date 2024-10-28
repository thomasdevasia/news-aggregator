from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import psycopg2
import os

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
AUTH_SERVICE_URL = "http://auth-service:8001"

def get_user_info(username):
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, username, name, email FROM users WHERE username = '{username}'")
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(e)
        return None

def update_news_selection(user_id, news_selection):
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = conn.cursor()
        # check if news_topic table already has the news_selection
        cursor.execute(f"SELECT * FROM news_topic WHERE user_id = {user_id}")
        if cursor.fetchone():
            cursor.execute(f"UPDATE news_topic SET topics = %s WHERE user_id = %s", (news_selection, user_id))
        else:
            cursor.execute("INSERT INTO news_topic (user_id, topics) VALUES (%s, %s)", (user_id, news_selection))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False

app = FastAPI()

@app.middleware("http")
async def auth_middleware(request, call_next):

    # print("auth middleware")
    header_authorization = request.headers.get("Authorization")

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/validate", headers={"Authorization": header_authorization})

    if response.status_code == 200:
        payload = response.json()['payload']
        # print(payload)
        request.state.username = payload["username"]
        response = await call_next(request)
        return response
    else:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

@app.get("/")
def read_root(request: Request):

    user_info = get_user_info(request.state.username)
    
    response = {"Info": "user service", **dict(zip(["id","username", "name", "email"], user_info))}

    return response

@app.get("/news")
def get_news(request: Request):
    user_info = get_user_info(request.state.username)
    if not user_info:
        return {"message": "User not found"}
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT topics FROM news_topic WHERE user_id = {user_info[0]}")
        news_selection = cursor.fetchone()
        print(news_selection)
        if news_selection:
            return {"topics": news_selection[0], "username": user_info[1]}
        else:
            return {"message": "No news selection found"}
    except Exception as e:
        print(e)
        return {"message": "Error fetching news selection"}

@app.post("/news")
async def news_action(request: Request):
    
    body = await request.json()
    user_info = get_user_info(request.state.username)

    if body["action"] == "update":
        res =  update_news_selection(user_info[0], body["topics"])
        if res:
            return {"message": "News selection updated successfully"}
        else:
            return {"message": "News selection update failed"}

    response = {"Info": "user service", "action": "news"}


