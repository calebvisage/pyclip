import requests
import time
import paho.mqtt.client as paho
import getpass
import sys
import clipboard
import getpass
import tkinter as tk
import pyperclip
import os



def setClipboardText(text):
    try:
        pyperclip.copy(text)
    except:
        print("You need to install 'xsel' and or 'xclip'")
        print("try 'sudo apt-get install xsel xclip'")
        sys.exit()


def getClipboardText():
    root = SYS.tkin
    # keep the window from showing
    root.withdraw()
    try:
        return root.clipboard_get()
    except:
        print("COUND NOT GET CLIPBOARD")
        pass
    root.destroy()


class SYS:
    username = getpass.getuser()
    broker = "broker.hivemq.com"
    curClipboard = ''
    prevClipboard = ''
    running = False
    topic = ''
    tkin = None
    changeClipboard = False
    newClipboardText = ''
    doCheck = False 


def on_message(client, userdata, message):
    SYS.doCheck = False
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    # SYS.newClipboardText = msg
    # SYS.changeClipboard = True
    SYS.prevClipboard = msg
    SYS.curClipboard = msg
    setClipboardText(msg)
    print(f"NEW CLIPBOARD TEXT RECEIVED: {msg}")
    SYS.doCheck = True


if len(sys.argv) < 2:
    print("You need to pass a username as a parameter")
    sys.exit()


topicEnd = sys.argv[1]
topic = f"xclipboard/shared/{topicEnd}"

SYS.topic = topic


client=paho.Client(SYS.username) 
client.on_message=on_message
client.connect(SYS.broker)
client.loop_start()
client.subscribe(topic)#subscribe


SYS.tkin = tk.Tk()



SYS.running = True

SYS.curClipboard = getClipboardText()
SYS.prevClipboard = getClipboardText()


while SYS.running:
    if SYS.doCheck:
        try:
            SYS.curClipboard = getClipboardText()
            if not SYS.curClipboard == SYS.prevClipboard:
                SYS.prevClipboard = SYS.curClipboard
                client.publish(SYS.topic, SYS.curClipboard)
        except Exception as e:
            print(f"UNABLE TO GET CLIPBOARD: {e}")
    time.sleep(0.1)


client.disconnect() #disconnect
client.loop_stop() #stop loop






