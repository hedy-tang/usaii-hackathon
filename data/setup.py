import asyncio
import pathlib
from pathlib import Path
from twscrape import API, gather

from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parents[1]  # goes from data/collect.py up to project folder
secrets = dotenv_values(BASE_DIR / ".env")

auth_token = secrets["AUTH_TOKEN"]
ct0 = secrets["ct0"]


async def main():
    api = API()  # or API("accounts.db")

    # Add once; the session is stored in the account database.
    cookies = f"auth_token={auth_token}; ct0={ct0}"
    await api.pool.add_account_cookies("my_account", cookies)



if __name__ == "__main__":
    asyncio.run(main())