import asyncio

from Huobi.Huobi_p2p_price import Huobi_p2p_data
from Huobi.Huobi_spot_price import Huobi_spot_price
from Huobi.Huobi_config import *
from main_config import limits

async def get_p2p_price(session):
    tasks = []

    for side in ['sell', 'buy']:
        for payment in payments.keys():
            for crypto in crypto_values.keys():
                # for limit in limits:
                tasks.append(Huobi_p2p_data(coinId=crypto, currency=fiat['RUB'], payMethod=payment,
                                                tradeType=side,).price(session))

    answer_p2p = await asyncio.gather(*tasks)
    new_answer = []
    for el in answer_p2p:
        if el != None:
            for item in el:
                if item not in new_answer and item != None:
                    new_answer.append(item)
    return new_answer

async def get_spot_price(session):
    pair_price = Huobi_spot_price()
    huobi_spot = await pair_price.get_pair()
    return huobi_spot

async def huobi_main(session):

    huobi_spot = await get_spot_price(session)
    print('Сбор данных на P2P Huobi занимает до 1 минуты...')
    huobi_p2p = await get_p2p_price(session)

    return huobi_p2p, huobi_spot