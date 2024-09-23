FROM --platform=linux/amd64 python:3.11.8-slim-bullseye as python3

FROM python3 as python-build-stage

ARG APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR ${APP_HOME}

RUN pip install --upgrade pip
RUN pip install poetry
COPY poetry.toml pyproject.toml ./
RUN poetry install

COPY manage.py gunicorn.conf.py ./
COPY config ./config
COPY common ./common
COPY transactions ./transactions
COPY users ./users

FROM python3 as python-run-stage

ARG APP_HOME=/app
ARG USER=django

WORKDIR ${APP_HOME}

# For Mac Specific Error
# RUN echo "Acquire::http::Pipeline-Depth 0;" > /etc/apt/apt.conf.d/99custom && \
#     echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99custom && \
#     echo "Acquire::BrokenProxy    true;" >> /etc/apt/apt.conf.d/99custom

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    tesseract-ocr \
    gettext && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --system ${USER} && \
    adduser --system --ingroup ${USER} ${USER}

COPY --chown=${USER}:${USER} ./docker/start /start

RUN sed -i 's/\r$//g' /start && \
    chmod +x /start && \
    chown ${USER}:${USER} ${APP_HOME}

USER ${USER}

COPY --from=python-build-stage /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=python-build-stage --chown=${USER}:${USER} ${APP_HOME} ${APP_HOME}

ENV PATH="/${APP_HOME}/.venv/bin:$PATH"

ENTRYPOINT ["/bin/bash"]
