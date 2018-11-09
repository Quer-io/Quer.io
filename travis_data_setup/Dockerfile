FROM frolvlad/alpine-python-machinelearning:latest
ADD . /code
WORKDIR /code
COPY . .


RUN apk add --no-cache bash

RUN pip install --upgrade pip && \
 apk update && \
 apk add postgresql-libs && \
 apk add python3-dev && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt

ENTRYPOINT ["python", "travis_init_database.py", "10000000", "travis_rows.csv"]  
