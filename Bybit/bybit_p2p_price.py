import math

import requests
import asyncio
import aiohttp

from Bybit.bybit_config import *
from main_config import limits

class Bybit_p2p_data():

    def __init__(self, **kwargs):
        self.headers = {
            'authority': 'api2.bybit.com',
            'accept': 'application/json',
            'accept-language': 'en-US',
            # Requests sorts cookies= alphabetically
            # 'cookie': '_by_l_g_d=bc291a57-d12c-0324-7580-b481e54e4edb; BYBIT_REG_REF_prod={"lang":"ru-RU","g":"bc291a57-d12c-0324-7580-b481e54e4edb","referrer":"www.youtube.com/","source":"youtube.com","medium":"referral","ref":"RRZPZL","url":"https://www.bybit.com/ru-RU/invite/?ref=RRZPZL&utm_campaign=ByBit"}; _gcl_au=1.1.876710930.1655985242; _ga=GA1.2.1814419144.1655985243; _ym_uid=1655985243234512566; _ym_d=1655985243; tmr_lvid=31fb268131f12d3732aa26d49d6cb8ad; tmr_lvidTS=1655985242910; sensorsdata2015session=%7B%7D; _by_ref=https://www.google.com/; b_t_c_k=; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2229053550%22%2C%22first_id%22%3A%2218176b3966099d-013e28086d90544-26021b51-2073600-18176b39661c5f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22_a_u_v%22%3A%220.0.5%22%2C%22%24latest_utm_campaign%22%3A%22ByBit%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgxOTA2YzRiMTM2ZDMtMDViY2NkZWM3OWE0ZDY0LTI2MDIxYTUxLTIwNzM2MDAtMTgxOTA2YzRiMTRmOWQiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIyOTA1MzU1MCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2229053550%22%7D%2C%22%24device_id%22%3A%2218176b3966099d-013e28086d90544-26021b51-2073600-18176b39661c5f%22%7D; _abck=151B93ADCDB71FB9A71F83CBD3A36DA1~0~YAAQHBvQF/8ale2BAQAArpm/AQhvWGczNob5oj9meDnPLrw8WzuBcfMEhz69TezjuKSZ53PoH47++Qxw0g0GhyPkaJbs2FjhMekb6YgiKP9oDJ+PilMV00Ew1598uliZzkNdmFzn6Z/GXZzbVtYHIL3hldhmofSBQbL3AcMg0C6An1nQv1YXNWb3EYfrZCTszcMh4CTsu9x18/BfZHf6KdGSfAlatCP0RkNo/Yr7UyXUnSwUhpSYpugb92rKrI/QPiQUXY0WuX2b/hR+IS9bM0O1le+UbjtOv047EGmTiMIE8fPRlZhb9bMEVDPB/RhnhEMRrCxrnHpCMGjHKbgMIRzIVQx3iMooS1Lzp9g/ZA8opKjRIF/NUClU/9bUGAlaWv5DcmIBHTWt8EuwgcKForYQk53NCJ8=~-1~-1~-1; bm_sz=D28AD97883486B4677EF6DDCC989C15B~YAAQHBvQFwIble2BAQAArpm/ARAFs9KKNbQja2ySPkq2XItvR2Q9LpLA73aH1t6hZj5Ujpv2tZwtTt7WIId7A3oA8DaAzhYSgHd9y/+o0H9H4Z9xA2Wm50ORnefo9183vYPuEpi4ToRQBs8AhHslo6U3HU7YqwGA8M1aYOkxi4qzKe2z0SyVvySExOgSBlfquqjt1RE5Wt+dw5p9+H4BIa3vTznBjlfkK1z2e2VVKMAiPHx09Vm06Jn0zoi2rOmoqE8wr/T5HuxDaw1wdlIAwk0dC0jqdIlT//PPOYhYgwHOCA==~3225669~4277058; bm_mi=70BE2C4889AAD58182528F4B0C3803A6~YAAQHBvQFwoble2BAQAAna2/ARC7MOcAahcQUqiOtjwwHq0155nM8g1UoyAiP2a57ohcWQ+pr2whSPcPI4eVoWMs52I1own9MtTnH9qbJaGQJ615cUpvKLlVmWCiKsTqBIuq+cXtQ0PEc0B7bN+AxUM5wHAEpRO8QaSNk1wlDSdCLl6FWKli31DK9br+kAgFwsSDPmhIJSHiiZaygYtB5LJoUdOKgO1O0ECXl+VeeV2ceRYOrlpRdxL8CDvY8EicvAKbLkFgQHM1+dxLCHthLpgff43CiZGpoYd1f4vmbedMKgGFYGqvJ7Jygyg49J7c9NTt20rh3zDITdZVjt+ey1k8mL2H+PT+SCMC5i9f4Y2Y0iQ=~1; ak_bmsc=D7822D86BFF4CE4CF6074BF6B69B9FFA~000000000000000000000000000000~YAAQHBvQFxQble2BAQAAg7G/ARBDdojfJsqCGjiDySZtZcEUJrbXtxtNNwpteRGOo9orLNZB++/aZEewWj2U+vkJmrDtOIO0o74Pi8Rnqr1DM0x7RvNIlif3nODIEoMA/eh5MY1k7A/iH59XDX8Vz+0MIabsvUz+44nyQOsY9H1P/IqNffIj8Y8Tv7l1FmLFN+ikVPMcNPUWAMkFdfrzpdrY66P36C292/I5B+XG5sa5Y1qXaK3C/XCxRdUMShRCwAxRhZSXakZJ0BJDY7ejWtJ0O2ftQkUdY8Hh0ZuKruIioXfooPayubk91cRwNV0LX7RJoHgyhAcyvMnMmsAwgMIAwjDeoV2ogSENk98l0yDbbhwf2DhAu5zo2y2YUhgPlGydZjcCm2/9uTpycJBuXT/Z+OMRgkFm+ByV4txtjtr6TWPA3dASnJ0SUsvjtKa0gZkpBN2yok3JQmL41cAwJNBTATGUJSl3cwMIyBfltJqZff+DsSxOoViI5r5tDmdwPWu76lAucPdvHUbFy/njLLYB/kI1eU4MexjXK8LBL1io1FEJEdA=; _gid=GA1.2.1807190412.1657886726; _ym_isad=1; RT="z=1&dm=bybit.com&si=ceb7429c-4b86-4ca5-9667-4481257c256f&ss=l5mexwte&sl=1&tt=jbn&rl=1&ld=jbt&ul=29oc&hd=29og"; bm_sv=5062A0FD6BE8FAB084A5FAA532154992~YAAQHBvQFwgcle2BAQAAyUvBARBShKrcD2tQnTYO7rwVw8EzQPhWDcu2Vbbx1Y2iBR9u+aKz9+V97nwRFTy0kni00hbqXxFF44w1DTvpQkRdNSjbvfBZCvfhKFhohtHhIdf3DVa2Hggp7y/zVMRP2CyEQCJFojR7zxT8c3tS7Zgu9BIXTL1txhTweMmAGs87Z9Ahq5v1FHEGYY6j5i+bysk7ua4k85G7v9EyDtr/btPXGHjJDdRC+cI2jRupDJng~1; tmr_reqNum=55; _gat_UA-126371352-1=1',
            'guid': 'bc291a57-d12c-0324-7580-b481e54e4edb',
            'lang': 'en-US',
            'origin': 'https://www.bybit.com',
            'platform': 'PC',
            'referer': 'https://www.bybit.com/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }

        self.data = {
            'userId': '',
            'tokenId': kwargs.get('tokenId'),
            'currencyId': kwargs.get('currencyId'),
            'payment': kwargs.get('payment'),
            'side': kwargs.get('side'),
            'size': '10',
            'page': '1',
            # 'amount': kwargs.get('amount'),
        }

        self.url = 'https://api2.bybit.com/spot/api/otc/item/list'
        self.side = sides[self.data['side']]
        self.fiat = payments[self.data["payment"]]
        self.crypto = self.data["tokenId"]

    async def price(self, session):

        try:
            async with session.post(url=self.url, headers=self.headers, data=self.data) as response:
                data = await response.json()
                min_price = float(data['result']['items'][0]['price'])
                answer = []
                for j in range(len(limits)):
                    for i in range(min(5, len(data['result']['items']))):
                        if float(data['result']['items'][i]['minAmount']) >= limits[j] and float(data['result']['items'][i]['minAmount']) <= limits[min((j+1), (len(limits)-1))]:
                            if float(data['result']['items'][i]['recentExecuteRate']) > 85 and float(data['result']['items'][i]['price']) < (min_price * 1.05):
                                answer.append((self.side, self.fiat, self.crypto, float(data['result']['items'][i]['price']), \
                                       float(data['result']['items'][i]['minAmount']), \
                                       (float(data['result']['items'][i]['lastQuantity']) * float(data['result']['items'][i]['price'])), 'Bybit'))
                        else:
                            continue
                return answer

        except Exception:
            return self.side, self.fiat, self.crypto, 0, 0, 0, 'Bybit'

