FROM python:alpine3.18
LABEL maintainer="miladsey"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.developer.txt /tmp/requirements.developer.txt
COPY ./tourism /tourism
WORKDIR /tourism
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.developer.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser -D -H  tourism-user


ENV PATH="/py/bin:$PATH"

USER tourism-user
