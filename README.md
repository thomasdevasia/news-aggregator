# News Aggregator Project Summary

## Project Aim

The aim of this project is to create a sophisticated news aggregator platform that collects news from various sources, personalizes content for users, and provides an interactive news consumption experience. The platform will use a microservices architecture for scalability and flexibility.

## Key Features

- User account management
- Automated news collection
- Personalized news recommendations
- AI-powered conversations about news articles
- Real-time notifications
- Analytics for user behavior
- Fast, responsive front-end experience
- Powerful full-text search capabilities

## Service Breakdown

1. **API Gateway**
   - Acts as the single entry point for all client requests
   - Routes requests to appropriate microservices
   - built with fastapi
2. **Authentication Service**
   - Manages user authentication and authorization
   - Generates and validates JWT tokens for secure access
   - Built using fastapi
3. **User Service**
   - Handles user account management
   - Stores and retrieves user profiles and preferences
   - Built using fastapi
4. **News Collection Service**
   - Automatically collects news articles from various sources
   - Categorizes and stores articles in the database
   - Uses Airflow for scheduling collection jobs.
   - The service is built using TypeScript and
5. **Frontend Service** - Delivers a fast, responsive user interface - Implements server-side rendering for improved performance and SEO - Built using Next.js, Shacn and TypeScript
   **Services under development**
6. **Recommendation Service**
   - Generates personalized news recommendations for users
   - Utilizes user preferences and behavior data for accurate suggestions
7. **RAG (Retrieval Augmented Generation) Service**
   - Enables AI-powered conversations about news articles using Langchain
   - Allows users to ask questions and get insights about news content
8. **Notification Service**
   - Sends real-time notifications to users
   - Alerts users about new articles, recommendations, and account activities
9. **Analytics Service**
   - Tracks and analyzes user behavior
   - Provides insights for improving user experience and content curation
10. **Search Service**
    - Provides powerful full-text search capabilities across news articles
    - Enables advanced filtering and faceted search
