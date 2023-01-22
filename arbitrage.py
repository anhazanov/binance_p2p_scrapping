from comission import comission, spot_comission
from db import Database

async def arbitrage_buy(p2p_total_buy, spot_total, p2p_total_sell):

    all_trades = []

    start_balance = 20_000

    db_arbitrage = Database()

    db_data = []

    for key1 in p2p_total_buy.keys():
        for k1, v1 in p2p_total_buy[key1].items():
            if v1 != 0:
                current_balance1 = start_balance / v1
            else:
                current_balance1 = 0
            currency1 = k1.split("-")[0]
            position1 = key1.split("-")[-1]
            start_currency = key1.split("-")[0]
            exchange_path1 = f'1. На бирже {position1} как ТЕЙКЕР за {start_currency} ' \
                             f'покупаем {currency1} по курсу {v1}.\n'

            for value_1 in comission.keys():
                if value_1.split('-')[-1] == position1 and value_1.split('-')[0] == currency1:
                    for v_in_1, k_in_1 in comission[value_1].items():
                        for value_2 in comission.keys():
                            if value_2.split('-')[-1] != position1 and value_2.split('-')[0] == currency1:
                                for v_in_2 in comission[value_2].keys():
                                    if v_in_1 == v_in_2:
                                        position2 = value_2.split('-')[-1]
                                        currency2 = currency1
                                        current_balance2 = current_balance1 - k_in_1
                                        exchange_path2 = exchange_path1 + f'2. Переводим наши {currency1} с биржы {position1} на биржу {position2}' \
                                                         f' через сеть {v_in_1} с комиссией {k_in_1}.\n'

                                        for key3 in p2p_total_buy.keys():
                                            for k3, v3 in p2p_total_buy[key3].items():
                                                if k3.split('-')[0] == currency2 and k3.split('-')[-1] == position2:
                                                    current_balance3 = current_balance2 * v3
                                                    position3 = position2
                                                    currency3 = key3.split("-")[0]
                                                    exchange_path3 = exchange_path2 + f'3. На бирже {position2} как МЕЙКЕР продаем наши {currency2} за ' \
                                                                     f'{currency3} по курсу {v3}.\n'
                                                    profit = round((current_balance3 - start_balance)/start_balance*100, 2)
                                                    all_trades.append([currency1, f'С {start_currency}-{position1} на {currency3}-{position3}',
                                                                       f'{currency1}>{currency1}', round(profit, 2), exchange_path3])
                                                    if profit > 0:
                                                        db_data.append((profit, position1, position3, start_currency,
                                                                        currency3,
                                                                        f'{currency1}>{currency2}',
                                                                        'тейкер-мейкер', exchange_path3))
                                        for key4 in p2p_total_sell.keys():
                                            for k4, v4 in p2p_total_sell[key4].items():
                                                if k4.split('-')[0] == currency2 and k4.split('-')[-1] == position2:
                                                    current_balance4 = current_balance2 * v4
                                                    position4 = position2
                                                    currency4 = key4.split("-")[0]
                                                    exchange_path4 = exchange_path2 + f'3. На бирже {position2} как ТЕЙКЕР продаем наши {currency2} за ' \
                                                                     f'{currency4} по курсу {v4}.\n'
                                                    profit = round((current_balance4 - start_balance)/start_balance*100, 2)
                                                    all_trades.append([currency1, f'С {start_currency}-{position1} на {currency4}-{position4}',
                                                                       f'{currency1}>{currency1}', round(profit, 2), exchange_path4])
                                                    if profit > 0:
                                                        db_data.append((profit, position1, position4, start_currency,
                                                                        currency4,
                                                                        f'{currency1}>{currency2}',
                                                                        'тейкер-тейкер', exchange_path4))

