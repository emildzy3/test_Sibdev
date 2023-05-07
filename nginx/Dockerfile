FROM python:3.10.6-slim AS server

WORKDIR /server

COPY ./server/pyproject.toml /server/
COPY ./server/poetry.lock /server/

RUN pip install --use-pep517 psycopg2-binary && pip install poetry && poetry config virtualenvs.create false && pip install poetry && poetry install --no-dev


COPY ./server /server

RUN python ./manage.py collectstatic --noinput

#########################################

FROM nginx:1.19.2

RUN rm -v /etc/nginx/nginx.conf
ADD ./nginx/nginx.conf /etc/nginx/

RUN mkdir /nginx
COPY --from=server /server/staticfiles /nginx/static
