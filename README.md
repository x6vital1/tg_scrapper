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

## Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```bash
API_ID=telegram_api_id
API_HASH=telegram_api_hash
SHEET_ID=google_sheets_id
```

**How to get `telegram_api_id` and `telegram_api_hash`:**
1. Follow to the [Telegram App manager] (https://my.telegram.org/apps)
2. Login to your Telegram account

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

Once the containers are up, you can interact with the scraper. Here are a few examples of commands you can run inside the container:

```bash
# Run the scraper
poetry run python parser.py
```
**Flags to configure the scraper:**
1. `--mode` - `interval` or `parse_limit`. Default is `interval`.
2. `--interval` - Interval in seconds for periodic parsing. Default is 60.
3. `--limit` - Limit of messages to parse. Default is 1.
4. `--refresh` - Clear parsed data in Google Sheets.

