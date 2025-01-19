FROM node:23-alpine

WORKDIR /code

COPY ./tsCollectionServer/ .

RUN npm install

EXPOSE 3001

CMD ["npm", "start"]
