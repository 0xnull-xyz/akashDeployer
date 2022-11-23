# FROM m.docker-registry.ir/python:3.9.12
FROM python:3.9.12

COPY . /var/apps
WORKDIR /var/apps

RUN pip install -r requirements.txt
RUN cp .env.prod .env

EXPOSE 8000

CMD gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0 --enable-stdio-inheritance