import base64
import time
import datetime
import random
import requests
import jwt

from Garantex.Garantex_config import privat_key, uid, public_key

class Garantex_p2p_price:

    def __init__(self, **kwargs):
        host = 'garantex.io'

        key = base64.b64decode(privat_key)
        iat = int(time.mktime(datetime.datetime.now().timetuple()))
        claims = {
            "exp": iat + 1 * 60 * 60,  # JWT Request TTL in seconds since epoch
            "jti": hex(random.getrandbits(12)).upper()
        }
        jwt_token = jwt.encode(claims, key, algorithm="RS256")
        ret = requests.post('https://dauth.' + host + '/api/v1/sessions/generate_jwt',
                            json={'kid': uid, 'jwt_token': jwt_token})
        token = ret.json().get('token')

        self.data = {
            'direction': kwargs.get('direction'),
        }

        self.url = 'https://garantex.io/api/v2/otc/ads'

        self.headers = {'Authorization': 'Bearer ' + token}
        # self.side = kwargs.get('side')
        # self.fiat = f'{self.params["legal"]}-Kucoin'
        # self.crypto = f"{self.params['currency']}-Kucoin"

    async def price(self, session):
        try:
            async with session.get(url=self.url,
                                   # headers=self.headers,
                                   data=self.data) as response:
                data = await response.json()
                for el in data:
                    print(el['payment_method'], el['price'])
            return None

        except Exception:
            return None