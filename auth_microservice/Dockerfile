FROM python:3.12

WORKDIR /auth_microservice


COPY requirements.txt /auth_microservice/
RUN pip install --upgrade pip; pip install  -r /auth_microservice/requirements.txt

COPY . .
