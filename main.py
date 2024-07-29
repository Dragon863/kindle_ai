from core.conf_handler import CentralConfig
from core.event_log import EventLog
from core.plugin_loader import importAllPlugins


class Central:
    def __init__(self):
        self.config = CentralConfig()
        self.plugins = []
        self.eventLog = EventLog(self.config.core)
        self.load()

    def load(self):
        self.plugins = importAllPlugins(self.config, self.eventLog)


central = Central()
