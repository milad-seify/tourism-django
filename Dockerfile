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
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev zlib zlib-dev \
    geos proj gdal binutils proj-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.developer.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser -D -H  tourism-user && \
    mkdir -p /vol/web/media/ && \
    mkdir -p /vol/web/static && \
    chown -R tourism-user:tourism-user /vol && \
    chmod -R 755 /vol


ENV PATH="/py/bin:$PATH"

USER tourism-user
