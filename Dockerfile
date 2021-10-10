FROM python:3.9.7-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential nano procps && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uwsgi==2.0.20
ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /var/www/c3po

ADD src/ .

RUN ./manage.py collectstatic --noinput && \
    ./manage.py migrate

CMD ./manage.py migrate && \
    uwsgi --http :8000 --module app.wsgi --master --process 4 --threads 2 --harakiri 1200 --chdir /var/www/c3po
