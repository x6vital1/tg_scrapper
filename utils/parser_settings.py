import argparse
import asyncio
import json
import os

from colorama import Fore, Style, init


from auth import GoogleSheetsHelper
from utils.channel_parser import TelegramChannelParser

init(autoreset=True)


class Settings:
    def __init__(self, config_file='config.json'):
        self.config_file = self.load_config(config_file)
        self.sheet_handler = GoogleSheetsHelper(credentials_file='credentials.json')

        self.sheet_id = self.config_file['api']['sheet_id']
        self.api_id = self.config_file['api']['api_id']
        self.api_hash = self.config_file['api']['api_hash']

        self.session_name = self.config_file.get('session_name', 'default')
        self.time_zone = self.config_file.get('time_zone', 'Europe/Kiev')
        self.parse_mode = self.config_file.get('parse_mode', 'interval')
        self.frequency = self.config_file.get('frequency', 60)
        self.limit = self.config_file.get('limit', 1)
        self.refresh = self.config_file.get('refresh', False)

        self.args = self.parse_args()
        self.override_config_with_args()

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="Telegram channel parser")
        parser.add_argument('-sn', '--session_name', type=str, help="Session name")
        parser.add_argument('-tz', '--time_zone', type=str, help="Time zone")
        parser.add_argument('-F', '--frequency', type=int, help="Interval in seconds")
        parser.add_argument('--limit', type=int, help="Limit of messages")
        parser.add_argument('-M', '--parse_mode', choices=['interval', 'parse_limit'], help="Parsing mode")
        parser.add_argument('--refresh', action='store_true', help="Clear parsed data in Google Sheets")
        return parser.parse_args()

    def override_config_with_args(self):
        if self.args.session_name:
            self.session_name = self.args.session_name
        if self.args.time_zone:
            self.time_zone = self.args.time_zone
        if self.args.frequency:
            self.frequency = self.args.frequency
        if self.args.limit:
            self.limit = self.args.limit
        if self.args.parse_mode:
            self.parse_mode = self.args.parse_mode
        if self.args.refresh:
            self.refresh = self.args.refresh

    def print_config(self):
        print(f"{Fore.CYAN}Session name:{Style.BRIGHT} {Fore.GREEN}{self.session_name}")
        print(f"{Fore.CYAN}Time zone:{Style.BRIGHT} {Fore.GREEN}{self.time_zone}")
        print(f"{Fore.CYAN}Interval:{Style.BRIGHT} {Fore.GREEN}{self.frequency}")
        print(f"{Fore.CYAN}Limit:{Style.BRIGHT} {Fore.GREEN}{self.limit}")
        print(f"{Fore.CYAN}Parse mode:{Style.BRIGHT} {Fore.GREEN}{self.parse_mode}")
        print(f"{Fore.CYAN}Refresh:{Style.BRIGHT} {Fore.GREEN}{self.refresh}")
        print(f"{Fore.LIGHTBLUE_EX}Config loaded successfully.{Style.RESET_ALL}")
        print(f"{Fore.RED}Press Ctrl+C to stop the parser.{Style.RESET_ALL}")

    def run(self):
        self.print_config()

        parser = PeriodicParser(
            api_id=self.api_id,
            api_hash=self.api_hash,
            channels=self.sheet_handler.get_channels_urls(self.sheet_id),
            interval=self.frequency,
            limit=self.limit,
            sheet_handler=self.sheet_handler,
            session_name=self.session_name,
            sheet_id=self.sheet_id,
            time_zone=self.time_zone
        )
        if self.parse_mode == 'interval':
            asyncio.run(parser.run_interval())
        elif self.parse_mode == 'parse_limit':
            data = asyncio.run(parser.parse_channels())
            parser.save_data(data, mode='parse_limit')

    @staticmethod
    def load_config(config_path):
        if os.path.exists(config_path):
            with open(config_path, "r") as config_file:
                return json.load(config_file)
        else:
            print(f"Config file {config_path} not found. Using default values.")
            return {}


class PeriodicParser(TelegramChannelParser):
    def __init__(self, sheet_id, sheet_handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sheet_handler = sheet_handler
        self.sheet_id = sheet_id

    async def run_interval(self):
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
