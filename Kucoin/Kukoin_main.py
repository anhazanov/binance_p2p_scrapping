import asyncio

import aiohttp
import asyncio

from Kucoin.Kucoin_p2p_price import Kucoin_p2p_price
from Kucoin.Kucoin_spot_price import Kucoin_spot_price
from Kucoin.Kucoin_config import *

async def get_p2p_price(session):
    tasks = []
    for side in ('SELL', 'BUY'):
        for crypto in crypto_values:
            tasks.append(Kucoin_p2p_price(legal='RUB', currency=crypto, side=side).price(session))
    answer_p2p = await asyncio.gather(*tasks)

    p2p_price = []
    for el in answer_p2p:
        for item in el:
            if item not in p2p_price:
                p2p_price.append(item)
    return p2p_price

async def get_spot_price(session):
    spot_price = Kucoin_spot_price()
    pair_price = await spot_price.get_price(session)
    return pair_price

async def Kukoin_main(session):
    Kucoin_p2p = await get_p2p_price(session)
    Kucoin_spot = await get_spot_price(session)


    return Kucoin_p2p, Kucoin_spot