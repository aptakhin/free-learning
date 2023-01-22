FROM node:18-alpine3.16

ARG NODE_ENV="production"
ENV NODE_ENV=${NODE_ENV}

WORKDIR /app

EXPOSE 3000

# This docker file will copy code from app directory
# including the node_modules and .next folder.
COPY . .

# This run the server at default port 3000
CMD ["npm", "run", "start"]
