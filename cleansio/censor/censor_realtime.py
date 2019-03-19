""" Censors audio chunks in a continuous stream """

from colorama import Fore
import platform
from .censor_realtime_mac import CensorRealtimeMac
from utils import create_env_var

class CensorRealtime():
    """ Filters audio stream in real-time """
    def __init__(self, args, explicits):
        super().__init__()
        self.explicits = explicits
        self.args = args
        create_env_var('CLEANSIO_REALTIME', 'true')

    def censor(self):
        system = platform.system()
        if system == 'Darwin':
            CensorRealtimeMac(self.args, self.explicits).censor()
        else:
            print(Fore.RED + 'Real-time does not support your OS' + Fore.RESET)
