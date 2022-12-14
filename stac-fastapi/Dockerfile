FROM python:3.10-slim as base
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y build-essential git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

FROM base as builder
ARG STAC_FASTAPI_TAG
WORKDIR /code
RUN git clone https://github.com/stac-utils/stac-fastapi --depth 1 --branch ${STAC_FASTAPI_TAG}
RUN cd stac-fastapi && \
    pip install stac_fastapi/types && \
    pip install stac_fastapi/api && \
    pip install stac_fastapi/extensions && \
    pip install stac_fastapi/pgstac[server]
RUN rm -rf /code/stac-fastapi
