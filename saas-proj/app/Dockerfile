FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci 
COPY src/ ./src/

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/package*.json ./surface
RUN npm ci --only=production
COPY --from=builder /app/src ./src

USER node

EXPOSE 3000
CMD ["npm", "start"]
