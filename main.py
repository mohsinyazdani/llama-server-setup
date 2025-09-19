#!/usr/bin/env python3
"""
LLama Server Main Entry Point
"""
import json
import sys

try:
    import requests
except ImportError:
    print("Installing required packages...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
        print("Successfully installed requests")
    except subprocess.CalledProcessError:
        print("Failed to install requests. Please run: pip install requests")
        sys.exit(1)

from setup import LlamaServerSetup

def main():
    setup = LlamaServerSetup()

    try:
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nWarning: Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
