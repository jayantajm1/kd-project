# test keylogger
# 🛡️ Keylogger Intrusion Detection CLI Tool

This is a simple command-line tool to detect **potential exploitation activities** based on keylog data. It uses a trained machine learning model (`.pkl`) to classify whether the activity is **normal** or **malicious**.

---

## 📂 Features

- Detects suspicious commands and keywords from keylogs
- Trained with synthetic labeled data using RandomForestClassifier
- CLI-based and easy to use
- Extensible with additional features or models

---

## 🔧 How to Use

### 1. Save the Script

Save the tool script as:

---

### 2. Prepare Your Files

Ensure you have:

- A trained model file: `keylogger_intrusion_model.pkl`
- A keylog `.txt` file to test: e.g., `suspicious_keylog.txt` or `normal_keylog.txt`

---

### 3. Run from Terminal

Basic usage (with model in same directory):

```bash
python keylog_detector.py suspicious_keylog.txt

