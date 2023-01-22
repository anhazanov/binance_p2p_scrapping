from Garantex.Garantex_config import crypto_values
from main_config import crypto_list

async def get_pair_price(id, session):
    data = {'id': id}
    url = 'https://garantex.io/api/v2/depth'
    try:
        async with session.get(url=url, data=data) as response:
            data = await response.json()
        return data
    except Exception:
        return None

async def get_pair(session):
    url = 'https://garantex.io/api/v2/markets'
    try:
        answer = {}
        async with session.get(url=url) as response:
            data = await response.json()
            for el in data:
                if el['name'].split('/')[0] in crypto_list and el['name'].split('/')[1] in crypto_list:
                    answer[el['name']] = el['id']
        return answer
    except Exception:
        return None

class Garantex_spot_price:
    def __init__(self, **kwargs):
        self.url = 'https://garantex.io/api/v2/depth'

        self.data = {'market': kwargs.get('id')}
        self.pair = kwargs.get('name')
    async def price(self, session):
        try:

            async with session.get(url=self.url, data=self.data) as response:
                data = await response.json()
                buy_in = self.pair.split("/")[0], self.pair.split("/")[1], float(data['asks'][0]['price']), 'Garantex'

            return buy_in
        except Exception:
            return None