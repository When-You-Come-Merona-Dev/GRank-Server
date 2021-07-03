FROM python:3.7
RUN apt-get update && apt-get -y install \
    libpq-dev

WORKDIR /app
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt
EXPOSE 3052