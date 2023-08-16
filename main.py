import aiohttp
import asyncio
from datetime import datetime

URL_PREFIX = "https://api.privatbank.ua/p24api/exchange_rates?date="


async def main():
    today = datetime.now()

    async with aiohttp.ClientSession() as session:
        url = f"{URL_PREFIX}{today.strftime('%d.%m.%Y')}"
        print(url)

        async with session.get(url) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            response_data = await response.text()
            print(response_data)



if __name__ == "__main__":
    asyncio.run(main())
