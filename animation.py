import itertools
import threading
import time
import sys

done = False

#here is the animation
def loading_text(text):
    for spin in itertools.cycle(['|', '/', '-', '\\']):
        if done: # Change to CLEANSIO_REALTIME
            print()
            break
        sys.stdout.write('\r{0} {1} '.format(text, spin))
        sys.stdout.flush()
        time.sleep(0.1)

t = threading.Thread(target=loading_text, args=['Capturning audio in real-time'])
t.start()

#long process here
time.sleep(10)
done = True
