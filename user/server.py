from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
# import httpx
import psycopg2
import os
import pika
from datetime import datetime

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
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
        cursor.execute(
            f"SELECT id, username, name, email FROM users WHERE username = '{username}'")
        user = cursor.fetchone()
        conn.close()
        return user
    except Exception as e:
        print(e)
        return None


def get_user_info_by_id(user_id):
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, username, name, email FROM users WHERE id = {user_id}')
        user = cursor.fetchone()
        conn.close()
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
            cursor.execute(
                "UPDATE news_topic SET topics = %s WHERE user_id = %s", (news_selection, user_id))
        else:
            cursor.execute(
                "INSERT INTO news_topic (user_id, topics) VALUES (%s, %s)", (user_id, news_selection))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_all_userid() -> list[str]:
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    except Exception as e:
        print(e)
        return None


def get_all_user_name() -> list[str]:
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    except Exception as e:
        print(e)
        return None


def get_news_topic(user_id: str) -> list[str]:
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT topics from news_topic where user_id = %s", (user_id,))
        topics = cursor.fetchone()
        conn.close()
        if topics:
            return topics[0]
        else:
            return ([])
    except Exception as e:
        print(e)
        return None


class NewsItem(BaseModel):
    source: str
    heading: str
    datetime: str
    newsType: str
    data: str


def save_news_db(user_id: str, news: list[NewsItem]):
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO news_collection (user_id, source, heading, date_created, news_type, data) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, news['source'], news['heading'], datetime.now(), news['newsType'], news['data'])
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True


def get_all_news_db(user_id: str):
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * from news_collection where user_id=%s", (user_id,))
        news = cursor.fetchall()
        conn.close()
        return news
    except Exception as e:
        print(e)
        return None


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

# @app.middleware("http")
# async def auth_middleware(request, call_next):
#
#     # print("auth middleware")
#     header_authorization = request.headers.get("Authorization")
#
#     async with httpx.AsyncClient() as client:
#         response = await client.post(f"{AUTH_SERVICE_URL}/validate", headers={"Authorization": header_authorization})
#
#     if response.status_code == 200:
#         payload = response.json()['payload']
#         # print(payload)
#         request.state.username = payload["username"]
#         response = await call_next(request)
#         return response
#     else:
#         return JSONResponse(status_code=401, content={"message": "Unauthorized"})
#


@app.get("/")
def read_root(request: Request):

    # user_info = get_user_info(request.state.username)

    # response = {"Info": "user service", ** dict(zip(["id", "username", "name", "email"], user_info))}
    response = {"Info": "user service running"}

    return response


# user info and details
@app.get("/{user_name}/")
def get_user(request: Request, user_name: str):
    print(user_name)
    user_info = get_user_info(user_name)
    if not user_info:
        return {"message": "User not found"}
    response = {"Info": "user service", ** dict(zip(["id", "username", "name", "email"], user_info))}
    return JSONResponse(content=response, status_code=200)


# return user selected news topics
@app.get("/{user_name}/news_topic")
def get_news(request: Request, user_name: str):
    user_info = get_user_info(user_name)
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
        cursor.execute(
            f"SELECT topics FROM news_topic WHERE user_id = {user_info[0]}")
        news_selection = cursor.fetchone()
        print(news_selection)
        if news_selection:
            return {"topics": news_selection[0], "username": user_info[1]}
        else:
            return {"message": "No news selection found", "topics": [], "username": user_info[1]}
    except Exception as e:
        print(e)
        return {"message": "Error fetching news selection"}


# updating user news selection
@app.post("/{user_name}/news_topic")
async def news_action(request: Request, user_name: str):

    body = await request.json()
    user_info = get_user_info(user_name)

    if body["action"] == "update":
        res = update_news_selection(user_info[0], body["topics"])
        if res:
            return {"message": "News selection updated successfully"}
        else:
            return {"message": "News selection update failed"}


# runs news collection for all users
@app.get("/get_latest_news")
async def get_latest_news():
    users = get_all_userid()
    for user in users:
        news_topic = get_news_topic(user[0])
        user_name = get_user_info_by_id(user[0])[1]
        payload = json.dumps({"userName": user_name, "topics": news_topic})
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='rabbitmq',
                credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            ))
            channel = connection.channel()
            channel.queue_declare(queue='user.newsCollection', durable=True, auto_delete=True)
            channel.basic_publish(exchange='', routing_key='user.newsCollection', body=payload)
            connection.close()
        except Exception:
            response = {"message": "Error connecting to RabbitMQ"}
            return JSONResponse(content=response, status_code=500)
    response = {"message": "News collection successful queued"}
    return JSONResponse(content=response, status_code=200)


# save user news
@app.post("/{user_name}/news")
async def save_news(request: Request, user_name: str):
    body = await request.json()
    user_info = get_user_info(user_name)
    if "action" not in body:
        response = {"message": "Action not provided"}
        return JSONResponse(content=response, status_code=400)
    if body["action"] == "save":
        res = save_news_db(user_info[0], body["news"])
        if res:
            response = {"message": "News saved successfully"}
        else:
            response = {"message": "News save failed"}
            return JSONResponse(content=response, status_code=500)
    else:
        response = {"message": "Invalid action"}
        return JSONResponse(content=response, status_code=400)
    return JSONResponse(content=response, status_code=200)


# get all news for user
@app.get("/{user_name}/news")
async def get_all_news(user_name: str):
    user_info = get_user_info(user_name)
    all_news = get_all_news_db(user_info[0])
    response = {
        "allNews": []
    }
    for news in all_news:
        response['allNews'].append(
            {
                "news_id": news[0],
                "heading": news[1],
                "data": news[2],
                "newsType": news[3],
                "source": news[4],
                "dateCreated": str(news[5])
            }
        )
    return JSONResponse(content=response, status_code=200)


# chat websocket with ai
@app.websocket("/{user_name}/chat")
async def chat_websocket_endpoint(websocket: WebSocket, user_name: str):
    print(f'websocket running for {user_name}')
    await websocket.accept()
    try:
        while True:
            response = await websocket.receive_text()
            data = json.loads(response)
            print(data)
            response = {"message": "Message received", "data": 'acknowledged'}
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        # await websocket.close()
        print(f'websocket closed for {user_name}')
