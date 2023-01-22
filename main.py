import asyncio
import time
import subprocess

import aiohttp


from Bybit.bybit_main import bybit_main
from Binance.Binance_main import Binance_main
from Binance.Binance_spot_price import Binance_spot_price
from OKX.OKX_main import OKX_main
from Kucoin.Kukoin_main import Kukoin_main
from Garantex.Garantex_main import Garantex_main
from Huobi.Huobi_main import huobi_main
from Bitzlato.Bitzlato_main import bitzlato_main

from app import app
from main_config import etalon_percent

from arbitrage import arbitrage_buy
from arbitrage_new import arbitrage


async def main():

    while True:

        value = 'RUB'
        p2p_total, spot_total = [], []

        async with aiohttp.ClientSession() as session:
            start_time = time.time()

            try:
                print('--> Сбор данных на бирже Binance')
                binance_p2p, binance_spot = await Binance_main(session, value)
                spot_total = spot_total + binance_spot
                p2p_total = p2p_total + binance_p2p
            except Exception as e:
                print('Binance отказался отдавать данные', e)

            """ Выбираю курсы для сортировки """
            etalon_rates = await Binance_spot_price().get_etalon_price(binance_spot)

            # try:
            #    print('--> Сбор данных на бирже Bitzlto')
            #    bitzlto_p2p = await bitzlato_main(session)
            #    p2p_total = p2p_total + bitzlto_p2p
            # except Exception:
            #    print('Bitzlto отказался отдавать данные')

            try:
                print('--> Сбор данных на бирже Huobi')
                huobi_p2p, huobi_spot = await huobi_main(session)
                spot_total = spot_total + huobi_spot
                p2p_total = p2p_total + huobi_p2p
            except Exception as e:
                print('Huobi отказался отдавать данные', e)

            try:
                print('--> Сбор данных на бирже Bybit')
                bybit_p2p, bybit_spot = await bybit_main(session)
                spot_total = spot_total + bybit_spot
                p2p_total = p2p_total + bybit_p2p
            except Exception:
                print('Bybit отказался отдавать данные')
            try:
                print('--> Сбор данных на бирже Garantex')
                garantex_p2p, garantex_spot = await Garantex_main(session)
                spot_total = spot_total + garantex_spot
                p2p_total = p2p_total + garantex_p2p
            except Exception as e:
                print('Garantex отказался отдавать данные', e)

            try:
                print('--> Сбор данных на бирже OKX')
                okx_p2p, okx_spot, = await OKX_main(session)
                spot_total = spot_total + okx_spot
                p2p_total = p2p_total + okx_p2p
            except Exception:
                print('OKX отказался отдавать данные')

            try:
                print('--> Сбор данных на бирже Kucoin')
                kucoin_p2p, kucoin_spot = await Kukoin_main(session)
                spot_total = spot_total + kucoin_spot
                p2p_total = p2p_total + kucoin_p2p
            except Exception:
                print('Kucoin отказался отдавать данные')
        print(f'Сбор данных занял! {(time.time() - start_time) / 60} минут')

        p2p_total_new = []
        for el in p2p_total:
            for item in etalon_rates:
                if (type(el) == tuple or type(el) == list) and el[2] == item[0]:
                    if el[3] < (item[2] * (1+etalon_percent)) and el[3] > (item[2] * (1-etalon_percent)):
                        p2p_total_new.append(el)
                    elif el[2] == 'HT':
                        p2p_total_new.append(el)
                    else:
                        break
        spot_total_new = [el for el in spot_total if (type(el) == tuple or type(el) == list)]
        start_time = time.time()
        print('Начало расчета связок')
        await arbitrage(p2p_total_new, spot_total_new)
        print(f'Расчет связок занял {(time.time() - start_time)/60} минут')
        print('Следующие обновление через 60 секунд')
        time.sleep(60)

if __name__ == '__main__':
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())




