# News Aggregator Project Summary

## Project Aim

The aim of this project is to create a sophisticated news aggregator platform that collects news from various sources, personalizes content for users, and provides an interactive news consumption experience. The platform will use a microservices architecture for scalability and flexibility.

## How to Run

Since the all of the technologies used in this project are containerized, you can run the project using Docker Compose to run Locally. To run the project, follow these steps:

```bash
docker-compose up -d
```

```

```

## Service Breakdown

1. **API Gateway**
   - Acts as the single entry point for all client requests
   - Routes requests to appropriate microservices
   - Performs Authentication using JWT tokens
     Tech Stack: FastAPI, JWT, Python, Docker
2. **Authentication Service**
   - Manages user authentication and authorization
   - Generates and validates JWT tokens for secure access
     Tech Stack: FastAPI, JWT, Python, Docker
3. **User Service**
   - Handles user account management
   - Stores and retrieves user profiles and preferences
     Tech Stack: FastAPI, MongoDB, Postgress, Python, Docker, Grpc
4. **News Collection Service**
   - Automatically collects news articles from various sources
   - Categorizes and stores articles in the database
   - Uses Airflow for scheduling collection jobs.
     Tech Stack: TypeScript, Node.js, Airflow, Docker, RabbitMQ
5. **Frontend Service** -
   - Delivers a fast, responsive user interface
   - Implements server-side rendering for improved performance and SEO
     Tech Stack: Next.js, React, TypeScript, Tailwind CSS, Docker, Shadcn
6. Postgres Database
   - Stores user data, news articles, and other application data
     Tech Stack: Postgres, Docker
7. Vector Search Service
   - Provides AI-powered search capabilities for news articles
   - Uses embeddings to find similar articles
     Tech Stack: Chroma DB, Ollama, Docker
8. Airflow Service
   - The service that schedules and orchestrates news collection jobs
   - Automatically triggers news collection tasks.
     Tech Stack: Airflow, Docker, RabbitMQ
9. RabbitMQ
   - Message broker for cretating queues for performing asynchronous tasks.
   - It mostly manages the communication between the services for news collection.
     Tech Stack: RabbitMQ, Docker
10. Consumer Service
    - The service uses Golang to consume messages from RabbitMQ and process them.
    - It processes the news articles and stores them in the relational Db and a Vector Database.
      Tech Stack: Golang, Docker, RabbitMQ, Postgres, Chroma DB
11. Chat Service
    - Provides AI-powered conversations about news articles using RAG.
    - Manages the LLM model for generating responses.
    - Uses open-source models like Ollama and IBM's Granite
      Tech Stack: Grpc,Ollama, Langchain, Chroma db, LLM
