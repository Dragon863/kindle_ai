import asyncio
import importlib
import os

from core.conf_handler import CentralConfig
from core.event_log import EventLog


class PluginLibrary:
    pass


async def load_and_run_plugin(plugin_name, config, eventLog):
    try:
        loadedPlugin = importlib.import_module(f"plugins.{plugin_name}")
        await loadedPlugin.main(config.plugins[plugin_name], eventLog)
    except KeyError:
        print(f"Plugin {plugin_name} is not configured, skipping.")
    except Exception as e:
        print(f"Error loading plugin {plugin_name}: {e}")


async def runPlugins(config: CentralConfig, eventLog: EventLog):
    plugins = PluginLibrary()
    tasks = []
    for file in os.listdir("plugins"):
        if file.endswith(".py"):
            pluginName = file[:-3]
            tasks.append(load_and_run_plugin(pluginName, config, eventLog))

    await asyncio.gather(*tasks)
    return plugins

def importAllPlugins(config: CentralConfig, eventLog: EventLog):
    asyncio.run(runPlugins(config, eventLog))
