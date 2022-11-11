import json
import os
from typing import TypedDict, cast

CONFIG_FILE = '~/.config/nintendo-store.json'


class NintendoStoreConfigData(TypedDict):
    token: str


class NintendoStoreConfig:
    def __init__(self, path: str = CONFIG_FILE):
        self.path = os.path.expanduser(path)

    def exists(self):
        return os.path.isfile(self.path)

    def read(self) -> NintendoStoreConfigData:
        with open(self.path, "r") as f:
            return json.load(f)

    def write(self, data: NintendoStoreConfigData):
        with open(self.path, "w") as f:
            return json.dump(data, f)

    def update(self, new_data: NintendoStoreConfigData):
        if self.exists():
            data = self.read()
        else:
            data = {}
        data.update(cast(dict, new_data))
        self.write(data)
