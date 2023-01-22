import requests
from Bitzlato.Bitzlto_config import *

class Bitzlato_spot_price:
    def __init__(self):

        self.data = {
                    'symbol': '',
                     }

        self.crypto1 = f'{""}-Bybit'
        self.crypto2 = f'{""}-Bybit'

        self.url_pair = 'https://api.huobi.pro/v2/settings/common/symbols'
        self.url_price = 'https://bitzlato.bz/api/v2/peatio/public/markets'

    async def price(self):

        resp = requests.get(url=self.url_price)
        all_price = resp.json()
        print(all_price)



        return None