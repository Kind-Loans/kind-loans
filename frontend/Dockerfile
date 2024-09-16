FROM node:alpine

WORKDIR /app
COPY . .

RUN npm install

ARG DEV
RUN if [ $ENV = "false" ]; \
    then npm run build; \
    else npm run dev; \
    fi
