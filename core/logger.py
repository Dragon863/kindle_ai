from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()


class Logger:
    def __init__(self):
        self.level = 2
        pass

    def debug(self, msg):
        if self.level < 2:
            print(Fore.GREEN + "[D] " + Style.RESET_ALL + msg)

    def info(self, msg):
        if self.level < 3:
            print(Fore.BLUE + "[I] " + Style.RESET_ALL + msg)

    def warning(self, msg):
        if self.level < 4:
            print(Fore.YELLOW + "[W] " + Style.RESET_ALL + msg)

    def error(self, msg):
        if self.level < 5:
            print(Fore.RED + "[E] " + Style.RESET_ALL + msg)
