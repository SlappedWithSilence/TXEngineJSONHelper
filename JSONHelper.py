import json
import os.path as osp
import WindowHelper
import requests

def JSON_from_url(url: str):
    r = requests.get(url)
    return r.json()

def read_items(path: str):
    file = open(path)

    if not osp.isfile(path):
        return

    json_raw = json.load(file)

    items_raw = json_raw['items']

    item_map = {}
    for item in items_raw:
        i = WindowHelper.make_item_skeleton()
        for key in i.keys():
            if key == "effects" and item['type'] == 'item':
                i[key] = []
            else:
                i[key] = item[key]
        item_map[item['id']] = i

    return item_map
