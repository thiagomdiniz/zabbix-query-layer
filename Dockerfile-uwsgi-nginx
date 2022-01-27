FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8
#FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
