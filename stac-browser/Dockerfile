FROM node:19-buster-slim as base
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y build-essential git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

FROM base as builder
ARG CATALOG_URL
ARG STAC_BROWSER_TAG
ENV NODE_OPTIONS=--openssl-legacy-provider=value
WORKDIR /code
RUN git clone https://github.com/radiantearth/stac-browser --depth=1 --branch ${STAC_BROWSER_TAG}
WORKDIR /code/stac-browser
RUN npm install && npm run build -- --catalogUrl=${CATALOG_URL}

FROM builder as server
ARG STAC_BROWSER_PORT
WORKDIR /root
RUN npm install -g http-server
COPY --from=builder /code/stac-browser/dist ./dist
ENV STAC_BROWSER_PORT=${STAC_BROWSER_PORT}
CMD http-server dist -p $STAC_BROWSER_PORT
