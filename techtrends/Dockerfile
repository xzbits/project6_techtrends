FROM python:3.8.14-slim

WORKDIR /app
EXPOSE 3111
COPY templates /app

RUN pip install -r requirements.txt
RUN cd techtrends
RUN python init_db.py

CMD ["python", "app.py"]
