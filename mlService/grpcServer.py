from concurrent import futures
import logging
import json
import grpc
import aiChat_pb2
import aiChat_pb2_grpc
import asyncio
import httpx
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

OLLAMA_URL = 'http://host.docker.internal:11434/api/'


def create_embedding(prompt):
    data = {
        # "model": "llama3.2:1b",
        "model": "granite-embedding:278m",
        "prompt": prompt
    }
    response = httpx.post(OLLAMA_URL + 'embeddings', json=data)
    if response.status_code == 200:
        return response.json()['embedding']
    else:
        return None


class CustomEmbeddingFunction(EmbeddingFunction):
    def __init__(self, embedding_function):
        self.embedding_function = embedding_function

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = [self.embedding_function(doc) for doc in input]
        return embeddings


async def save_to_vector_db(newsData):
    client = await chromadb.AsyncHttpClient(host='vectordb', port=8000)
    emf = CustomEmbeddingFunction(create_embedding)
    collection = await client.get_or_create_collection(newsData.userName, embedding_function=emf)
    # print(newsData.heading)
    # print(newsData.data)
    await collection.add(
        documents=[newsData.data],
        metadatas=[{
            "heading": newsData.heading,
            "date": newsData.newsDate,
        }],
        ids=[newsData.heading]
    )


async def vector_search(userName, prompt):
    client = await chromadb.AsyncHttpClient(host='vectordb', port=8000)
    emf = CustomEmbeddingFunction(create_embedding)
    collection = await client.get_collection(userName, embedding_function=emf)
    result = await collection.query(
        query_texts=[prompt],
        n_results=3
    )
    return result


async def chat_ollama(userName, prompt):
    searchResult = await vector_search(userName, prompt)
    if len(searchResult['ids'][0]) > 0:
        searchContext = ""
        for i in range(len(searchResult['ids'][0])):
            searchContext = searchContext + f"""
            News Heading: {searchResult['metadatas'][0][i]['heading']}
            Date of News: {searchResult['metadatas'][0][i]['date'].split('T')[0]}
            News Content: {searchResult['documents'][0][i]}
            -------------------------------------------------------------------------------------------
            """
    else:
        searchContext = "There is no news available for the user"
    template = f"""
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Use three sentences maximum and keep the answer as concise as possible.
        Always say "thanks for asking!" at the end of the answer. You are a news chatbot. Users cant see the context you are provided.
        Just answer about the information on the news and greetings. Each news is seperated by multiple '-'

        News from the users Database:
        {searchContext}

        Question: {prompt}
    """
    data = {
        "model": "llama3.2:1b",
        "prompt": template
    }
    # response = httpx.post(OLLAMA_URL + 'generate', json=data)
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", OLLAMA_URL + 'generate', json=data) as response:
            async for line in response.aiter_text():
                if line:
                    yield json.loads(line)


class AiChatService(aiChat_pb2_grpc.AiChatServicer):
    async def SaveToVectorDb(self, request, context):
        logging.info("SaveToVectorDb")
        # logging.info(request)
        # logging.info(request.data)
        # get_embedding(request.data)
        await save_to_vector_db(request)
        return aiChat_pb2.SaveToVectorDbResponse(status=True, response="SaveToVectorDb")

    async def Chat(self, request, context):
        logging.info("Chat")
        logging.info(request)
        async for response in chat_ollama(request.userName, request.prompt):
            # print(response)
            yield aiChat_pb2.ChatResponse(status=True, response=response['response'], done=response['done'])
        # logging.info(request.data)
        # get_embedding(request.data)
        # await chat(request)
        # return aiChat_pb2.ChatResponse(status=True, response="Chat")


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    aiChat_pb2_grpc.add_AiChatServicer_to_server(AiChatService(), server)
    server.add_insecure_port('[::]:50051')
    logging.info('Starting server. Listening on port 50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler('server.log'),
            logging.StreamHandler()
        ]
    )
    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)
    logging.info('server started')
    # print('server started')
    asyncio.run(serve())
