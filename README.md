# **Telegram channels parser** - Run Instruction

## How It Works

This script is designed to parse messages from Telegram channels and upload the data to Google Sheets. It supports two
modes of operation:

**`Interval` Mode:**

* This mode is intended for periodic parsing of specified channels with real-time updates to Google Sheets.
* The script runs, parses all channels, updates the Google Sheet, waits for a specified interval (default is 30
  seconds),
  and repeats the process.
* For each channel, one row of the sheet is updated with the latest data (message date, keywords, post URL).

**`Parse_Limit` Mode:**

* This mode performs a one-time parsing of a specified number of messages from each channel.
* After parsing, the data is uploaded to Google Sheets, adding new rows for each message.
* The user can set a limit on the number of messages per channel, controlling the amount of data to be parsed.

## Key Features:

* **Periodic Parsing in `Interval` Mode:** Automatically updates the data in the sheet at regular intervals.
* **One-time Parsing in `Parse_Limit` Mode:** Allows you to parse a fixed number of messages from each channel and
  upload them
  to the sheet.
* **Google Sheets Updates:** Parsed data from Telegram channels is saved and updated in Google Sheets via the Google
  Sheets
  API.

## Requirements:

1. **Telegram Authentication:**

* The script requires Telegram authentication to simulate user actions for proper operation.

2. **Google Cloud Console Account:**

- You need to create an account on Google Cloud Console to access the Google Sheets API.
- Create service account credentials and download the `credentials.json` file, which will be used for authentication and
  working with Google Sheets.

---

## Prerequisites

- Python 3.11
- pip
- poetry
- Git
- Docker
- Docker Compose

---

## Clone the Repository

```sh
git clone https://github.com/x6vital1/tg_scrapper.git

cd tg_scrapper
```

## Configuration

* To configure the scraper, you need to create a `config.json` file in the `root` directory.
* The `config.json` file should contain the following parameters:

```json
{
  "session_name": "session_name",
  "time_zone": "Europe/Kiev",
  "mode": "interval",
  "api": {
    "api_id": 12345678,
    "api_hash": "telegram_api_hash",
    "sheet_id": "your_google_sheet_id"
  },
  "interval": 30,
  "limit": 1,
  "refresh": true
}
```

**How to get `api_id` and `telegram_api_hash`:**

1. Follow to the [Telegram App manager](https://my.telegram.org/apps)
2. Login to your Telegram account

**How row to get `your_google_sheet_id`:**

1. Follow to the [Google Sheets](https://docs.google.com/spreadsheets/)
2. Login to your Google account
3. Create a new spreadsheet
4. Table ID starts after `/d/` and ends with `/edit`
   *Example: https://docs.google.com/spreadsheets/d/1eCdtRKMBR3E-FDbBGGxybYgb_y0HI7ZVKsocAjT-z_I/edit#gid=0*

#### Building and Running the Docker Containers

Build and start the containers.

* using standalone tool **docker-compose**:
    ```
    docker-compose up --build -d
    or
    docker compose up --build -d
    ```

#### Usage

When the container is up you can use terminal for working with the scraper.

```
docker-compose exec parser python parser.py # You cant add flags here if it needed

docker-compose stop # Stop the containers
docker-compose start # Start the containers
```

**Please note that the phone number must be specified without "+" during the first authorization, then the data is saved
during the session and you do not have to be authenticated.**

#### Flags

**Flags to configure the scraper:**

1. **-sn, --session_name**: Session name (default: "session_name")
2. **-tz, --time_zone**: Time zone (default: "Europe/Kiev")
3. **-M, --parse_mode**: Mode interval or parse_limit (default: "interval")
4. **-F, --frequency**: Interval (default: 30)
5. **--limit**: Limit (default: 1)
6. **--refresh**: Clear parsed data in Google Sheets (default: True)



