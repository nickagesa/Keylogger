# Keylogger
This Python-based keylogger captures and logs keystrokes to a file named keylog.txt within the temp_files directory. Once the log file exceeds a defined size threshold (default: 200 bytes, configurable in the code), it automatically encrypts the contents and sends the encrypted log, along with the decryption key, to the attacker's specified email address. After successful transmission, the script cleans up by deleting the log file and the directory from the victim's machine, leaving minimal traces of its activity.

<img src="https://github.com/user-attachments/assets/4a7a06d2-f727-422e-8043-c46c80c134dc" width="150" height="160" />

<img src="https://github.com/user-attachments/assets/abad1947-3aa2-4573-8d60-b0ab011657fd" width="150" height="160" />

<img src="https://github.com/user-attachments/assets/6978678c-fcc4-4014-87f1-b7446279e857" width="150" height="110" />

<img src="https://github.com/user-attachments/assets/ab16d5f0-2133-4685-893f-7503e2a39fe3" width="215" height="190" />

<img src="https://github.com/user-attachments/assets/2d606a91-a1bc-43ba-a6df-cd4049c72164" width="600" height="100" />



⚠️ Legal Disclaimer
This project is for educational purposes and ethical use only.
Do not deploy or distribute this tool for malicious purposes.
The author is not responsible for any misuse.


Check out the tutorials to learn how to build the keylogger from scratch.

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/nickagesa/Keylogger.git
   cd Keylogger

2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   
3. **Add your details to the .env** (check out Creating_a_Gmail_App_Password_Guide.pdf)
   
4. **Run File**:
   ```sh
   python Keylogger_main.py
