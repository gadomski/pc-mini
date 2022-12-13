#!/usr/bin/env python3

import concurrent.futures
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict

import orjson
from pystac import Collection, ItemCollection
from pystac_client import Client

URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
ROOT = Path(__file__).parent
DATA = ROOT / "data"
LIMIT = 10
MAX_ITEMS = 10
SORTBY = "-properties.datetime"
# TODO allow per-collection locations
BBOX = [-105.101, 40.167, -105.100, 40.168]  # Longmont, Colorado
MAX_WORKERS = 8


def get_items(collection: Collection) -> ItemCollection:
    client = Client.open(URL)
    item_search = client.search(
        method="POST",
        collections=[collection.id],
        limit=LIMIT,
        max_items=MAX_ITEMS,
        bbox=BBOX,
    )
    return item_search.item_collection()


def save_data(collection: Collection, item_collection: ItemCollection) -> None:
    collection_as_dict = collection.to_dict()
    collection_as_dict = clean_structural_links(collection_as_dict)
    collection_as_str = orjson.dumps(collection_as_dict, option=orjson.OPT_INDENT_2)

    item_collection_as_dict = item_collection.to_dict()
    cleaned_items = []
    for item in item_collection_as_dict.pop("features"):
        item = clean_structural_links(item)
        cleaned_items.append(item)
    item_collection_as_dict["features"] = cleaned_items
    item_collection_as_str = orjson.dumps(
        item_collection_as_dict, option=orjson.OPT_INDENT_2
    )

    directory = DATA / collection.id
    directory.mkdir()
    with open(directory / "collection.json", "wb") as f:
        f.write(collection_as_str)
    with open(directory / "item-collection.json", "wb") as f:
        f.write(item_collection_as_str)

    print(f"Saved {collection.id} to {DATA / collection.id}")


def clean_structural_links(d: Dict[str, Any]) -> Dict[str, Any]:
    links = d.pop("links")
    cleaned_links = []
    if links:
        for link in links:
            if link["rel"] not in (
                "self",
                "collection",
                "parent",
                "child",
                "root",
                "items",
            ):
                cleaned_links.append(link)
    d["links"] = cleaned_links
    return d


shutil.rmtree(DATA, ignore_errors=True)
DATA.mkdir()
client = Client.open(URL)
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {
        executor.submit(get_items, collection): collection
        for collection in client.get_collections()
    }
    for future in concurrent.futures.as_completed(futures):
        collection = futures[future]
        try:
            item_collection = future.result()
        except Exception as e:
            print(f"Getting items from {collection} produced an exception: {e}")
        else:
            if not item_collection.items:
                print(f"Skipping {collection.id}, no items found")
            else:
                save_data(collection, item_collection)
