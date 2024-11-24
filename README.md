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
git clone https://github.com/DemetrSin/TeamOtzovik.git

cd TeamOtzovik
```
## Install `poetry` and create a virtual environment
```sh
pip install poetry
poetry init
```

## Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```bash
API_ID=telegram_api_id
API_HASH=telegram_api_id
SHEET_ID=google_sheets_id
```

#### Building and Running the Docker Containers
Build and start the containers.
* using standalone tool **docker-compose**:
    ```
    docker-compose up --build
    or
    docker compose up --build
    ```