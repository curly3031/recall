FROM python:3.9-alpine
RUN apk add vim
COPY . .
RUN pip install -r requirements.txt