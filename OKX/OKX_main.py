import aiohttp
import asyncio

from OKX.OKX_p2p_price import OKX_p2p_price
from OKX.OKX_spot_price import OKX_spot_price, OKX_spot_pair
from OKX.OKX_config import *
from main_config import limits

async def get_p2p_price(session):
    tasks = []
    for side in ('sell', 'buy',):
        for payment in payments.keys():
            for crypto in crypto_values:
                for limit in limits:
                    tasks.append(OKX_p2p_price(quoteCurrency='RUB', baseCurrency=crypto, side=side,
                                                  paymentMethod=payment, quoteMinAmountPerOrder=limit).price(session))
    answer_p2p = list(set(await asyncio.gather(*tasks)))
    return answer_p2p

async def get_pair(session):
    pair = OKX_spot_pair()
    return await pair.get_pair(session)

async def get_spot_price(session):
    spot_pair = await get_pair(session)
    tasks = []
    for pair in spot_pair:
        tasks.append(OKX_spot_price(pair).price(session))
    spot_price = await asyncio.gather(*tasks)
    return spot_price

async def OKX_main(session):
    OKX_p2p = await get_p2p_price(session)
    OKX_spot = await get_spot_price(session)

    return OKX_p2p, OKX_spot