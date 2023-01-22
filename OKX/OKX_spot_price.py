import aiohttp

from OKX.OKX_config import crypto_values
from main_config import crypto_list

class OKX_spot_price:
    def __init__(self, pair):
        self.headers = {
            'authority': 'www.okx.com',
            'accept': 'application/json',
            'accept-language': 'ru-RU',
            'app-type': 'web',
            # Requests sorts cookies= alphabetically
            # 'cookie': 'first_ref=https%3A%2F%2Fwww.google.com%2F; amp_56bf9d_okx.com=cUc4KGhAvEnMOlyh2lhM76...1g7girqpp.1g7gk9cu2.7.1.8; amp_56bf9d=cUc4KGhAvEnMOlyh2lhM76...1g7hg905h.1g7hg9m5d.4.2.6; locale=en_US',
            'devid': '3b525e5f-9891-4fcc-ab43-fc4fc6b47778',
            'referer': 'https://www.okx.com/ru/trade-spot/btc-usdt',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-cdn': 'https://static.okx.com',
            'x-utc': '3',
        }

        self.params = {
            'instId': pair,
            'sz': '10',
        }
        self.url = 'https://www.okx.com/priapi/v5/market/books'
        self.pair_1 = pair.split('-')[0]
        self.pair_2 = pair.split('-')[1]

    async def price(self, session):
        try:
            async with session.get(url=self.url, headers=self.headers, params=self.params) as response:
                data = await response.json()
                if self.pair_1 in crypto_list and self.pair_2 in crypto_list:
                    return self.pair_1, self.pair_2, float(data['data'][0]['asks'][0][0]), 'OKX'
        except Exception:
            return self.pair_1, self.pair_2, 0, 'OKX'

class OKX_spot_pair:
    def __init__(self):
        self.headers = {
            'authority': 'www.okx.com',
            'accept': 'application/json',
            'accept-language': 'ru-RU',
            'app-type': 'web',
            # Requests sorts cookies= alphabetically
            # 'cookie': 'first_ref=https%3A%2F%2Fwww.google.com%2F; amp_56bf9d_okx.com=cUc4KGhAvEnMOlyh2lhM76...1g7girqpp.1g7gk9cu2.7.1.8; amp_56bf9d=cUc4KGhAvEnMOlyh2lhM76...1g7hg905h.1g7hg9acj.3.2.5; locale=ru_RU',
            'devid': '3b525e5f-9891-4fcc-ab43-fc4fc6b47778',
            'referer': 'https://www.okx.com/ru/trade-spot/btc-usdt',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-cdn': 'https://static.okx.com',
            'x-utc': '3',
        }
        self.params = {
            't': '1657371154432',
            'instType': 'SPOT',
        }
        self.url = 'https://www.okx.com/priapi/v5/public/simpleProduct'

    async def get_pair(self, session):
        spot_pair = []
        try:
            async with session.get(url=self.url, headers=self.headers, params=self.params) as response:
                data = await response.json()
                for el in data['data']:
                    spot_pair.append(el['instId'])
                return spot_pair
        except Exception:
            return None