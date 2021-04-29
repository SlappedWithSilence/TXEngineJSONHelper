# This file holds a series of classes that are used to aid the functionality of the many windows that can be
# created by main.py. Each class defined here will usually only serve a single window, but a window will only ever
# use a single class defined here.

# A class that manages all the items currently in the manifest
import JSONHelper


def make_item_skeleton():
    return {"type": None, "name": None, "description": None, "id": None, "value": None, "maxStacks": None,
            "effects": None}


def make_item(name: str, id: int, desc: str, item_class: str, effects: list, value: int, max_stacks: int):
    return {"type": item_class,
            "name": name,
            "description": desc,
            "id": id,
            "value": value,
            "maxStacks": max_stacks,
            "effects": effects
            }


def make_effect(class_name: str, properties: list):
    return {"class_name": class_name, "properties": properties}


class ItemWindowHelper:
    item_map = {}  # A dict that maps the id of an item to a sub-dict that stores the values associated with that ID
    item_class_names = ["item", "consumable", "usable", "wearable", "wieldable"]

    # Makes and returns a structure to hold all the critical information about an item.
    # A dict holds these values to make them easily queriable.

    # Makes a structure to hold all the critical values for effects: class name and a list of properties
    # A dict holds these values

    # Returns a list that only holds the classnames of each of the effects associated with the item with id == "key"
    def get_effects_as_strings(self, key: int):
        values = []
        try:
            for value in self.item_map[key]["effects"]:
                values.append(value["className"])
        except KeyError:
            return []

        return values

    def load_manifest(self, path: str):
        self.item_map = JSONHelper.read_items(path)

    def get_items_as_strings(self):
        values = []
        for item in self.item_map.values():
            combined_title = str(item['id']) + ': ' + item['name']
            values.append(combined_title)


        return values
