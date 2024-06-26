FROM python:3.10

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python3", "stankin_get_news.py"]
