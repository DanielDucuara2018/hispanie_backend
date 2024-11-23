FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN --mount=type=cache,target=/root/.cache pip install --editable .

RUN apt update -y && apt install supervisor -y
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENTRYPOINT ["/usr/bin/supervisord"]
