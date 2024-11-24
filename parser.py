from utils import PeriodicParser, EnvLoader, parse_args
from auth import GoogleSheetsHelper
import asyncio

sheet_handler = GoogleSheetsHelper(credentials_file='credentials.json')


def main():
    try:
        session_name = input("Please enter the session name: ")
        time_zone = input("Please enter the time zone example (Europe/Kiev): ")
        args = parse_args()

        env_loader = EnvLoader()
        sheet_id = env_loader.get_env('SHEET_ID')

        parser = PeriodicParser(
            api_id=env_loader.get_env('API_ID'),
            api_hash=env_loader.get_env('API_HASH'),
            channels=sheet_handler.get_channels_urls(sheet_id),
            interval=args.interval,
            limit=args.limit,
            sheet_handler=sheet_handler,
            session_name=session_name,
            sheet_id=sheet_id,
            time_zone=time_zone
        )

        if args.refresh:
            sheet_handler.clear_parsed_data(sheet_id)
        try:
            if args.mode == 'interval':
                asyncio.run(parser.run_interval())
            elif args.mode == 'parse_limit':
                data = asyncio.run(parser.parse_channels())
                parser.save_data(data, mode='parse_limit')
            else:
                print("Invalid mode specified. Please use 'interval' or 'parse_limit'.")
        except KeyboardInterrupt:
            print("\nParser stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
