# pc-mini

A small clone of [Planetary Computer](planetarycomputer.microsoft.com/) [STAC](https://stacspec.org) [collections](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md) and [items](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md), loaded into a [pgstac](https://github.com/stac-utils/pgstac) database, served with [stac-fastapi](https://github.com/stac-utils/stac-fastapi).

## Usage

Build then start the servers with [docker-compose](https://docs.docker.com/compose/):

```shell
docker-compose build
docker-compose up
```

The STAC server will be available on <http://localhost:7822>.
A [stac-browser](https://github.com/radiantearth/stac-browser) will be available on <http://localhost:7823>.
If you want to connect to the database directly, it is on <http://localhost:7824>.

## Updating the STAC collections and items

Install the necessary requirements:

```shell
pip install -r requirements.txt
```

Then use the provided script:

```shell
./update.py
```

This will update the files in the [data](./data) directory.

## Contributing

Install the dev requirements:

```shell
pip install -r requirements-dev.txt
```

Then, install the [pre-commit](https://pre-commit.com/) hooks:

```shell
pre-commit install
```
