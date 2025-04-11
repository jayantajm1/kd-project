import re
import pickle
from datetime import datetime

# ✅ Load the trained model (ensure file is uploaded in /content/)
model_path = "/content/keylogger_intrusion_model.pkl"
keylog_path = "/content/normal_keylog.txt"

# Load model
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Read keylog data
with open(keylog_path, "r") as f:
    raw_data = f.read().lower()

# ✅ Feature extraction function with 6 features
def extract_features_from_keylog(raw_text):
    special_keys = ['enter', 'ctrl', 'alt', 'esc', 'shift', 'tab', 'backspace']
    hacking_keywords = ['netstat', 'msfvenom', 'exploit', 'reverse', 'shell', 'payload', 'tasklist']

    keystroke_length = len(re.findall(r"[a-z0-9]", raw_text))  # Count of normal characters
    special_keys_count = sum(raw_text.count(k) for k in special_keys)
    command_count = sum(raw_text.count(cmd) for cmd in ['netstat', 'tasklist', 'whoami', 'ipconfig'])
    contains_keywords = sum(raw_text.count(k) for k in hacking_keywords)
    password_attempts = raw_text.count("password")
    hour_of_day = datetime.now().hour  # Current hour (0–23)

    # ✅ Ensure feature order matches training: 
    # ["keystroke_length", "command_detected", "repeated_password_inputs",
    #  "suspicious_keywords", "access_to_admin_tools", "hour_of_day"]
    return [[
        keystroke_length,
        command_count,
        password_attempts,
        contains_keywords,
        special_keys_count,
        hour_of_day
    ]]

# Extract features
features = extract_features_from_keylog(raw_data)

# ✅ Make prediction
prediction = model.predict(features)[0]

# ✅ Output result
if prediction == 1:
    print("⚠ Potential Exploitation Detected")
else:
    print("✅ Normal Activity")