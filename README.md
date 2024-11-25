# **Telegram channels parser** - Run Instruction

---
## Prerequisites

- Python 3.11
- pip
- poetry
- Git
- Virtualenv
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

**How to get `telegram_api_id` and `telegram_api_hash`:**
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
    docker-compose up --build
    or
    docker compose up --build
    ```
When the container is up you can use terminal for working with the scraper.
```
docker exec -it tg_channel_parser bash
```
#### Usage
```bash
# Run the scraper
poetry run python parser.py
```
**Flags to configure the scraper:**
1. **-sn, --session_name**: Session name (default: "session_name")
2. **-tz, --time_zone**: Time zone (default: "Europe/Kiev")
3. **-M, --parse_mode**: Mode (default: "interval")
4. **-F, --frequency**: Interval (default: 30)
5. **--limit**: Limit (default: 1)
6. **--refresh**: Clear parsed data in Google Sheets (default: True)



