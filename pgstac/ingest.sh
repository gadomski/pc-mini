#!/usr/bin/env sh

set -e

if [ -z "$1" ]; then
    data=/data
else
    data=$1
fi

if [ -z "$2" ]; then
    dsn="host=/var/run/postgresql"
else
    dsn=$2
fi

for directory in "$data"/*; do
    echo "Loading collections for $directory"
    pypgstac --dsn "$dsn" load collections "$directory"/collection.json
    echo "Loading items for $directory"
    pypgstac --dsn "$dsn" load items "$directory"/items.ndjson
done
