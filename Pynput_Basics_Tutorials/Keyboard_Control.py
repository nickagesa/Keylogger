'''Keyboard control:
# This script demonstrates how to control the keyboard using the `pynput` library in Python.
# Use case: Automating tasks, red team operations (e.g., simulating keystrokes in phishing payloads).
# Install the library: pip install pynput or py -m pip install pynput 

##❌IMPORTANT❌: THIS SCRIPT IS FOR EDUCATIONAL PURPOSES ONLY. USE RESPONSIBLY AND ETHICALLY ##
'''
from pynput.keyboard import Controller, Key

keyboard = Controller() # creating an instance of the keyboard controller

# Type a string
keyboard.type("Hello, World!")

#'''
# Press and release special keys
keyboard.press(Key.enter)
keyboard.release(Key.enter)
#'''

#'''
# Press 'Ctrl + C' (simulate copy)
with keyboard.pressed(Key.ctrl):
    keyboard.press('c')
    keyboard.release('c')
#'''