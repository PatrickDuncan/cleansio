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
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        return self

    def __exit__(self, type, value, traceback):
        if IS_WINDOWS:
            pass
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def poll(self):
        if IS_WINDOWS:
            if not len(self.captured_chars) == 0:
                return self.captured_chars.pop(0)

            events_peek = self.read_handle.PeekConsoleInput(10000)

            if len(events_peek) == 0:
                return None

            if not len(events_peek) == self.cur_event_length:
                for curEvent in events_peek[self.cur_event_length:]:
                    if curEvent.EventType == KEY_EVENT:
                        if ord(curEvent.Char) == 0 or not curEvent.KeyDown:
                            pass
                        else:
                            curChar = str(curEvent.Char)
                            self.captured_chars.append(curChar)
                self.cur_event_length = len(events_peek)

            if not len(self.captured_chars) == 0:
                return self.captured_chars.pop(0)
            else:
                return None
        else:
            dr, dw, de = select.select([sys.stdin], [], [], 0)
            if not dr == []:
                return sys.stdin.read(1)
            return None

def key():
    with KeyPoller() as key_poller:
        while True:
            c = key_poller.poll()
            if c == ' ':
                print("SPACE PRESSED")

Thread(target=key, args=[]).start()

while True:
    print("LOOP")
    time.sleep(2)
