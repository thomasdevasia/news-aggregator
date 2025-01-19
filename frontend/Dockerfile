FROM node:23-alpine

WORKDIR /code

COPY ./web-app/package*.json ./
# Copy the rest of the source files into the image.
COPY ./web-app/ .

# RUN npm install
# # prisma setup pull and migrate
# RUN npx prisma db pull
# RUN npx prisma generate
RUN npm install \
  npx prisma db pull \
  npx prisma generate

# Run the application as a non-root user.
# USER node



# Expose the port that the application listens on.
EXPOSE 3000

CMD npm run dev
