FROM node:22.7-slim

WORKDIR /app

COPY package.json tsconfig.json /app/

RUN npm install -y

CMD ["npm", "run", "dev"]

