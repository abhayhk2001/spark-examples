FROM python:3.10
WORKDIR /app

COPY app.py .
COPY py_minIO.py .
COPY requirements.txt .

RUN apt update
RUN apt upgrade -y
RUN apt install build-essential


RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "/app/app.py"]