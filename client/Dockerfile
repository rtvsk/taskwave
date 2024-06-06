FROM node:20-slim

WORKDIR /usr/src/app

COPY package*.json ./ 

RUN npm install

COPY . .

RUN npm run build

WORKDIR /usr/src/app/nodeServer

RUN npm install

WORKDIR /usr/src/app

EXPOSE 5173

CMD ["node", "nodeServer/nodeServer.js"]
