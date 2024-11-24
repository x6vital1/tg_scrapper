import time
import argparse
import asyncio
from utils.channel_parser import TelegramChannelParser

class PeriodicParser(TelegramChannelParser):
    def __init__(self, sheet_id, sheet_handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sheet_handler = sheet_handler
        self.sheet_id = sheet_id

    async def run_interval(self):
        print("\nChannels scrapper started...")
        print("Press Ctrl+C to stop.")
        while True:
            try:

                data = await self.parse_channels()
                if data:
                    self.save_data(data)
                else:
                    print("No data parsed.")

            except Exception as e:
                print(f"An error occurred during parsing: {e}")

            await asyncio.sleep(self.interval)

    def save_data(self, data, mode='interval'):
        try:
            if data:
                self.sheet_handler.update_parsed_data(self.sheet_id, data, mode)
            else:
                print("No data to save.")
        except Exception as e:
            print(f"Failed to save data: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description="Telegram channel parser")
    parser.add_argument('--interval', type=int, default=60, help='Interval in seconds for periodic parsing')
    parser.add_argument('--limit', type=int, default=10, help='Limit of messages to parse')
    parser.add_argument('--mode', choices=['interval', 'parse_limit'], default='interval', help='Choose parsing mode')
    parser.add_argument('--refresh', action='store_true', help='Clear parsed data in Google Sheets')

    args = parser.parse_args()

    if args.interval <= 0:
        raise ValueError("Interval must be a positive integer.")
    if args.limit <= 0:
        raise ValueError("Limit must be a positive integer.")

    return args
