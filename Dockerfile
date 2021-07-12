FROM python:3.7
RUN apt-get update && apt-get -y install \
    libpq-dev

WORKDIR /app
ADD ./requirements.txt /app/
ADD scripts /app/scripts
RUN chmod +x scripts/*

RUN pip install -r requirements.txt
EXPOSE 3052