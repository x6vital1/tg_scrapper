from auth import GoogleSheetsHelper
from utils import Settings
import signal
import sys
import asyncio

sheet_handler = GoogleSheetsHelper(credentials_file='credentials.json')

def signal_handler(sig, frame):
    print("Stopping the parser...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    try:
        tg_parser = Settings()
        tg_parser.run()
    except asyncio.CancelledError:
        print("\nParser stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
