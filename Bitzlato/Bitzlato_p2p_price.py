import json
import requests
from Bitzlato.Bitzlto_config import *

class Bitzlato_p2p_data():

    def __init__(self, **kwargs):
        self.cookies = {
            '_gid': 'GA1.2.468295180.1658936429',
            '_ga_SGZR2Q1P2G': 'GS1.1.1658936427.1.1.1658936472.0',
            '_ga': 'GA1.2.115778528.1658936427',
        }

        self.headers = {
            'authority': 'bitzlato.bz',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cs;q=0.6',
            # Requests sorts cookies= alphabetically
            # 'cookie': '_gid=GA1.2.468295180.1658936429; _ga_SGZR2Q1P2G=GS1.1.1658936427.1.1.1658936472.0; _ga=GA1.2.115778528.1658936427',
            'referer': 'https://bitzlato.bz/ru/p2p/buy-usdt-rub',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }

        self. params = {
            'lang': 'ru',
            'limit': '15',
            'skip': '0',
            'type': kwargs.get('type'),
            'currency': kwargs.get('currency'),
            'cryptocurrency': kwargs.get('cryptocurrency'),
            'isOwnerVerificated': 'false',
            'isOwnerTrusted': 'false',
            'isOwnerActive': 'false',
            'paymethod': kwargs.get('paymethod'),
            'paymethodSlug': kwargs.get('paymethodSlug'),
            'amountType': 'currency',
            'amount': kwargs.get('amount')
}

        self.url = 'https://bitzlato.bz/api2/p2p/public/exchange/dsa/'
        self.side = sides[self.params['type']]
        self.fiat = payments[self.params['paymethod']]
        self.crypto = self.params['cryptocurrency']

    async def price(self, session):
        try:
            async with session.get(url=self.url, params=self.params, cookies=self.cookies, headers=self.headers) as response:
                data = await response.json()
                return self.side, self.fiat, self.crypto, float(data['data'][0]['rate']), \
                       float(data['data'][0]['limitCurrency']['min']), float(data['data'][0]['limitCurrency']['max']), 'Bitzlato'

        except Exception as ex:
            return None