# web/Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY web/package*.json ./
RUN npm install
COPY web/ .
RUN npm run build
EXPOSE 3000
CMD ["npx", "serve", "-s", "build"]