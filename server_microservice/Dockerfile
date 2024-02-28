FROM python:3.12

WORKDIR /server_microservice


COPY requirements.txt /server_microservice/
RUN pip install --upgrade pip; pip install  -r /server_microservice/requirements.txt

COPY . .
