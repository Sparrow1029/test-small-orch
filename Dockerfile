FROM python:3.12-slim AS builder

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry==1.8.2 \
  && poetry export --output=requirements.txt


FROM builder AS dev
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=www-data:www-data . /usr/src/app
COPY --chown=www-data:www-data --chmod=755 ./bin/server ./bin/server

EXPOSE 8080
USER www-data:www-data

CMD ["/usr/src/app/bin/server"]
