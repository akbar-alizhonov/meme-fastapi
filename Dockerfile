FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

WORKDIR src

CMD ["fastapi", "run", "meme/main.py", "--port", "8000"]