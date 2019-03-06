# pylint: disable=W0201

""" Retrieves key input on macOS and Windows """

from os import environ
import time
from threading import Thread

# https://stackoverflow.com/a/31736883/9335095

global IS_WINDOWS

IS_WINDOWS = False
try:
    from win32api import STD_INPUT_HANDLE
    from win32console import GetStdHandle, KEY_EVENT, ENABLE_ECHO_INPUT, \
        ENABLE_LINE_INPUT, ENABLE_PROCESSED_INPUT
    IS_WINDOWS = True
except ImportError as error:
    import sys
    import select
    import termios

class KeyPoller():
    """ Retrieves key input on macOS and Windows """
    def __enter__(self):
        global IS_WINDOWS
        if IS_WINDOWS:
            self.read_handle = GetStdHandle(STD_INPUT_HANDLE)
            self.read_handle.SetConsoleMode(
                ENABLE_LINE_INPUT|ENABLE_ECHO_INPUT|ENABLE_PROCESSED_INPUT)

            self.cur_event_length = 0
            self.cur_keys_length = 0

            self.captured_chars = []
        else:
            # Save the terminal settings
            self.fileno = sys.stdin.fileno()
            self.new = termios.tcgetattr(self.fileno)
            self.old = termios.tcgetattr(self.fileno)

            # New terminal setting unbuffered
            self.new[3] = (self.new[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fileno, termios.TCSAFLUSH, self.new)

        return self

    def __exit__(self, _, value, traceback):
        if not IS_WINDOWS:
            termios.tcsetattr(self.fileno, termios.TCSAFLUSH, self.old)

    def poll(self):
        """ Returns the pressed key or Null """
        if IS_WINDOWS:
            if not len(self.captured_chars) == 0:
                return self.captured_chars.pop(0)

            events_peek = self.read_handle.PeekConsoleInput(10000)

            if len(events_peek) == 0:
                return None

            if not len(events_peek) == self.cur_event_length:
                for cur_event in events_peek[self.cur_event_length:]:
                    if cur_event.EventType == KEY_EVENT:
                        if ord(cur_event.Char) == 0 or not cur_event.KeyDown:
                            pass
                        else:
                            cur_char = str(cur_event.Char)
                            self.captured_chars.append(cur_char)
                self.cur_event_length = len(events_peek)

            if not len(self.captured_chars) == 0:
                return self.captured_chars.pop(0)
            else:
                return None
        else:
            inp, _, _ = select.select([sys.stdin], [], [], 0)
            if not inp == []:
                return sys.stdin.read(1)
            return None

def space_key():
    """ Listen for when a space key is pressed and update CLEANSIO_SPACE_KEY """
    with KeyPoller() as key_poller:
        while True:
            if key_poller.poll() == ' ':
                print("SPACE PRESSED")
                env_var = 'CLEANSIO_SPACE_KEY'
                if not env_var in environ or environ[env_var] == 'false':
                    environ[env_var] = 'true'
                else:
                    environ[env_var] = 'false'

Thread(target=space_key, args=[]).start()

while True:
    print("LOOP")
    time.sleep(2)
