FROM python:3.7
COPY requirements.txt .
RUN pip install --default-timeout=100 -r requirements.txt
COPY . .
EXPOSE 3052