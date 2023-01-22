import math

import requests

from Binance.Binance_config import payments
from main_config import limits
class Binance_p2p_price:
    def __init__(self, **kwargs):
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "123",
            "content-type": "application/json",
            "Host": "p2p.binance.com",
            "Origin": "https://p2p.binance.com",
            "Pragma": "no-cache",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
        }
        self.json_data = {
            'page': 1,
            'rows': 20,
            'payTypes': kwargs.get('payTypes'),
            'countries': [],
            'publisherType': None,
            'asset': kwargs.get('asset'),
            'fiat': kwargs.get('fiat'),
            'tradeType': kwargs.get('tradeType'),
            'transAmount': kwargs.get('transAmount')
        }

        self.url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
        self.fiat = payments["RUB"]["".join(self.json_data["payTypes"])]
        self.crypto = self.json_data['asset']

    async def price(self, session):
        # try:
        #     async with session.post(url=self.url, headers=self.headers, json=self.json_data) as response:
        #         data = await response.json()
        #         for i in range(5):
        #             if float(data['data'][i]['advertiser']['monthFinishRate']) > 0.85:
        #                 return self.json_data['tradeType'].lower(), self.fiat, self.crypto, float(data['data'][i]['adv']['price'])
        # except Exception:
        try:
            resp = requests.post(url=self.url, headers=self.headers, json=self.json_data)
            data = resp.json()
            min_price = float(data['data'][0]['adv']['price'])
            answer_list = []
            for limit in limits:
                for i in range(len(data['data'])):
                    if float(data['data'][i]['adv']['minSingleTransAmount']) >= limit:
                        if float(data['data'][i]['advertiser']['monthFinishRate']) > 0.85 and float(
                            data['data'][i]['adv']['price']) < (min_price * 1.05):

                            answer_list.append((self.json_data['tradeType'].lower(), self.fiat, self.crypto, float(data['data'][i]['adv']['price']), \
                            float(data['data'][i]['adv']['minSingleTransAmount']), float(data['data'][i]['adv']['dynamicMaxSingleTransAmount']), \
                            'Binance'))
                            break

            return answer_list
                # if float(data['data'][i]['advertiser']['monthFinishRate']) > 0.85 and float(data['data'][i]['adv']['price']) < (min_price * 1.05):
                #     return self.json_data['tradeType'].lower(), self.fiat, self.crypto, float(data['data'][i]['adv']['price']), \
                #             float(data['data'][i]['adv']['minSingleTransAmount']), float(data['data'][i]['adv']['dynamicMaxSingleTransAmount']), \
                #             'Binance'
        except Exception:
            return self.json_data['tradeType'].lower(), self.fiat, self.crypto, 0, 0, 0, 'Binance'

