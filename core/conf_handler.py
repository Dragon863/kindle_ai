import json
import os
from .exceptions import ConfigurationError
from core.logger import Logger

log = Logger()


class CentralConfig:
    def __init__(self):
        self.plugins = {}
        self.core = {}
        for file in os.listdir("config"):
            if file.endswith(".json") and file != "core.json":
                with open("config/" + file) as f:
                    data = json.load(f)
                    try:
                        pluginName = data["name"]
                        self.plugins[pluginName] = data
                    except KeyError:
                        raise ConfigurationError(
                            "Plugin name not found in config file: " + file
                        )
        with open("config/core.json") as f:
            data = json.load(f)
            self.core = data
