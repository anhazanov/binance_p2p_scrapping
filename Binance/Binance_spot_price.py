from main_config import crypto_list

class Binance_spot_price:
    def __init__(self):

        self.url_1 = 'https://api.binance.com/api/v3/ticker/price'
        self.url = 'https://api.binance.com/api/v3/exchangeInfo'

    async def price(self, session):
        price_pair = []
        pair_list = []
        try:
            async with session.get(url=self.url) as response:
                data = await response.json()
                for el in data['symbols']:
                    if el['baseAsset'] in crypto_list and el['quoteAsset'] in crypto_list:
                        if (el['baseAsset'] == 'USDC' and el['quoteAsset'] == 'BNB') or \
                                (el['baseAsset'] == 'DAI' and el['quoteAsset'] == 'BTC') or \
                                (el['baseAsset'] == 'DAI' and el['quoteAsset'] == 'USDT') or \
                                (el['baseAsset'] == 'DAI' and el['quoteAsset'] == 'BUSD') or \
                                (el['baseAsset'] == 'DAI' and el['quoteAsset'] == 'BNB') or \
                                (el['baseAsset'] == 'SHIB' and el['quoteAsset'] == 'RUB') or \
                                (el['baseAsset'] == 'EOS' and el['quoteAsset'] == 'RUB'):  # absurd rates from Binance
                            continue
                        else:
                            pair_list.append([el['symbol'], el['baseAsset'], el['quoteAsset']])

            async with session.get(url=self.url_1) as response:
                data = await response.json()
                for pair in pair_list:
                    for el in data:
                        if pair[0] == el['symbol']:
                            price_pair.append([pair[1], pair[2], float(el['price']), 'Binance'])
            return price_pair
        except Exception:
            return None

    async def get_etalon_price(self, binance_spot):
        etalon_price = []
        for el in binance_spot:
            if el[0] == 'USDT' and el[1] == 'RUB':
                etalon = el[2]
                etalon_price.append([el[0], el[1], el[2]])
            elif el[0] == 'RUB' or el[1] == 'RUB':
                etalon_price.append([el[0], el[1], el[2]])

        for crypto in crypto_list:
            for el in binance_spot:
                for et in etalon_price:
                    if et[0] == el[0]:
                        break
                else:
                    if el[1] == 'USDT':
                        if [el[0], 'RUB', float(el[2] * etalon)] not in etalon_price:
                            etalon_price.append([el[0], 'RUB', float(el[2] * etalon)])
        etalon_price.append(['RUB', 'RUB', 1.0])



        return etalon_price


