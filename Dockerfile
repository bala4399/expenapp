FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
COPY .env .
RUN pip install -r requirements.txt

COPY . .
RUN apt update -y && apt install aws
CMD ["python", "app.py"]