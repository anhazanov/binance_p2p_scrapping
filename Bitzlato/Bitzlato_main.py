import asyncio

from Bitzlato.Bitzlato_p2p_price import Bitzlato_p2p_data
from Bitzlato.Bitzlato_spot_price import Bitzlato_spot_price
from Bitzlato.Bitzlto_config import *
from main_config import limits

async def get_p2p_price(session):
    # spot = Bitzlato_p2p_data()
    # await spot.price(session)


    tasks = []
    for side in sides.keys():
        for payment in payments.keys():
            for crypto in crypto_values:
                for limit in limits:
                    tasks.append(Bitzlato_p2p_data(cryptocurrency=crypto, currency='RUB', paymethod=payment, amount=limit,
                                                paymethodSlug=payments[payment].lower(),type=side).price(session))

    answer_p2p = list(set(await asyncio.gather(*tasks)))
    return answer_p2p

async def get_spot_price(session):
    pair_price = Bitzlato_spot_price()
    price = await pair_price.price()

    # Huobi_spot = {}
    # for el in price:
    #     Huobi_spot[el[0]] = {}
    # for el in price:
    #     Huobi_spot[el[0]][el[1]] = el[2]
    # return Huobi_spot

async def bitzlato_main(session):

    # Bitzlto_spot = await get_spot_price(session)
    Bitzlto_p2p = await get_p2p_price(session)


    return Bitzlto_p2p