# 1 обмен на споте первой биржи
    for key1 in p2p_total_buy.keys():
        for k1, v1 in p2p_total_buy[key1].items():
            if v1 != 0:
                current_balance1 = start_balance / v1
            else:
                current_balance1 = 0
            currency1 = k1.split("-")[0]
            position1 = key1.split("-")[-1]
            start_currency = key1.split("-")[0]
            exchange_path1 = f'1. На бирже {position1} как ТЕЙКЕР за {start_currency} ' \
                             f'покупаем {currency1} по курсу {v1}.\n'

            for key2 in spot_total.keys():
                for k2, v2 in spot_total[key2].items():
                    if key2.split('-')[0] == currency1 and key2.split('-')[-1] == position1:
                        if v2 != 0:
                            current_balance2 = current_balance1 / v2 * (1 - spot_comission[position1])
                        else:
                            current_balance2 = 0
                        currency2 = k2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    elif k2.split('-')[0] == currency1 and k2.split('-')[-1] == position1:
                        current_balance2 = current_balance1 * v2 * (1 - spot_comission[position1])
                        currency2 = key2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    else:
                        break

                    for value_1 in comission.keys():
                        if value_1.split('-')[-1] == position2 and value_1.split('-')[0] == currency2:
                            for v_in_1, k_in_1 in comission[value_1].items():
                                for value_2 in comission.keys():
                                    if value_2.split('-')[-1] != position2 and value_2.split('-')[0] == currency2:
                                        for v_in_2 in comission[value_2].keys():
                                            if v_in_1 == v_in_2:
                                                position3 = value_2.split('-')[-1]
                                                currency3 = currency2
                                                current_balance3 = current_balance2 - k_in_1
                                                exchange_path3 = exchange_path2 + f'3. Переводим наши {currency2} с биржы {position2} на биржу {position3}' \
                                                                 f' через сеть {v_in_1} с комиссией {k_in_1}.\n'

                                                for key4 in p2p_total_buy.keys():
                                                    for k4, v4 in p2p_total_buy[key4].items():
                                                        if k4.split('-')[0] == currency3 and k4.split('-')[-1] == position3:
                                                            current_balance4 = current_balance3 * v4
                                                            position4 = position3
                                                            currency4 = key4.split("-")[0]
                                                            exchange_path4 = exchange_path3 + f'4. На бирже {position3} как МЕЙКЕР продаем наши {currency3} за ' \
                                                                             f'{currency4} по курсу {v4}.\n'
                                                            profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                                                            all_trades.append([currency2, f'С {start_currency}-{position1} на {currency4}-{position4}',
                                                                               f'{currency1}>{currency2}>{currency3}', round(profit, 2), exchange_path4])
                                                            if profit > 0:
                                                                db_data.append((profit, position1, position4, start_currency, currency4, f'{currency1}>{currency2}>{currency3}',
                                                                                'тейкер-мейкер', exchange_path4))

                                                for key5 in p2p_total_sell.keys():
                                                    for k5, v5 in p2p_total_sell[key5].items():
                                                        if k5.split('-')[0] == currency3 and k5.split('-')[-1] == position3:
                                                            current_balance5 = current_balance3 * v5
                                                            position5 = position3
                                                            currency5 = key5.split("-")[0]
                                                            exchange_path5 = exchange_path3 + f'4. На бирже {position3} как ТЕЙКЕР продаем наши {currency3} за ' \
                                                                             f'{currency5} по курсу {v5}.\n'
                                                            profit = round((current_balance5 - start_balance) / start_balance * 100, 2)
                                                            all_trades.append([currency2, f'С {start_currency}-{position1} на {currency5}-{position5}',
                                                                               f'{currency1}>{currency2}>{currency3}', round(profit, 2), exchange_path5])
                                                            if profit > 0:
                                                                db_data.append((
                                                                               profit, position1, position5, start_currency,
                                                                               currency5,
                                                                               f'{currency1}>{currency2}>{currency3}',
                                                                               'тейкер-тейкер', exchange_path5))

    # 1 обмен на споте второй биржи
    for key1 in p2p_total_buy.keys():
        for k1, v1 in p2p_total_buy[key1].items():
            if v1 != 0:
                current_balance1 = start_balance / v1
            else:
                current_balance1 = 0
            currency1 = k1.split("-")[0]
            position1 = key1.split("-")[-1]
            start_currency = key1.split("-")[0]
            exchange_path1 = f'1. На бирже {position1} как ТЕЙКЕР за {start_currency} ' \
                             f'покупаем {currency1} по курсу {v1}.\n'

            for value_1 in comission.keys():
                if value_1.split('-')[-1] == position1 and value_1.split('-')[0] == currency1:
                    for v_in_1, k_in_1 in comission[value_1].items():
                        for value_2 in comission.keys():
                            if value_2.split('-')[-1] != position1 and value_2.split('-')[0] == currency1:
                                for v_in_2 in comission[value_2].keys():
                                    if v_in_1 == v_in_2:
                                        position2 = value_2.split('-')[-1]
                                        currency2 = currency1
                                        current_balance2 = current_balance1 - k_in_1
                                        exchange_path2 = exchange_path1 + f'2. Переводим наши {currency1} с биржы {position1} на биржу {position2}' \
                                                         f' через сеть {v_in_1} с комиссией {k_in_1}.\n'

                                        for key3 in spot_total.keys():
                                            for k3, v3 in spot_total[key3].items():
                                                if key3.split('-')[0] == currency2 and key3.split('-')[-1] == position2:
                                                    if v3 != 0:
                                                        current_balance3 = current_balance2 / v3 * (
                                                                    1 - spot_comission[position2])
                                                    else:
                                                        current_balance3 = 0
                                                    currency3 = k3.split('-')[0]
                                                    position3 = position2
                                                    exchange_path3 = exchange_path2 + f'3. Наши {currency2} на споте меняем на {currency3} по курсу {v3}.\n'
                                                elif k3.split('-')[0] == currency2 and k3.split('-')[-1] == position2:
                                                    current_balance3 = current_balance2 * v3 * (
                                                                1 - spot_comission[position2])
                                                    currency3 = key3.split('-')[0]
                                                    position3 = position2
                                                    exchange_path3 = exchange_path2 + f'3. Наши {currency2} на споте меняем на {currency3} по курсу {v3}.\n'
                                                else:
                                                    break


                                                for key4 in p2p_total_buy.keys():
                                                    for k4, v4 in p2p_total_buy[key4].items():
                                                        if k4.split('-')[0] == currency3 and k4.split('-')[-1] == position3:
                                                            current_balance4 = current_balance3 * v4
                                                            position4 = position3
                                                            currency4 = key4.split("-")[0]
                                                            exchange_path4 = exchange_path3 + f'4. На бирже {position3} как МЕЙКЕР продаем наши {currency3} за ' \
                                                                             f'{currency4} по курсу {v4}.\n'
                                                            profit = round((current_balance4 - start_balance)/start_balance*100, 2)
                                                            all_trades.append([currency1, f'С {start_currency}-{position1} на {currency4}-{position4}',
                                                                               f'{currency1}>{currency2}>{currency3}', round(profit, 2), exchange_path4])
                                                            if profit > 0:
                                                                db_data.append((profit, position1, position4,
                                                                                start_currency, currency4,
                                                                                f'{currency1}>{currency2}>{currency3}',
                                                                                'тейкер-мейкер', exchange_path4))
                                                for key5 in p2p_total_sell.keys():
                                                    for k5, v5 in p2p_total_sell[key5].items():
                                                        if k5.split('-')[0] == currency3 and k5.split('-')[-1] == position3:
                                                            current_balance5 = current_balance3 * v5
                                                            position5 = position3
                                                            currency5 = key5.split("-")[0]
                                                            exchange_path5 = exchange_path3 + f'4. На бирже {position3} как ТЕЙКЕР продаем наши {currency3} за ' \
                                                                             f'{currency5} по курсу {v5}.\n'
                                                            profit = round((current_balance5 - start_balance)/start_balance*100, 2)
                                                            all_trades.append([currency1, f'С {start_currency}-{position1} на {currency5}-{position5}',
                                                                               f'{currency1}>{currency2}>{currency3}', round(profit, 2), exchange_path5])
                                                            if profit > 0:
                                                                db_data.append((
                                                                    profit, position1, position5, start_currency,
                                                                    currency5,
                                                                    f'{currency1}>{currency2}>{currency3}',
                                                                    'тейкер-тейкер', exchange_path5))


    # 2 обменa на споте на обоих биржах
    for key1 in p2p_total_buy.keys():
        for k1, v1 in p2p_total_buy[key1].items():
            if v1 != 0:
                current_balance1 = start_balance / v1
            else:
                current_balance1 = 0
            currency1 = k1.split("-")[0]
            position1 = key1.split("-")[-1]
            start_currency = key1.split("-")[0]
            exchange_path1 = f'1. На бирже {position1} как ТЕЙКЕР за {start_currency} ' \
                             f'покупаем {currency1} по курсу {v1}.\n'

            for key2 in spot_total.keys():
                for k2, v2 in spot_total[key2].items():
                    if key2.split('-')[0] == currency1 and key2.split('-')[-1] == position1:
                        if v2 != 0:
                            current_balance2 = current_balance1 / v2 * (1 - spot_comission[position1])
                        else:
                            current_balance2 = 0
                        currency2 = k2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    elif k2.split('-')[0] == currency1 and k2.split('-')[-1] == position1:
                        current_balance2 = current_balance1 * v2 * (1 - spot_comission[position1])
                        currency2 = key2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    else:
                        break

                    for value_1 in comission.keys():
                        if value_1.split('-')[-1] == position2 and value_1.split('-')[0] == currency2:
                            for v_in_1, k_in_1 in comission[value_1].items():
                                for value_2 in comission.keys():
                                    if value_2.split('-')[-1] != position2 and value_2.split('-')[0] == currency2:
                                        for v_in_2 in comission[value_2].keys():
                                            if v_in_1 == v_in_2:
                                                position3 = value_2.split('-')[-1]
                                                currency3 = currency2
                                                current_balance3 = current_balance2 - k_in_1
                                                exchange_path3 = exchange_path2 + f'3. Переводим наши {currency2} с биржы {position2} на биржу {position3}' \
                                                                 f' через сеть {v_in_1} с комиссией {k_in_1}.\n'

                                                for key4 in spot_total.keys():
                                                    for k4, v4 in spot_total[key4].items():
                                                        if key4.split('-')[0] == currency3 and key4.split('-')[
                                                            -1] == position3:
                                                            if v4 != 0:
                                                                current_balance4 = current_balance3 / v4 * (
                                                                        1 - spot_comission[position3])
                                                            else:
                                                                current_balance4 = 0
                                                            currency4 = k4.split('-')[0]
                                                            position4 = position3
                                                            exchange_path4 = exchange_path3 + f'4. Наши {currency3} на споте меняем на {currency4} по курсу {v4}.\n'
                                                        elif k4.split('-')[0] == currency3 and k4.split('-')[-1] == position3:
                                                            current_balance4 = current_balance3 * v4 * (
                                                                    1 - spot_comission[position3])
                                                            currency4 = key4.split('-')[0]
                                                            position4 = position3
                                                            exchange_path4 = exchange_path3 + f'4. Наши {currency3} на споте меняем на {currency4} по курсу {v4}.\n'
                                                        else:
                                                            break

                                                        for key5 in p2p_total_buy.keys():
                                                            for k5, v5 in p2p_total_buy[key5].items():
                                                                if k5.split('-')[0] == currency4 and k5.split('-')[-1] == position4:
                                                                    current_balance5 = current_balance4 * v5
                                                                    position5 = position4
                                                                    currency5 = key5.split("-")[0]
                                                                    exchange_path5 = exchange_path4 + f'5. На бирже {position5} как МЕЙКЕР продаем наши {currency4} за ' \
                                                                                                      f'{currency5} по курсу {v5}.\n'
                                                                    profit = round((current_balance5 - start_balance) / start_balance * 100, 2)
                                                                    all_trades.append([currency2,
                                                                                       f'С {start_currency}-{position1} на {currency5}-{position5}',
                                                                                       f'{currency1}>{currency2}>{currency3}>{currency4}',
                                                                                       round(profit, 2), exchange_path5])
                                                                    if profit > 0:
                                                                        db_data.append((profit, position1, position5,
                                                                                        start_currency, currency5,
                                                                                        f'{currency1}>{currency2}>{currency3}>{currency4}',
                                                                                        'тейкер-мейкер', exchange_path5))

                                                        for key6 in p2p_total_sell.keys():
                                                            for k6, v6 in p2p_total_sell[key6].items():
                                                                if k6.split('-')[0] == currency4 and k6.split('-')[-1] == position4:
                                                                    current_balance6 = current_balance4 * v6
                                                                    position6 = position4
                                                                    currency6 = key6.split("-")[0]
                                                                    exchange_path6 = exchange_path4 + f'5. На бирже {position6} как ТЕЙКЕР продаем наши {currency4} за ' \
                                                                                                      f'{currency6} по курсу {v6}.\n'
                                                                    profit = round((current_balance6 - start_balance) / start_balance * 100, 2)
                                                                    all_trades.append([currency2,
                                                                                       f'С {start_currency}-{position1} на {currency6}-{position6}',
                                                                                       f'{currency1}>{currency2}>{currency3}>{currency4}',
                                                                                       round(profit, 2), exchange_path6])
                                                                    if profit > 0:
                                                                        db_data.append((profit, position1, position6,
                                                                                        start_currency, currency6,
                                                                                        f'{currency1}>{currency2}>{currency3}>{currency4}',
                                                                                        'тейкер-тейкер', exchange_path6))

    # Внутрибиржевые связки
    for key1 in p2p_total_buy.keys():
        for k1, v1 in p2p_total_buy[key1].items():
            if v1 != 0:
                current_balance1 = start_balance / v1
            else:
                current_balance1 = 0
            currency1 = k1.split("-")[0]
            position1 = key1.split("-")[-1]
            start_currency = key1.split("-")[0]
            exchange_path1 = f'1. На бирже {position1} как ТЕЙКЕР за {start_currency} ' \
                             f'покупаем {currency1} по курсу {v1}.\n'

            for key2 in spot_total.keys():
                for k2, v2 in spot_total[key2].items():
                    if key2.split('-')[0] == currency1 and key2.split('-')[-1] == position1:
                        if v2 != 0:
                            current_balance2 = current_balance1 / v2 * (1 - spot_comission[position1])
                        else:
                            current_balance2 = 0
                        currency2 = k2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    elif k2.split('-')[0] == currency1 and k2.split('-')[-1] == position1:
                        current_balance2 = current_balance1 * v2 * (1 - spot_comission[position1])
                        currency2 = key2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    else:
                        break

                    for key4 in p2p_total_buy.keys():
                        for k4, v4 in p2p_total_buy[key4].items():
                            if k4.split('-')[0] == currency2 and k4.split('-')[-1] == position2:
                                current_balance4 = current_balance2 * v4
                                position4 = position2
                                currency4 = key4.split("-")[0]
                                exchange_path4 = exchange_path2 + f'3. На бирже {position2} как МЕЙКЕР продаем наши {currency2} за ' \
                                                 f'{currency4} по курсу {v4}.\n'
                                profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                                all_trades.append([currency2, f'С {start_currency}-{position1} на {currency4}-{position4}',
                                                   f'{currency1}>{currency2}', round(profit, 2), exchange_path4])
                                if profit > 0:
                                    db_data.append((profit, position1, position4, start_currency, currency4, f'{currency1}>{currency2}',
                                                    'тейкер-мейкер', exchange_path4))

                    for key5 in p2p_total_sell.keys():
                        for k5, v5 in p2p_total_sell[key5].items():
                            if k5.split('-')[0] == currency2 and k5.split('-')[-1] == position2:
                                current_balance5 = current_balance2 * v5
                                position5 = position2
                                currency5 = key5.split("-")[0]
                                exchange_path5 = exchange_path2 + f'3. На бирже {position2} как ТЕЙКЕР продаем наши {currency2} за ' \
                                                 f'{currency5} по курсу {v5}.\n'
                                profit = round((current_balance5 - start_balance) / start_balance * 100, 2)
                                all_trades.append([currency2, f'С {start_currency}-{position1} на {currency5}-{position5}',
                                                   f'{currency1}>{currency2}', round(profit, 2), exchange_path5])
                                if profit > 0:
                                    db_data.append((
                                                   profit, position1, position5, start_currency,
                                                   currency5,
                                                   f'{currency1}>{currency2}',
                                                   'тейкер-тейкер', exchange_path5))


    """ Start from MAKER """
    for key1 in p2p_total_sell.keys():
        for k1, v1 in p2p_total_sell[key1].items():
            if v1 != 0:
                current_balance1 = start_balance / v1
            else:
                current_balance1 = 0
            currency1 = k1.split("-")[0]
            position1 = key1.split("-")[-1]
            start_currency = key1.split("-")[0]
            exchange_path1 = f'1. На бирже {position1} как МЕЙКЕР за {start_currency} ' \
                             f'покупаем {currency1} по курсу {v1}.\n'

            for value_1 in comission.keys():
                if value_1.split('-')[-1] == position1 and value_1.split('-')[0] == currency1:
                    for v_in_1, k_in_1 in comission[value_1].items():
                        for value_2 in comission.keys():
                            if value_2.split('-')[-1] != position1 and value_2.split('-')[0] == currency1:
                                for v_in_2 in comission[value_2].keys():
                                    if v_in_1 == v_in_2:
                                        position2 = value_2.split('-')[-1]
                                        currency2 = currency1
                                        current_balance2 = current_balance1 - k_in_1
                                        exchange_path2 = exchange_path1 + f'2. Переводим наши {currency1} с биржы {position1} на биржу {position2}' \
                                                         f' через сеть {v_in_1} с комиссией {k_in_1}.\n'

                                        for key3 in p2p_total_buy.keys():
                                            for k3, v3 in p2p_total_buy[key3].items():
                                                if k3.split('-')[0] == currency2 and k3.split('-')[-1] == position2:
                                                    current_balance3 = current_balance2 * v3
                                                    position3 = position2
                                                    currency3 = key3.split("-")[0]
                                                    exchange_path3 = exchange_path2 + f'3. На бирже {position2} как МЕЙКЕР продаем наши {currency2} за ' \
                                                                     f'{currency3} по курсу {v3}.\n'
                                                    profit = round((current_balance3 - start_balance)/start_balance*100, 2)
                                                    all_trades.append([currency1, f'С {start_currency}-{position1} на {currency3}-{position3}',
                                                                       f'{currency1}>{currency1}', round(profit, 2), exchange_path3])
                                                    if profit > 0:
                                                        db_data.append((profit, position1, position3, start_currency,
                                                                        currency3,
                                                                        f'{currency1}>{currency2}',
                                                                        'мейкер-мейкер', exchange_path3))
                                        for key4 in p2p_total_sell.keys():
                                            for k4, v4 in p2p_total_sell[key4].items():
                                                if k4.split('-')[0] == currency2 and k4.split('-')[-1] == position2:
                                                    current_balance4 = current_balance2 * v4
                                                    position4 = position2
                                                    currency4 = key4.split("-")[0]
                                                    exchange_path4 = exchange_path2 + f'3. На бирже {position2} как ТЕЙКЕР продаем наши {currency2} за ' \
                                                                     f'{currency4} по курсу {v4}.\n'
                                                    profit = round((current_balance4 - start_balance)/start_balance*100, 2)
                                                    all_trades.append([currency1, f'С {start_currency}-{position1} на {currency4}-{position4}',
                                                                       f'{currency1}>{currency1}', round(profit, 2), exchange_path4])
                                                    if profit > 0:
                                                        db_data.append((profit, position1, position4, start_currency,
                                                                        currency4,
                                                                        f'{currency1}>{currency2}',
                                                                        'мейкер-тейкер', exchange_path4))

    # 1 обмен на споте первой биржи
    for key1 in p2p_total_sell.keys():
        for k1, v1 in p2p_total_sell[key1].items():
            if v1 != 0:
                current_balance1 = start_balance / v1
            else:
                current_balance1 = 0
            currency1 = k1.split("-")[0]
            position1 = key1.split("-")[-1]
            start_currency = key1.split("-")[0]
            exchange_path1 = f'1. На бирже {position1} как МЕЙКЕР за {start_currency} ' \
                             f'покупаем {currency1} по курсу {v1}.\n'

            for key2 in spot_total.keys():
                for k2, v2 in spot_total[key2].items():
                    if key2.split('-')[0] == currency1 and key2.split('-')[-1] == position1:
                        if v2 != 0:
                            current_balance2 = current_balance1 / v2 * (1 - spot_comission[position1])
                        else:
                            current_balance2 = 0
                        currency2 = k2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    elif k2.split('-')[0] == currency1 and k2.split('-')[-1] == position1:
                        current_balance2 = current_balance1 * v2 * (1 - spot_comission[position1])
                        currency2 = key2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    else:
                        break

                    for value_1 in comission.keys():
                        if value_1.split('-')[-1] == position2 and value_1.split('-')[0] == currency2:
                            for v_in_1, k_in_1 in comission[value_1].items():
                                for value_2 in comission.keys():
                                    if value_2.split('-')[-1] != position2 and value_2.split('-')[0] == currency2:
                                        for v_in_2 in comission[value_2].keys():
                                            if v_in_1 == v_in_2:
                                                position3 = value_2.split('-')[-1]
                                                currency3 = currency2
                                                current_balance3 = current_balance2 - k_in_1
                                                exchange_path3 = exchange_path2 + f'3. Переводим наши {currency2} с биржы {position2} на биржу {position3}' \
                                                                                  f' через сеть {v_in_1} с комиссией {k_in_1}.\n'

                                                for key4 in p2p_total_buy.keys():
                                                    for k4, v4 in p2p_total_buy[key4].items():
                                                        if k4.split('-')[0] == currency3 and k4.split('-')[
                                                            -1] == position3:
                                                            current_balance4 = current_balance3 * v4
                                                            position4 = position3
                                                            currency4 = key4.split("-")[0]
                                                            exchange_path4 = exchange_path3 + f'4. На бирже {position3} как МЕЙКЕР продаем наши {currency3} за ' \
                                                                                              f'{currency4} по курсу {v4}.\n'
                                                            profit = round((
                                                                                       current_balance4 - start_balance) / start_balance * 100,
                                                                           2)
                                                            all_trades.append([currency2,
                                                                               f'С {start_currency}-{position1} на {currency4}-{position4}',
                                                                               f'{currency1}>{currency2}>{currency3}',
                                                                               round(profit, 2), exchange_path4])
                                                            if profit > 0:
                                                                db_data.append((profit, position1, position4,
                                                                                start_currency, currency4,
                                                                                f'{currency1}>{currency2}>{currency3}',
                                                                                'мейкер-мейкер', exchange_path4))

                                                for key5 in p2p_total_sell.keys():
                                                    for k5, v5 in p2p_total_sell[key5].items():
                                                        if k5.split('-')[0] == currency3 and k5.split('-')[
                                                            -1] == position3:
                                                            current_balance5 = current_balance3 * v5
                                                            position5 = position3
                                                            currency5 = key5.split("-")[0]
                                                            exchange_path5 = exchange_path3 + f'4. На бирже {position3} как ТЕЙКЕР продаем наши {currency3} за ' \
                                                                                              f'{currency5} по курсу {v5}.\n'
                                                            profit = round((
                                                                                       current_balance5 - start_balance) / start_balance * 100,
                                                                           2)
                                                            all_trades.append([currency2,
                                                                               f'С {start_currency}-{position1} на {currency5}-{position5}',
                                                                               f'{currency1}>{currency2}>{currency3}',
                                                                               round(profit, 2), exchange_path5])
                                                            if profit > 0:
                                                                db_data.append((
                                                                    profit, position1, position5, start_currency,
                                                                    currency5,
                                                                    f'{currency1}>{currency2}>{currency3}',
                                                                    'мейкер-тейкер', exchange_path5))

    # 1 обмен на споте второй биржи
    for key1 in p2p_total_sell.keys():
        for k1, v1 in p2p_total_sell[key1].items():
            if v1 != 0:
                current_balance1 = start_balance / v1
            else:
                current_balance1 = 0
            currency1 = k1.split("-")[0]
            position1 = key1.split("-")[-1]
            start_currency = key1.split("-")[0]
            exchange_path1 = f'1. На бирже {position1} как МЕЙКЕР за {start_currency} ' \
                             f'покупаем {currency1} по курсу {v1}.\n'

            for value_1 in comission.keys():
                if value_1.split('-')[-1] == position1 and value_1.split('-')[0] == currency1:
                    for v_in_1, k_in_1 in comission[value_1].items():
                        for value_2 in comission.keys():
                            if value_2.split('-')[-1] != position1 and value_2.split('-')[0] == currency1:
                                for v_in_2 in comission[value_2].keys():
                                    if v_in_1 == v_in_2:
                                        position2 = value_2.split('-')[-1]
                                        currency2 = currency1
                                        current_balance2 = current_balance1 - k_in_1
                                        exchange_path2 = exchange_path1 + f'2. Переводим наши {currency1} с биржы {position1} на биржу {position2}' \
                                                                          f' через сеть {v_in_1} с комиссией {k_in_1}.\n'

                                        for key3 in spot_total.keys():
                                            for k3, v3 in spot_total[key3].items():
                                                if key3.split('-')[0] == currency2 and key3.split('-')[
                                                    -1] == position2:
                                                    if v3 != 0:
                                                        current_balance3 = current_balance2 / v3 * (
                                                                1 - spot_comission[position2])
                                                    else:
                                                        current_balance3 = 0
                                                    currency3 = k3.split('-')[0]
                                                    position3 = position2
                                                    exchange_path3 = exchange_path2 + f'3. Наши {currency2} на споте меняем на {currency3} по курсу {v3}.\n'
                                                elif k3.split('-')[0] == currency2 and k3.split('-')[
                                                    -1] == position2:
                                                    current_balance3 = current_balance2 * v3 * (
                                                            1 - spot_comission[position2])
                                                    currency3 = key3.split('-')[0]
                                                    position3 = position2
                                                    exchange_path3 = exchange_path2 + f'3. Наши {currency2} на споте меняем на {currency3} по курсу {v3}.\n'
                                                else:
                                                    break

                                                for key4 in p2p_total_buy.keys():
                                                    for k4, v4 in p2p_total_buy[key4].items():
                                                        if k4.split('-')[0] == currency3 and k4.split('-')[
                                                            -1] == position3:
                                                            current_balance4 = current_balance3 * v4
                                                            position4 = position3
                                                            currency4 = key4.split("-")[0]
                                                            exchange_path4 = exchange_path3 + f'4. На бирже {position3} как МЕЙКЕР продаем наши {currency3} за ' \
                                                                                              f'{currency4} по курсу {v4}.\n'
                                                            profit = round((
                                                                                       current_balance4 - start_balance) / start_balance * 100,
                                                                           2)
                                                            all_trades.append([currency1,
                                                                               f'С {start_currency}-{position1} на {currency4}-{position4}',
                                                                               f'{currency1}>{currency2}>{currency3}',
                                                                               round(profit, 2), exchange_path4])
                                                            if profit > 0:
                                                                db_data.append((profit, position1, position4,
                                                                                start_currency, currency4,
                                                                                f'{currency1}>{currency2}>{currency3}',
                                                                                'мейкер-мейкер', exchange_path4))
                                                for key5 in p2p_total_sell.keys():
                                                    for k5, v5 in p2p_total_sell[key5].items():
                                                        if k5.split('-')[0] == currency3 and k5.split('-')[
                                                            -1] == position3:
                                                            current_balance5 = current_balance3 * v5
                                                            position5 = position3
                                                            currency5 = key5.split("-")[0]
                                                            exchange_path5 = exchange_path3 + f'4. На бирже {position3} как ТЕЙКЕР продаем наши {currency3} за ' \
                                                                                              f'{currency5} по курсу {v5}.\n'
                                                            profit = round((
                                                                                       current_balance5 - start_balance) / start_balance * 100,
                                                                           2)
                                                            all_trades.append([currency1,
                                                                               f'С {start_currency}-{position1} на {currency5}-{position5}',
                                                                               f'{currency1}>{currency2}>{currency3}',
                                                                               round(profit, 2), exchange_path5])
                                                            if profit > 0:
                                                                db_data.append((
                                                                    profit, position1, position5, start_currency,
                                                                    currency5,
                                                                    f'{currency1}>{currency2}>{currency3}',
                                                                    'мейкер-тейкер', exchange_path5))

    # 2 обменa на споте на обоих биржах
    for key1 in p2p_total_sell.keys():
        for k1, v1 in p2p_total_sell[key1].items():
            if v1 != 0:
                current_balance1 = start_balance / v1
            else:
                current_balance1 = 0
            currency1 = k1.split("-")[0]
            position1 = key1.split("-")[-1]
            start_currency = key1.split("-")[0]
            exchange_path1 = f'1. На бирже {position1} как МЕЙКЕР за {start_currency} ' \
                             f'покупаем {currency1} по курсу {v1}.\n'

            for key2 in spot_total.keys():
                for k2, v2 in spot_total[key2].items():
                    if key2.split('-')[0] == currency1 and key2.split('-')[-1] == position1:
                        if v2 != 0:
                            current_balance2 = current_balance1 / v2 * (1 - spot_comission[position1])
                        else:
                            current_balance2 = 0
                        currency2 = k2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    elif k2.split('-')[0] == currency1 and k2.split('-')[-1] == position1:
                        current_balance2 = current_balance1 * v2 * (1 - spot_comission[position1])
                        currency2 = key2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    else:
                        break

                    for value_1 in comission.keys():
                        if value_1.split('-')[-1] == position2 and value_1.split('-')[0] == currency2:
                            for v_in_1, k_in_1 in comission[value_1].items():
                                for value_2 in comission.keys():
                                    if value_2.split('-')[-1] != position2 and value_2.split('-')[0] == currency2:
                                        for v_in_2 in comission[value_2].keys():
                                            if v_in_1 == v_in_2:
                                                position3 = value_2.split('-')[-1]
                                                currency3 = currency2
                                                current_balance3 = current_balance2 - k_in_1
                                                exchange_path3 = exchange_path2 + f'3. Переводим наши {currency2} с биржы {position2} на биржу {position3}' \
                                                                                  f' через сеть {v_in_1} с комиссией {k_in_1}.\n'

                                                for key4 in spot_total.keys():
                                                    for k4, v4 in spot_total[key4].items():
                                                        if key4.split('-')[0] == currency3 and key4.split('-')[
                                                            -1] == position3:
                                                            if v4 != 0:
                                                                current_balance4 = current_balance3 / v4 * (
                                                                        1 - spot_comission[position3])
                                                            else:
                                                                current_balance4 = 0
                                                            currency4 = k4.split('-')[0]
                                                            position4 = position3
                                                            exchange_path4 = exchange_path3 + f'4. Наши {currency3} на споте меняем на {currency4} по курсу {v4}.\n'
                                                        elif k4.split('-')[0] == currency3 and k4.split('-')[
                                                            -1] == position3:
                                                            current_balance4 = current_balance3 * v4 * (
                                                                    1 - spot_comission[position3])
                                                            currency4 = key4.split('-')[0]
                                                            position4 = position3
                                                            exchange_path4 = exchange_path3 + f'4. Наши {currency3} на споте меняем на {currency4} по курсу {v4}.\n'
                                                        else:
                                                            break

                                                        for key5 in p2p_total_buy.keys():
                                                            for k5, v5 in p2p_total_buy[key5].items():
                                                                if k5.split('-')[0] == currency4 and k5.split('-')[
                                                                    -1] == position4:
                                                                    current_balance5 = current_balance4 * v5
                                                                    position5 = position4
                                                                    currency5 = key5.split("-")[0]
                                                                    exchange_path5 = exchange_path4 + f'5. На бирже {position5} как МЕЙКЕР продаем наши {currency4} за ' \
                                                                                                      f'{currency5} по курсу {v5}.\n'
                                                                    profit = round((
                                                                                               current_balance5 - start_balance) / start_balance * 100,
                                                                                   2)
                                                                    all_trades.append([currency2,
                                                                                       f'С {start_currency}-{position1} на {currency5}-{position5}',
                                                                                       f'{currency1}>{currency2}>{currency3}>{currency4}',
                                                                                       round(profit, 2),
                                                                                       exchange_path5])
                                                                    if profit > 0:
                                                                        db_data.append((profit, position1, position5,
                                                                                        start_currency, currency5,
                                                                                        f'{currency1}>{currency2}>{currency3}>{currency4}',
                                                                                        'мейкер-мейкер', exchange_path5))

                                                        for key6 in p2p_total_sell.keys():
                                                            for k6, v6 in p2p_total_sell[key6].items():
                                                                if k6.split('-')[0] == currency4 and k6.split('-')[
                                                                    -1] == position4:
                                                                    current_balance6 = current_balance4 * v6
                                                                    position6 = position4
                                                                    currency6 = key6.split("-")[0]
                                                                    exchange_path6 = exchange_path4 + f'5. На бирже {position6} как ТЕЙКЕР продаем наши {currency4} за ' \
                                                                                                      f'{currency6} по курсу {v6}.\n'
                                                                    profit = round((
                                                                                               current_balance6 - start_balance) / start_balance * 100,
                                                                                   2)
                                                                    all_trades.append([currency2,
                                                                                       f'С {start_currency}-{position1} на {currency6}-{position6}',
                                                                                       f'{currency1}>{currency2}>{currency3}>{currency4}',
                                                                                       round(profit, 2),
                                                                                       exchange_path6])
                                                                    if profit > 0:
                                                                        db_data.append((profit, position1, position6,
                                                                                        start_currency, currency6,
                                                                                        f'{currency1}>{currency2}>{currency3}>{currency4}',
                                                                                        'мейкер-тейкер', exchange_path6))

    # Внутрибиржевые связки
    for key1 in p2p_total_sell.keys():
        for k1, v1 in p2p_total_sell[key1].items():
            if v1 != 0:
                current_balance1 = start_balance / v1
            else:
                current_balance1 = 0
            currency1 = k1.split("-")[0]
            position1 = key1.split("-")[-1]
            start_currency = key1.split("-")[0]
            exchange_path1 = f'1. На бирже {position1} как МЕЙКЕР за {start_currency} ' \
                             f'покупаем {currency1} по курсу {v1}.\n'

            for key2 in spot_total.keys():
                for k2, v2 in spot_total[key2].items():
                    if key2.split('-')[0] == currency1 and key2.split('-')[-1] == position1:
                        if v2 != 0:
                            current_balance2 = current_balance1 / v2 * (1 - spot_comission[position1])
                        else:
                            current_balance2 = 0
                        currency2 = k2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    elif k2.split('-')[0] == currency1 and k2.split('-')[-1] == position1:
                        current_balance2 = current_balance1 * v2 * (1 - spot_comission[position1])
                        currency2 = key2.split('-')[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {v2}.\n'
                    else:
                        break

                    for key4 in p2p_total_buy.keys():
                        for k4, v4 in p2p_total_buy[key4].items():
                            if k4.split('-')[0] == currency2 and k4.split('-')[-1] == position2:
                                current_balance4 = current_balance2 * v4
                                position4 = position2
                                currency4 = key4.split("-")[0]
                                exchange_path4 = exchange_path2 + f'3. На бирже {position2} как МЕЙКЕР продаем наши {currency2} за ' \
                                                                  f'{currency4} по курсу {v4}.\n'
                                profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                                all_trades.append(
                                    [currency2, f'С {start_currency}-{position1} на {currency4}-{position4}',
                                     f'{currency1}>{currency2}', round(profit, 2), exchange_path4])
                                if profit > 0:
                                    db_data.append((profit, position1, position4, start_currency, currency4,
                                                    f'{currency1}>{currency2}',
                                                    'мейкер-мейкер', exchange_path4))

                    for key5 in p2p_total_sell.keys():
                        for k5, v5 in p2p_total_sell[key5].items():
                            if k5.split('-')[0] == currency2 and k5.split('-')[-1] == position2:
                                current_balance5 = current_balance2 * v5
                                position5 = position2
                                currency5 = key5.split("-")[0]
                                exchange_path5 = exchange_path2 + f'3. На бирже {position2} как ТЕЙКЕР продаем наши {currency2} за ' \
                                                                  f'{currency5} по курсу {v5}.\n'
                                profit = round((current_balance5 - start_balance) / start_balance * 100, 2)
                                all_trades.append(
                                    [currency2, f'С {start_currency}-{position1} на {currency5}-{position5}',
                                     f'{currency1}>{currency2}', round(profit, 2), exchange_path5])
                                if profit > 0:
                                    db_data.append((
                                        profit, position1, position5, start_currency,
                                        currency5,
                                        f'{currency1}>{currency2}',
                                        'мейкер-тейкер', exchange_path5))

    # best_trades = sorted(list(filter(lambda el: el if el[-2] > 0 and el[-2] < 20 else None, all_trades)), key=lambda x: x[-2], reverse=True)
    # for el in best_trades[:5]:
    #     print(*el, sep='\n')
    #     print()
    print('Очистка БД')
    db_arbitrage.clear_table()
    print('Запись новых данных в БД')
    db_arbitrage.add_trade(db_data)
    return all_trades, p2p_total_buy, p2p_total_sell
