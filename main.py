import subprocess
import pyautogui
import time
from pynput.keyboard import KeyCode, Key, Listener
from threading import Thread
import os
import pyperclip

def getPw():
    with open(os.path.expanduser("~/sex/pw")) as f:
        lines = f.readlines()
        return lines[0]

def getTf():
    with open(os.path.expanduser("~/sex/tf")) as f:
        lines = f.readlines()
        return lines[0]

class AutoP:

    COMM_R = False
    OPTN_R = False
    CMD = False
    pw = ""
    tf = ""

    def __init__(self):
        pyautogui.hotkey('command')
        self.pw = getPw()
        self.tf = getTf()

    def bloatShell(self):
        return subprocess.check_output([f"oathtool -b --totp {self.tf}"], shell=True).decode('utf-8').strip()

    def pressed(self, key):
        if key == Key.cmd_r: self.COMM_R = True
        if key == Key.alt_r: self.OPTN_R = True
        if key == Key.cmd: self.CMD = True

    def released(self, key):
        if self.COMM_R and self.CMD:
            print("Executing pw")
            pyperclip.copy(self.pw)
            time.sleep(.1)
            pyautogui.hotkey('command', 'v')
            self.COMM_R = False
            self.CMD = False
        if self.OPTN_R and self.CMD:
            print("Executing tf")
            time.sleep(.1)
            pyperclip.copy(self.bloatShell())
            pyautogui.hotkey('command', 'v')
            self.OPTN_R = False
            self.CMD = False
        if key == Key.cmd_r: self.COMM_R = False
        if key == Key.alt_r: self.OPTN_R = False
        if key == Key.cmd: self.CMD = False


autoP = AutoP()

keyboard_listener = Listener(on_press=autoP.pressed, on_release=autoP.released)

keyboard_listener.start()
keyboard_listener.join()
