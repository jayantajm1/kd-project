import re
import pickle
import argparse

# ✅ Feature extractor
def extract_features_from_keylog(raw_text):
    special_keys = ['enter', 'ctrl', 'alt', 'esc', 'shift', 'tab', 'backspace']
    hacking_keywords = ['netstat', 'msfvenom', 'exploit', 'reverse', 'shell', 'payload', 'tasklist']

    keystroke_length = len(re.findall(r"[a-z0-9]", raw_text))
    special_keys_count = sum(raw_text.count(k) for k in special_keys)
    command_count = sum(raw_text.count(cmd) for cmd in ['netstat', 'tasklist', 'whoami', 'ipconfig'])
    contains_keywords = sum(raw_text.count(k) for k in hacking_keywords)
    password_attempts = raw_text.count("password")
    hour_of_day = 14  # default value for static test

    return [[keystroke_length, command_count, password_attempts, contains_keywords, special_keys_count, hour_of_day]]

# ✅ CLI Argument parser
def main():
    parser = argparse.ArgumentParser(description="🔐 Keylogger Intrusion Detection CLI Tool")
    parser.add_argument("logfile", help="Path to keylog .txt file")
    parser.add_argument("--model", default="keylogger_intrusion_model.pkl", help="Path to .pkl model file")
    args = parser.parse_args()

    # Load model
    try:
        with open(args.model, "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print(f"❌ Model file not found: {args.model}")
        return

    # Read log
    try:
        with open(args.logfile, "r") as f:
            raw_data = f.read().lower()
    except FileNotFoundError:
        print(f"❌ Keylog file not found: {args.logfile}")
        return

    # Predict
    features = extract_features_from_keylog(raw_data)
    prediction = model.predict(features)[0]

    print(f"\n📄 Log file: {args.logfile}")
    print("🔍 Prediction:", "⚠️ Potential Exploitation Detected" if prediction == 1 else "✅ Normal Activity")

if __name__ == "__main__":
    main()
    # Example usage: python keylogger_intrusion_cli.py normal_keylog.txt --model keylogger_intrusion_model.pkl
    # Example usage: python keylogger_intrusion_cli.py malicious_keylog.txt --model keylogger_intrusion_model.pkl