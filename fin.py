import hashlib
import os
import json
import sys

# --- Configuration ---
TARGET_DIR = "."              # Monitor the current directory
HASH_DB = "baseline.json"     # Database file
IGNORE_FILES = ["fin.py", "baseline.json", "exploit_demo.py"] # Files to skip

def calculate_sha256(filepath):
    """Generate a SHA-256 hash for a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read in chunks to handle large files efficiently
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (FileNotFoundError, PermissionError):
        return None

def create_baseline():
    """Scan directory and save hashes to a file."""
    baseline = {}
    file_count = 0
    
    for root, _, files in os.walk(TARGET_DIR):
        for c_file in files:
            # Filter out the script and the DB itself
            if c_file in IGNORE_FILES:
                continue
                
            path = os.path.join(root, c_file)
            hash_value = calculate_sha256(path)
            if hash_value:
                baseline[path] = hash_value
                file_count += 1
    
    with open(HASH_DB, "w") as f:
        json.dump(baseline, f, indent=4)
    print(f"[+] Baseline created successfully with {file_count} files.")

def monitor():
    """Compare current files against the baseline."""
    if not os.path.exists(HASH_DB):
        print("[-] Error: No baseline found! Run 'python fin.py --baseline' first.")
        return

    with open(HASH_DB, "r") as f:
        baseline = json.load(f)

    current_files = {}
    for root, _, files in os.walk(TARGET_DIR):
        for c_file in files:
            if c_file in IGNORE_FILES:
                continue
                
            path = os.path.join(root, c_file)
            current_files[path] = calculate_sha256(path)

    print("-" * 30)
    print("SCANNING FOR INTEGRITY CHANGES...")
    print("-" * 30)

    alerts_triggered = False

    # 1. Check for modifications and deletions
    for path, old_hash in baseline.items():
        if path not in current_files:
            print(f"!!! ALERT: File DELETED -> {path}")
            alerts_triggered = True
        elif current_files[path] != old_hash:
            print(f"!!! ALERT: File MODIFIED -> {path}")
            alerts_triggered = True

    # 2. Check for new files
    for path in current_files:
        if path not in baseline:
            print(f"!!! ALERT: NEW FILE DETECTED -> {path}")
            alerts_triggered = True

    if not alerts_triggered:
        print("[OK] No integrity violations detected.")
    print("-" * 30)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--baseline":
        create_baseline()
    else:
        monitor()