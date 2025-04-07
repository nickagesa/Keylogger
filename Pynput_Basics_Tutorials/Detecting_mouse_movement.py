'''Detecting mouse movements:
# This script uses the `pynput` library to detect mouse movements, clicks, and scrolls.
# Use case: Detecting unusual cursor movement in forensic investigations or monitoring unauthorized remote access.
# You can track user interactions to detect suspicious activity, such as automated bot behavior.
# Install the library: pip install pynput or py -m pip install pynput

## ❌IMPORTANT❌: THIS SCRIPT IS FOR EDUCATIONAL PURPOSES ONLY. USE RESPONSIBLY AND ETHICALLY ##
The script below would run indefinately \place it in a multi string comment and use the one below it (with class) to stop the listener gracefully.
'''
from pynput.mouse import Listener

def on_move(x, y): # Callback function for mouse movement
    print(f"Mouse moved to ({x}, {y})")

def on_click(x, y, button, pressed): # Callback function for mouse clicks
    action = "pressed" if pressed else "released" # Determine if the button was pressed or released
    print(f"Mouse {button} {action} at ({x}, {y})") # Print the button and coordinates of the click

def on_scroll(x, y, dx, dy): # Callback function for mouse scroll
    # dx and dy are the scroll distances in the x and y directions respectively
    print(f"Scrolled {dy} at ({x}, {y})") # Print the scroll distance and coordinates

 
with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener_variable: 
    listener_variable.join() # Keep the listener running until interrupted (e.g., Ctrl+C)
# This will print the mouse movements, clicks, and scrolls to the console.

# with is a context manager that automatically handles the setup and teardown of the listener.(e.g., starting and stopping the listener)
# LIstener is a class that listens for mouse events and calls the appropriate callback functions when an event occurs.
# on_move, on_click, and on_scroll are the callback functions that handle mouse movements, clicks, and scrolls respectively.
# as listener_variable is used to give a name to the listener instance, which can be used to refer to it later in the code.
# The listener will run in the background and call the appropriate callback functions when an event occurs.

'''The script above would run indefinitely, printing mouse events to the console.
we need to implement a way to stop the listener gracefully.
you can do this by using a keyboard listener to listen for a specific key press (e.g., the ESC key) to stop the mouse listener.'''
'''
# Implement esc key to stop the mouse listener
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key

class MouseMonitor:
    def __init__(self):
        self.mouse_listener = MouseListener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        self.keyboard_listener = KeyboardListener(on_press=self.on_key_press)

    def on_move(self, x, y):
        print(f"Mouse moved to ({x}, {y})")

    def on_click(self, x, y, button, pressed):
        action = "pressed" if pressed else "released"
        print(f"Mouse {button} {action} at ({x}, {y})")

    def on_scroll(self, x, y, dx, dy):
        print(f"Scrolled {dy} at ({x}, {y})")

    def on_key_press(self, key):
        if key == Key.esc:
            print("ESC pressed, exiting...")
            self.stop()

    def start(self):
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.mouse_listener.join()
        self.keyboard_listener.join()

    def stop(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

if __name__ == "__main__":
    monitor = MouseMonitor()
    monitor.start()
'''