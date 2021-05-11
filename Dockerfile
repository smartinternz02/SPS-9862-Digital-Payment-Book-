FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install -y python3-pip python3-dev build-essential libmysqlclient-dev

WORKDIR /app
ADD . /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt
CMD ["python3","josvin_app.py"]