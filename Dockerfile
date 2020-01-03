FROM python:3.7

WORKDIR /usr/local/serverless-api

ENV FLASK_APP serverless_api
ENV FLASK_DEBUG 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libev-dev libevdev2

RUN pip install -U pip

COPY . .

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0"]