import aiohttp
import asyncio

from Binance.Binance_p2p_price import Binance_p2p_price
from Binance.Binance_spot_price import Binance_spot_price
from Binance.Binance_config import *
from main_config import limits


async def get_p2p_price(session, value):
    tasks = []
    for side in ('SELL', 'BUY'):
        for payment in payments[value].keys():
            for crypto in crypto_values[value]:
                for limit in (0, 1000):
                    tasks.append(Binance_p2p_price(fiat=value, asset=crypto, tradeType=side,
                                                  payTypes=[payment],
                                                    transAmount=limit
                                                    ).price(session))
    answer_p2p = await asyncio.gather(*tasks)
    new_answer = []
    for el in answer_p2p:
        for item in el:
            if item not in new_answer:
                new_answer.append(item)

    return new_answer


async def get_spot_price(session):
    price_pair = Binance_spot_price()
    binance_spot = await price_pair.price(session)
    return binance_spot


async def Binance_main(session, value):
    print('Сбор Р2Р Бинанс. Занимает до 1 минуты...')
    binance_p2p = await get_p2p_price(session, value)
    binance_spot = await get_spot_price(session)

    return binance_p2p, binance_spot