FROM ubuntu:16.04

RUN apt-get update -y \
    && apt-get install -y \
    gunicorn \
    python-dev \
    python-pip
RUN pip install --upgrade pip


COPY . /flask-app

WORKDIR /flask-app


RUN pip install -r requirements.txt

CMD ["gunicorn", "-b 0.0.0.0:5000", "src.wsgi:app"]

EXPOSE 5000
