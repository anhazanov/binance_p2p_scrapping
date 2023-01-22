import requests
from Huobi.Huobi_config import crypto_values
from main_config import crypto_list

class Huobi_spot_price:
    def __init__(self):

        self.data = {
                    'symbol': '',
                     }

        self.crypto1 = f'{""}-Bybit'
        self.crypto2 = f'{""}-Bybit'

        self.url_pair = 'https://api.huobi.pro/v2/settings/common/symbols'
        self.url_price = 'https://api.huobi.pro/market/tickers'

    async def get_pair(self):
        resp = requests.get(url=self.url_pair)
        data_pair = resp.json()['data']
        pair_list = []
        for el in data_pair:
            pair = el['dn']
            if pair.split('/')[0] in crypto_list and pair.split('/')[1] in crypto_list:
                pair_list.append([pair, pair.split('/')[0], pair.split('/')[1]])

        resp = requests.get(url=self.url_price)
        all_price = resp.json()['data']
        spot_price = []
        for el in all_price:
            for pair in pair_list:
                if el['symbol'] == pair[0].replace('/', '').lower():
                    spot_price.append([pair[1], pair[2], el['bid'], 'Huobi'])

        return spot_price
