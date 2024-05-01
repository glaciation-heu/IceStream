FROM rust:alpine

RUN apk add build-base

WORKDIR /usr/src/coordination_service

COPY . .

RUN cargo install --path .

CMD ["coordination_service"]
