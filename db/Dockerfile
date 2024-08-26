FROM postgres:latest

WORKDIR /docker-entrypoint-initdb.d

# Set the environment variables
ENV POSTGRES_USER=postgres
# ENV POSTGRES_PASSWORD=postgres123
ENV POSTGRES_DB=news_app_db

# ADD  init.sql /docker-entrypoint-initdb.d/init.sql
COPY ./scripts/init.sql /docker-entrypoint-initdb.d/init.sql