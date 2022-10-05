FROM python:3.8.14-slim

WORKDIR /app
EXPOSE 3111
COPY . /app

RUN pip install -r requirements.txt
RUN python ./techtrends/init_db.py

CMD ["python", "./techtrends/app.py"]
