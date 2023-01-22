import asyncio

from Bybit.bybit_p2p_price import Bybit_p2p_data
from Bybit.bybit_spot_price import Bybit_spot_price
from Bybit.bybit_config import *
from main_config import limits

async def get_p2p_price(session):
    tasks = []
    for side in sides.keys():
        for payment in payments.keys():
            for crypto in crypto_values:
                tasks.append(Bybit_p2p_data(tokenId=crypto, currencyId='RUB', payment=payment,
                                            side=side).price(session))


    answer_p2p = await asyncio.gather(*tasks)
    p2p_price = []
    for el in answer_p2p:
        for item in el:
            if item not in p2p_price:
                p2p_price.append(item)
    return p2p_price

async def get_spot_price(session):
    pairs = Bybit_spot_price()
    pair_list = await pairs.pair()

    tasks = []
    for pair in pair_list:
        tasks.append(Bybit_spot_price().price('/'.join(pair), session))

    answer = list(set(await asyncio.gather(*tasks)))
    return answer

async def bybit_main(session):
    Bybit_p2p = await get_p2p_price(session)
    Bybit_spot = await get_spot_price(session)


    return Bybit_p2p, Bybit_spot


