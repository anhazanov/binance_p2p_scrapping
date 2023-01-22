import asyncio

from Garantex.Garantex_p2p_price import Garantex_p2p_price
from Garantex.Garantex_spot_price import Garantex_spot_price, get_pair
from Garantex.Garantex_config import crypto_values

async def get_p2p_price(session):
    # На Р2Р покупаются пополнения баланса по курсу близким к 1:1

    # tasks = []
    # for side in ('sell', 'buy'):
    #     for crypto in crypto_values:
    #         tasks.append(Garantex_p2p_price(direction='side').price(session))
    # tasks.append(Garantex_p2p_price(direction='sell').price(session))
    # answer_p2p = await asyncio.gather(*tasks)

    Garantex_p2p = [
        ('sell', 'BANK', 'RUB', 1.00, 1000, 100_000, 'Garantex'),
        ('buy', 'BANK', 'RUB', 1.00, 1000, 100_000, 'Garantex')
    ]

    return Garantex_p2p

async def get_spot_price(session):
    pair = await get_pair(session)

    tasks = []
    for name, id in pair.items():
        tasks.append(Garantex_spot_price(name=name, id=id).price(session))

    answer_p2p = await asyncio.gather(*tasks)


    return answer_p2p

async def Garantex_main(session):
    Garantex_p2p = await get_p2p_price(session)
    Garantex_spot = await get_spot_price(session)


    return Garantex_p2p, Garantex_spot