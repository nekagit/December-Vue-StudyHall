#!/usr/bin/env python3
import subprocess
import sys
import os
import argparse
import time

def build_frontend():
    print("Building frontend...")
    result = subprocess.run(["npm", "run", "build"], cwd="frontend")
    if result.returncode == 0:
        print("Frontend built successfully.")
    else:
        print("Frontend build failed.")
        sys.exit(1)

def start_backend():
    print("Starting backend server on http://localhost:5000...")
    subprocess.run(["python", "backend/main.py"], cwd=".")

def start_frontend():
    print("Starting frontend dev server on http://localhost:5173...")
    subprocess.run(["npm", "run", "dev"], cwd="frontend")

def dev_mode():
    print("Starting development mode...")
    print("Backend: http://localhost:5000")
    print("Frontend: http://localhost:5173")
    
    # Start backend (non-blocking)
    backend_process = subprocess.Popen(
        ["python", "backend/main.py"],
        cwd="."
    )
    
    # Start frontend (blocking)
    try:
        subprocess.run(["npm", "run", "dev"], cwd="frontend")
    except KeyboardInterrupt:
        print("\nShutting down...")
        backend_process.terminate()
        backend_process.wait()

def main():
    parser = argparse.ArgumentParser(description="StudyHall Management Tool")
    parser.add_argument("action", choices=["build", "run", "dev"], help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "build":
        build_frontend()
    elif args.action == "run":
        start_backend()
    elif args.action == "dev":
        dev_mode()

if __name__ == "__main__":
    main()
