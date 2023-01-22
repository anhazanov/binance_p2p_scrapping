import requests

from Bybit.bybit_config import crypto_values
from main_config import crypto_list
class Bybit_spot_price:
    def __init__(self):

        self.headers = {
            'authority': 'api2.bybit.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-ru',
            'origin': 'https://www.bybit.com',
            'platform': 'pc',
            'referer': 'https://www.bybit.com/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }

        # self.data = {
        #             'symbol': pair.replace('/', ''),
        #              }

        # self.crypto1 = f'{pair.split("/")[0]}-Bybit'
        # self.crypto2 = f'{pair.split("/")[1]}-Bybit'

        self.url = 'https://api.bybit.com/public/linear/recent-trading-records'
        self.url_1 = 'https://api.bybit.com/spot/v1/symbols'

    async def pair(self):

        try:
            pair_list = []
            resp = requests.get(url=self.url_1)
            data_pair = resp.json()['result']
            for el in data_pair:
                if el['baseCurrency'] in crypto_list and el['quoteCurrency'] in crypto_list:
                    pair_list.append([el['baseCurrency'], el['quoteCurrency']])

            return pair_list
        except Exception:
            return None

    async def price(self, pair, session):
        data = {'symbol': pair.replace('/', ''),}
        crypto1 = pair.split("/")[0]
        crypto2 = pair.split("/")[1]
        try:

            resp = requests.get(url=self.url, headers=self.headers, params=data)

            # async with session.get(url=self.url, headers=self.headers, params=data) as resp:

            return crypto1, crypto2, float(resp.json()['result'][0]['price']), 'Bybit'

        except Exception:
            return crypto1, crypto2, 0, 'Bybit'