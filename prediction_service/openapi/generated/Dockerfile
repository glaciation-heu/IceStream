FROM python:3.9.18-alpine3.19

RUN apk update && apk upgrade && apk add curl

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

CMD ["python", "-m", "openapi_server"]
