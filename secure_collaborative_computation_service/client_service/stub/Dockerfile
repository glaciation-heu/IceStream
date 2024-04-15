FROM rust:latest

#RUN apk add build-base

WORKDIR /usr/src/client_service

COPY . .

RUN cargo install --path .

CMD ["client_service"]
