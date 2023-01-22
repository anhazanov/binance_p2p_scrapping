import requests
import asyncio
import aiohttp

from Huobi.Huobi_config import *
from main_config import limits

class Huobi_p2p_data():

    def __init__(self, **kwargs):
        self.headers = {
            'authority': 'otc-api.bitderiv.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cs;q=0.6',
            'client-type': 'web',
            'origin': 'https://c2c.huobi.com',
            'otc-language': 'ru-RU',
            'portal': 'web',
            'referer': 'https://c2c.huobi.com/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'token': 'undefined',
            'trace_id': 'bb413409-0f3b-4405-a45e-2120bfd0ef7c',
            'uid': '0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        self.params = {
            'coinId': kwargs.get('coinId'),
            'currency': kwargs.get('currency'),
            'tradeType': kwargs.get('tradeType'),
            'currPage': '1',
            'payMethod': kwargs.get('payMethod'),
            'acceptOrder': '0',
            'country': '',
            'blockType': 'general',
            'online': '1',
            'range': '0',
            # 'amount': kwargs.get('amount'),
            'isThumbsUp': 'false',
            'isMerchant': 'false',
            'isTraded': 'false',
            'onlyTradable': 'false',
        }

        self.url = 'https://otc-api.bitderiv.com/v1/data/trade-market'
        self.fiat = payments[self.params["payMethod"]]
        self.crypto = crypto_values[self.params["coinId"]]

    async def price(self, session):
        try:
            response = requests.get('https://otc-api.bitderiv.com/v1/data/trade-market', params=self.params, headers=self.headers)
            data = response.json()
            min_price = float(data['data'][0]['price'])
            answer_list = []
            for limit in limits:
                for i in range(len(data['data'])):
                    if float(data['data'][i]['minTradeLimit']) >= limit:
                        if float(data['data'][i]['orderCompleteRate']) > 80 and float(data['data'][i]['price']) < (min_price * 1.05):
                            if self.params['tradeType'] == 'sell':
                                answer_list.append(('buy', self.fiat, self.crypto, float(data['data'][i]['price']),
                                       float(data['data'][i]['minTradeLimit']), float(data['data'][i]['maxTradeLimit']), 'Huobi'))
                                break
                            elif self.params['tradeType'] == 'buy':
                                answer_list.append(('sell', self.fiat, self.crypto, float(data['data'][i]['price']),
                                        float(data['data'][i]['minTradeLimit']), float(data['data'][i]['maxTradeLimit']), 'Huobi'))
            return answer_list
        except Exception:
             return None

