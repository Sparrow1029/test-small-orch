FROM python:3.12-slim

WORKDIR /usr/src/app

COPY --chown=www-data:www-data . /usr/src/app
COPY --chown=www-data:www-data --chmod=755 ./bin/server ./bin/server

RUN pip install --no-cache-dir "orchestrator-core==2.7.2"

EXPOSE 8080
USER www-data:www-data

CMD ["/usr/src/app/bin/server"]
