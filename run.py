import requests
import time
import paho.mqtt.client as paho
import getpass
import sys
import clipboard
import getpass
import tkinter as tk




def getClipboardText():
    root = tk.Tk()
    # keep the window from showing
    root.withdraw()
    return root.clipboard_get()


class SYS:
    username = getpass.getuser()
    broker = "broker.hivemq.com"
    curClipboard = ''
    prevClipboard = ''
    running = False
    topic = ''


def on_message(client, userdata, message):
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    SYS.curClipboard = msg
    SYS.prevClipboard = msg
    print("NEW CLIPBOARD TEXT RECEIVED")


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


SYS.running = True

SYS.curClipboard = getClipboardText()
SYS.prevClipboard = getClipboardText()

while SYS.running:
    try:
        SYS.curClipboard = getClipboardText()
        if not SYS.curClipboard == SYS.prevClipboard:
            SYS.prevClipboard = SYS.curClipboard
            client.publish(SYS.topic, SYS.curClipboard)
    except Exception as e:
        print(f"UNABLE TO GET CLIPBOARD: {e}")
    time.sleep(0.5)


client.disconnect() #disconnect
client.loop_stop() #stop loop





