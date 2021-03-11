FROM python:3.7-slim

COPY telegram_bot_bot/ /app

WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["telegram_bot.py"]




