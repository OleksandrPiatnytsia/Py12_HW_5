import sys
import aiohttp
import asyncio
import json
from pprint import pprint
from datetime import datetime, timedelta

URL_PREFIX = "https://api.privatbank.ua/p24api/exchange_rates?date="

RESULT_LIST = []


async def currency_request(sub_days, session):
    today = datetime.now() - timedelta(
        days=1)  # мінус один день від поточної дати бо курси можуть бути ще не встановлені

    new_datetime = today - timedelta(days=sub_days)

    new_datetime_formatted = new_datetime.strftime('%d.%m.%Y')

    url = f"{URL_PREFIX}{new_datetime_formatted}"

    async with session.get(url) as response:
        if response.status == 200:
            response_data = await response.text()
            await get_json_currency(response_data, new_datetime_formatted)


async def get_json_currency(json_text, new_datetime_formatted):
    currency_objects = json.loads(json_text)
    # print(currency_objects)
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


async def main(check_days):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[currency_request(i, session) for i in range(0, check_days)])


if __name__ == "__main__":
    arguments = sys.argv

    other_arguments = arguments[1:]
    if other_arguments:
        check_days = int(other_arguments[0])
        if check_days > 10:
            print(f"Number {check_days} is too large, enter less than 10")
        else:
            asyncio.run(main(check_days))

            pprint(RESULT_LIST)
    else:
        print("No arguments!")
