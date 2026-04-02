# 🛡️ File Integrity Checker (FIM) 

A lightweight, proactive defensive security tool built in **Python** to monitor and detect unauthorized changes in a directory. This project demonstrates a practical application of the **Integrity** pillar in the CIA Triad (Confidentiality, Integrity, Availability).

## 🚀 Overview
In modern cybersecurity, detecting an intrusion is just as critical as preventing one. This tool uses **SHA-256 cryptographic hashing** to create a baseline of "known-good" files. When executed, it re-scans the directory and alerts the user if any files have been:
- **Modified:** Content within the file was changed.
- **Deleted:** A critical file was removed from the system.
- **Added:** A new, potentially malicious file was introduced.

## 🛠️ Technical Features
- **Secure Hashing:** Uses `hashlib` with SHA-256 (collision-resistant) for file verification.
- **Optimized Performance:** Reads files in **4KB chunks**, ensuring the script remains memory-efficient even for large files.
- **Exclusion Filter:** Built-in logic to ignore the script itself and its database to prevent false positives.
- **JSON Database:** Stores the baseline state in a structured `baseline.json` file for easy auditing.

## 📁 Project Structure
- `fin.py`: The main defensive monitoring engine.
- `exploit_demo.py`: A simulation script that mimics an attacker (modifying configs, dropping malware, deleting logs).
- `web_config.conf`: Sample configuration file for monitoring.
- `user_permissions.csv`: Sample sensitive data file.
- `integrity_check.log`: Sample system log.

## 🚦 How to Run

### 1. Create a Baseline
Initialize the "known-good" state of your directory:
```bash
python fin.py --baseline
