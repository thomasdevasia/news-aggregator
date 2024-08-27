ARG NODE_VERSION=21.7.3

FROM node:${NODE_VERSION}-alpine

ENV NODE_ENV development

WORKDIR /code

COPY ./web-app/package*.json ./
RUN npm install

# Run the application as a non-root user.
# USER node

# Copy the rest of the source files into the image.
COPY ./web-app/ .

# Expose the port that the application listens on.
EXPOSE 3000

CMD npm run dev
