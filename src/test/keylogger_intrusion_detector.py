import re
import pickle

# ✅ Load the trained model
model_path = "/content/keylogger_intrusion_model.pkl"
with open(model_path, "rb") as f:
    model = pickle.load(f)

# ✅ Feature extractor
def extract_features_from_keylog(raw_text):
    special_keys = ['enter', 'ctrl', 'alt', 'esc', 'shift', 'tab', 'backspace']
    hacking_keywords = ['netstat', 'msfvenom', 'exploit', 'reverse', 'shell', 'payload', 'tasklist']

    keystroke_length = len(re.findall(r"[a-z0-9]", raw_text))  # Count of normal characters
    special_keys_count = sum(raw_text.count(k) for k in special_keys)
    command_count = sum(raw_text.count(cmd) for cmd in ['netstat', 'tasklist', 'whoami', 'ipconfig'])
    contains_keywords = sum(raw_text.count(k) for k in hacking_keywords)
    password_attempts = raw_text.count("password")
    hour_of_day = 14  # You can modify this if you want dynamic time-based simulation

    return [[keystroke_length, command_count, password_attempts, contains_keywords, special_keys_count, hour_of_day]]

# ✅ List of test keylog files
log_files = ["normal_keylog.txt", "malicious_keylog.txt"]

# ✅ Run tests
for file in log_files:
    try:
        with open(f"/content/{file}", "r") as f:
            raw_data = f.read().lower()

        features = extract_features_from_keylog(raw_data)
        prediction = model.predict(features)[0]

        print(f"\n📄 Testing: {file}")
        print("🔍 Prediction:", "⚠ Potential Exploitation Detected" if prediction == 1 else "✅ Normal Activity")
    except FileNotFoundError:
        print(f"❌ File not found: {file}")
    except Exception as e:
        print(f"❌ Error processing {file}: {e}")
    finally:
        print("🔚 Test completed.\n")
        