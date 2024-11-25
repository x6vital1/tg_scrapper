import gspread
from google.auth.exceptions import GoogleAuthError
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from datetime import datetime


class GoogleSheetsHelper:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.client = self.authenticate()

    def authenticate(self):
        try:
            creds = Credentials.from_service_account_file(self.credentials_file, scopes=[
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ])
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
            client = gspread.authorize(creds)
            return client
        except GoogleAuthError as e:
            print(f"Authentication error: {e}")
            raise

    def get_channels_urls(self, spreadsheet_id):
        try:
            sheet = self.client.open_by_key(spreadsheet_id).sheet1
            return sheet.col_values(1)
        except gspread.exceptions.APIError as e:
            print(f"Error getting channels URLs: {e}")
            raise

    def update_parsed_data(self, spreadsheet_id, parsed_data, mode, sheet_name='Parsed Data'):
        try:
            # Получаем или создаем нужный лист
            sheet = self._get_or_create_sheet(spreadsheet_id, sheet_name)

            # Получаем существующие каналы из первого листа
            existing_channels = self.client.open_by_key(spreadsheet_id).sheet1.col_values(1)

            rows_to_add = []

            if mode == 'interval':
                # Проходим по каждому каналу и обновляем одну строку
                for channel in existing_channels:
                    # Ищем последнее сообщение для канала в parsed_data
                    channel_data_list = [row for row_list in parsed_data for row in row_list if row['channel'] == channel]
                    if channel_data_list:
                        channel_data = channel_data_list[-1]  # последнее сообщение для канала
                        date_str = channel_data['date'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(channel_data['date'], datetime) else channel_data['date']
                        row_data = [channel_data['channel'], ', '.join(channel_data['keywords']), channel_data['post_url'], date_str]
                    else:
                        # Если данных нет, ставим прочерки
                        row_data = [channel, '----', '----', '----']

                    # Обновляем существующую строку для канала
                    row_index = existing_channels.index(channel) + 1
                    sheet.update(f'A{row_index}:D{row_index}', [row_data])

            else:
                # В режиме parse_limit добавляем новые строки
                for row_list in parsed_data:
                    for channel_data in row_list:
                        date_str = channel_data['date'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(channel_data['date'], datetime) else channel_data['date']
                        row_data = [channel_data['channel'], ', '.join(channel_data['keywords']), channel_data['post_url'], date_str]
                        rows_to_add.append(row_data)

                # Добавляем строки в таблицу
                if rows_to_add:
                    sheet.append_rows(rows_to_add)

        except gspread.exceptions.APIError as e:
            print(f"Error updating parsed data: {e}")
            raise

    def _get_or_create_sheet(self, spreadsheet_id, sheet_name):
        try:
            spreadsheet = self.client.open_by_key(spreadsheet_id)
            try:
                sheet = spreadsheet.worksheet(sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                sheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=4)
            return sheet
        except gspread.exceptions.APIError as e:
            print(f"Error getting or creating sheet: {e}")
            raise

    def clear_parsed_data(self, spreadsheet_id, sheet_name='Parsed Data'):
        try:
            sheet = self._get_or_create_sheet(spreadsheet_id, sheet_name)
            sheet.clear()
            print(f"Sheet '{sheet_name}' cleared successfully.")
        except gspread.exceptions.APIError as e:
            print(f"Error clearing sheet '{sheet_name}': {e}")
            raise
