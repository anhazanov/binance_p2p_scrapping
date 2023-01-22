from Kucoin.Kucoin_config import crypto_values
from main_config import crypto_list

class Kucoin_spot_price:
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
        self.url = 'https://api.kucoin.com/api/v1/market/allTickers'

    async def get_price(self, session):
        try:
            answer = []
            async with session.get(url=self.url) as response:
                data = await response.json()
                for pair in data['data']['ticker']:
                    ticker = pair['symbol']
                    if ticker.split("-")[0] in crypto_list and ticker.split("-")[1] in crypto_list:
                        answer.append([ticker.split("-")[0], ticker.split("-")[1], float(pair['last']), 'Kucoin'])
            return answer
        except Exception:
            return None