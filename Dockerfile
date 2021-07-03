FROM python:3.7
RUN apt-get update && apt-get -y install \
    libpq-dev

WORKDIR /app
ADD ./requirements.txt /app/
RUN chmod -R 700 scripts/
RUN pip install -r requirements.txt
EXPOSE 3052