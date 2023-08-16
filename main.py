import aiohttp
import asyncio
import json
from pprint import pprint
from datetime import datetime, timedelta

URL_PREFIX = "https://api.privatbank.ua/p24api/exchange_rates?date="

RESULT_LIST = []


async def currency_request(sub_days):
    today = datetime.now()

    async with aiohttp.ClientSession() as session:
        new_datetime = today - timedelta(days=sub_days)

        new_datetime_formatted = new_datetime.strftime('%d.%m.%Y')
        # print(new_datetime_formatted)

        url = f"{URL_PREFIX}{new_datetime_formatted}"

        async with session.get(url) as response:
            # print("Status:", response.status)
            # print("Content-type:", response.headers['content-type'])

            response_data = await response.text()
            # print(response_data)
            await get_json_currency(response_data, new_datetime_formatted)


async def get_json_currency(json_text, new_datetime_formatted):
    currency_objects = json.loads(json_text)

    exchange_list = []
    # print(new_datetime_formatted)
    for currency_dict in currency_objects["exchangeRate"]:
        currency = currency_dict["currency"]

        if currency == "USD" or currency == "EUR":
            exchange_list.append({
                "currency": currency_dict['currency'],
                "saleRate": currency_dict['saleRate'],
                "purchaseRate": currency_dict['purchaseRate']})

    RESULT_LIST.append({
        "date": new_datetime_formatted,
        "exchange": exchange_list
    })

    # print(f"currency: {currency_dict['currency']} saleRate:{currency_dict['saleRate']}")


async def main(check_days):
    await asyncio.gather(*[currency_request(i) for i in range(0, check_days)])


if __name__ == "__main__":
    # check_days = int(input("check_days"))
    check_days = 3

    asyncio.run(main(check_days))
    # asyncio.run(currency_request(6))

    pprint(RESULT_LIST)
