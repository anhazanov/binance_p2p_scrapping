from comission import comission, spot_comission
from db import Database


async def arbitrage(p2p_total, spot_total):
    db_arbitrage = Database()
    db_data = []

    """Начинaю как ТЕЙКЕР"""
    # без обмена на споте
    for p2p1 in p2p_total:
        if p2p1[0] == 'buy':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000*i, (max_balance // 3)*i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как ТЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'

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
                                                                              f' через сеть {v_in_1} с комиссией {k_in_1}. Баланс: {current_balance2}\n'

                                            for p2p3 in p2p_total:
                                                if p2p3[0] == 'buy' and currency2 == p2p3[2] and position2 == p2p3[-1]:
                                                    position3 = position2
                                                    currency3 = p2p3[1]
                                                    current_balance3 = current_balance2 * p2p3[3]
                                                    exchange_path3 = exchange_path2 + f'3. На бирже {position3} как МЕЙКЕР продаем наши {currency2} за ' \
                                                                                      f'{currency3} по курсу {p2p3[3]}.\n'
                                                    profit = round((current_balance3 - start_balance) / start_balance * 100, 2)
                                                    if profit > 0:
                                                        db_data.append((profit, position1, position3, start_currency, currency3,
                                                                    f'{currency1}>сеть {v_in_1}>{currency2}', 'тейкер-мейкер',
                                                                    start_balance, round(max_balance), f'{p2p1[3]}>комис. {k_in_1}>{p2p3[3]}', 'RUB', exchange_path3))

                                            for p2p4 in p2p_total:
                                                if p2p4[0] == 'sell' and currency2 == p2p4[2] and position2 == p2p4[-1] \
                                                    and ((start_balance >= p2p4[4] and start_balance <= p2p4[5]) or (p2p4[4] >= start_balance and p2p4[4] <= max_balance)):
                                                    position4 = position2
                                                    currency4 = p2p4[1]
                                                    current_balance4 = current_balance2 * p2p4[3]
                                                    exchange_path4 = exchange_path2 + f'3. На бирже {position4} как ТЕЙКЕР продаем наши {currency2} за ' \
                                                                                      f'{currency4} по курсу {p2p4[3]}.\n'
                                                    profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                                                    if p2p4[5] < max_balance:
                                                        max_balance = p2p4[5]

                                                    if profit > 0:
                                                        if p2p4[4] > start_balance:
                                                            db_data.append((
                                                                           profit, position1, position4, start_currency,
                                                                           currency4,
                                                                           f'{currency1}>сеть {v_in_1}>{currency2}', 'тейкер-тейкер',
                                                                           p2p4[4], round(max_balance), f'{p2p1[3]}>комис.{k_in_1}>{p2p4[3]}', 'RUB', exchange_path4))
                                                        else:
                                                            db_data.append((profit, position1, position4, start_currency, currency4,
                                                                    f'{currency1}>сеть {v_in_1}>{currency2}', 'тейкер-тейкер',
                                                                    start_balance, round(max_balance), f'{p2p1[3]}>комис. {k_in_1}>{p2p4[3]}', 'RUB', exchange_path4))

    # 1 обмен на 1 бирже
    for p2p1 in p2p_total:
        if p2p1[0] == 'buy':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000*i, (max_balance // 3)*i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как ТЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'

                for spot2 in spot_total:
                    if currency1 == spot2[1] and position1 == spot2[-1]:
                        if spot2[2] != 0:
                            current_balance2 = current_balance1 / spot2[2] * (1 - spot_comission[position1])
                        else:
                            continue
                        currency2 = spot2[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    elif currency1 == spot2[0] and position1 == spot2[-1]:
                        current_balance2 = current_balance1 * spot2[2] * (1 - spot_comission[position1])
                        currency2 = spot2[1]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    else:
                        continue

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
                                                                                  f' через сеть {v_in_1} с комиссией {k_in_1}. Баланс: {current_balance3}\n'

                                                for p2p4 in p2p_total:
                                                    if p2p4[0] == 'buy' and currency3 == p2p4[2] and position3 == p2p4[-1]:
                                                        position4 = position3
                                                        currency4 = p2p4[1]
                                                        current_balance4 = current_balance3 * p2p4[3]
                                                        exchange_path4 = exchange_path3 + f'4. На бирже {position4} как МЕЙКЕР продаем наши {currency3} за ' \
                                                                                          f'{currency4} по курсу {p2p4[3]}. Баланс: {current_balance4}\n'
                                                        if start_balance != 0:
                                                            profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                                                            if profit > 0:
                                                                db_data.append((profit, position1, position4, start_currency, currency4,
                                                                            f'{currency1}>спот {currency2}>сеть {v_in_1}>{currency3}', 'тейкер-мейкер',
                                                                            start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>комис. {k_in_1}>{p2p4[3]}', 'RUB', exchange_path4))

                                                for p2p5 in p2p_total:
                                                    if p2p5[0] == 'sell' and currency3 == p2p5[2] and position3 == p2p5[-1] \
                                                        and ((start_balance >= p2p5[4] and start_balance <= p2p5[5]) or (p2p5[4] >= start_balance and p2p5[4] <= max_balance)):
                                                        position5 = position3
                                                        currency5 = p2p5[1]
                                                        current_balance5 = current_balance3 * p2p5[3]
                                                        exchange_path5 = exchange_path3 + f'4. На бирже {position5} как ТЕЙКЕР продаем наши {currency3} за ' \
                                                                                          f'{currency5} по курсу {p2p5[3]}. Баланс: {current_balance5}\n'
                                                        if start_balance != 0:
                                                            profit = round((current_balance5 - start_balance) / start_balance * 100, 2)
                                                            if p2p5[5] < max_balance:
                                                                max_balance = p2p5[5]

                                                            if profit > 0:
                                                                if p2p5[4] > start_balance:
                                                                    db_data.append((profit, position1, position5,
                                                                                    start_currency, currency5,
                                                                                    f'{currency1}>спот {currency2}>сеть {v_in_1}>{currency3}',
                                                                                    'тейкер-тейкер',
                                                                                    p2p5[4],
                                                                                    round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>комис. {k_in_1}>{p2p5[3]}', 'RUB', exchange_path5))
                                                                else:
                                                                    db_data.append((profit, position1, position5, start_currency, currency5,
                                                                            f'{currency1}>спот {currency2}>сеть {v_in_1}>{currency3}', 'тейкер-тейкер',
                                                                            start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>комис. {k_in_1}>{p2p5[3]}', 'RUB', exchange_path5))
    # 1 обмен на 2 бирже
    for p2p1 in p2p_total:
        if p2p1[0] == 'buy':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000*i, (max_balance // 3)*i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как ТЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'

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
                                                                              f' через сеть {v_in_1} с комиссией {k_in_1}. Баланс: {current_balance2}\n'

                                            for spot3 in spot_total:
                                                if currency2 == spot3[1] and position2 == spot3[-1]:
                                                    if spot3[2] != 0:
                                                        current_balance3 = current_balance2 / spot3[2] * (
                                                                    1 - spot_comission[position2])
                                                    else:
                                                        continue
                                                    currency3 = spot3[0]
                                                    position3 = position2
                                                    exchange_path3 = exchange_path2 + f'3. Наши {currency2} на споте меняем на {currency3} по курсу {spot3[2]}.Баланс: {current_balance3}\n'
                                                elif currency2 == spot3[0] and position2 == spot3[-1]:
                                                    current_balance3 = current_balance2 * spot3[2] * (
                                                                1 - spot_comission[position2])
                                                    currency3 = spot3[1]
                                                    position3 = position2
                                                    exchange_path3 = exchange_path2 + f'3. Наши {currency2} на споте меняем на {currency3} по курсу {spot3[2]}.Баланс: {current_balance3}\n'
                                                else:
                                                    continue

                                                for p2p4 in p2p_total:
                                                    if p2p4[0] == 'buy' and currency3 == p2p4[2] and position3 == p2p4[-1]:
                                                        position4 = position3
                                                        currency4 = p2p4[1]
                                                        current_balance4 = current_balance3 * p2p4[3]
                                                        exchange_path4 = exchange_path3 + f'4. На бирже {position4} как МЕЙКЕР продаем наши {currency3} за ' \
                                                                                          f'{currency4} по курсу {p2p4[3]}. Баланс: {current_balance4}\n'
                                                        if start_balance != 0:
                                                            profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                                                            if profit > 0:
                                                                db_data.append((profit, position1, position4, start_currency, currency4,
                                                                            f'{currency1}>сеть{v_in_1}>спот {currency2}>{currency3}', 'тейкер-мейкер',
                                                                            start_balance, round(max_balance), f'{p2p1[3]}>комис. {k_in_1}>спот {spot3[2]}>{p2p4[3]}', 'RUB', exchange_path4))

                                                for p2p5 in p2p_total:
                                                    if p2p5[0] == 'sell' and currency3 == p2p5[2] and position3 == p2p5[-1] \
                                                        and ((start_balance >= p2p5[4] and start_balance <= p2p5[5]) or (p2p5[4] >= start_balance and p2p5[4] <= max_balance)):
                                                        position5 = position3
                                                        currency5 = p2p5[1]
                                                        current_balance5 = current_balance3 * p2p5[3]
                                                        exchange_path5 = exchange_path3 + f'4. На бирже {position5} как ТЕЙКЕР продаем наши {currency3} за ' \
                                                                                          f'{currency5} по курсу {p2p5[3]}. Баланс: {current_balance5}\n'
                                                        if start_balance != 0:
                                                            profit = round((current_balance5 - start_balance) / start_balance * 100, 2)
                                                            if p2p5[5] < max_balance:
                                                                max_balance = p2p5[5]

                                                            if profit > 0:
                                                                if p2p5[4] > start_balance:
                                                                    db_data.append((profit, position1, position5,
                                                                                    start_currency, currency5,
                                                                                    f'{currency1}>сеть {v_in_1}>спот {currency2}>{currency3}',
                                                                                    'тейкер-тейкер',
                                                                                    p2p5[4],
                                                                                    round(max_balance), f'{p2p1[3]}>комис. {k_in_1}>спот {spot3[2]}>{p2p5[3]}', 'RUB', exchange_path5))
                                                                else:
                                                                    db_data.append((profit, position1, position5, start_currency, currency5,
                                                                            f'{currency1}>сеть {v_in_1}>спот {currency2}>{currency3}', 'тейкер-тейкер',
                                                                            start_balance, round(max_balance), f'{p2p1[3]}>комис. {k_in_1}>спот {spot3[2]}>{p2p5[3]}', 'RUB', exchange_path5))
    # 2 обмена на каждой из бирж
    for p2p1 in p2p_total:
        if p2p1[0] == 'buy':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000 * i, (max_balance // 3) * i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как ТЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'

                for spot2 in spot_total:
                    if currency1 == spot2[1] and position1 == spot2[-1]:
                        if spot2[2] != 0:
                            current_balance2 = current_balance1 / spot2[2] * (1 - spot_comission[position1])
                        else:
                            continue
                        currency2 = spot2[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    elif currency1 == spot2[0] and position1 == spot2[-1]:
                        current_balance2 = current_balance1 * spot2[2] * (1 - spot_comission[position1])
                        currency2 = spot2[1]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    else:
                        continue

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
                                                                                  f' через сеть {v_in_1} с комиссией {k_in_1}. Баланс: {current_balance3}\n '

                                                for spot4 in spot_total:
                                                    if currency3 == spot4[1] and position3 == spot4[-1]:
                                                        if spot4[2] != 0:
                                                            current_balance4 = current_balance3 / spot4[2] * (
                                                                    1 - spot_comission[position3])
                                                        else:
                                                            continue
                                                        currency4 = spot4[0]
                                                        position4 = position3
                                                        exchange_path4 = exchange_path3 + f'4. Наши {currency3} на споте меняем на {currency4} по курсу {spot4[2]}.Баланс: {current_balance4}\n '
                                                    elif currency3 == spot4[0] and position3 == spot4[-1]:
                                                        current_balance4 = current_balance3 * spot4[2] * (
                                                                1 - spot_comission[position3])
                                                        currency4 = spot4[1]
                                                        position4 = position3
                                                        exchange_path4 = exchange_path3 + f'4. Наши {currency3} на споте меняем на {currency4} по курсу {spot4[2]}.Баланс: {current_balance4}\n '
                                                    else:
                                                        continue

                                                    for p2p5 in p2p_total:
                                                        if p2p5[0] == 'buy' and currency4 == p2p5[2] and position4 == p2p5[-1]:
                                                            position5 = position4
                                                            currency5 = p2p5[1]
                                                            current_balance5 = current_balance4 * p2p5[3]
                                                            exchange_path5 = exchange_path4 + f'5. На бирже {position5} как МЕЙКЕР продаем наши {currency4} за ' \
                                                                                              f'{currency5} по курсу {p2p5[3]}. Баланс: {current_balance5}\n'
                                                            if start_balance != 0:
                                                                profit = round((current_balance5 - start_balance) / start_balance * 100, 2)
                                                                if profit > 0:
                                                                    db_data.append((profit, position1, position5,
                                                                                    start_currency, currency5,
                                                                                    f'{currency1}>спот {currency2}>сеть {v_in_1}>спот {currency3}>{currency4}',
                                                                                    'тейкер-мейкер',
                                                                                    start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>комис. {k_in_1}>спот {spot4[2]}>{p2p5[3]}', 'RUB', exchange_path5))

                                                    for p2p6 in p2p_total:
                                                        if p2p6[0] == 'sell' and currency4 == p2p6[2] and position4 == p2p6[
                                                            -1] \
                                                                and ((start_balance >= p2p6[4] and start_balance <= p2p6[5]) or (p2p6[4] >= start_balance and p2p6[4] <= max_balance)):
                                                            position6 = position4
                                                            currency6 = p2p6[1]
                                                            current_balance6 = current_balance4 * p2p6[3]
                                                            exchange_path6 = exchange_path4 + f'5. На бирже {position6} как ТЕЙКЕР продаем наши {currency4} за ' \
                                                                                              f'{currency6} по курсу {p2p6[3]}. Баланс: {current_balance6}\n'
                                                            if start_balance != 0:
                                                                profit = round((current_balance6 - start_balance) / start_balance * 100, 2)
                                                                if p2p6[5] < max_balance:
                                                                    max_balance = p2p6[5]
                                                                if profit > 0:
                                                                    if p2p6[4] > start_balance:
                                                                        db_data.append((profit, position1, position6,
                                                                                        start_currency, currency6,
                                                                                        f'{currency1}>спот {currency2}>сеть {v_in_1}>спот {currency3}>{currency4}',
                                                                                        'тейкер-тейкер',
                                                                                        p2p6[4],
                                                                                        round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>комис. {k_in_1}>спот {spot4[2]}>{p2p6[3]}', 'RUB', exchange_path6))
                                                                    else:
                                                                        db_data.append((profit, position1, position6,
                                                                                    start_currency, currency6,
                                                                                    f'{currency1}>спот {currency2}>сеть {v_in_1}>спот {currency3}>{currency4}',
                                                                                    'тейкер-тейкер',
                                                                                    start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>комис. {k_in_1}>спот {spot4[2]}>{p2p6[3]}', 'RUB', exchange_path6))
    # Внутрибирж с обменом
    for p2p1 in p2p_total:
        if p2p1[0] == 'buy':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000 * i, (max_balance // 3) * i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как ТЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'

                for spot2 in spot_total:
                    if currency1 == spot2[1] and position1 == spot2[-1]:
                        if spot2[2] != 0:
                            current_balance2 = current_balance1 / spot2[2] * (1 - spot_comission[position1])
                        else:
                            continue
                        currency2 = spot2[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    elif currency1 == spot2[0] and position1 == spot2[-1]:
                        current_balance2 = current_balance1 * spot2[2] * (1 - spot_comission[position1])
                        currency2 = spot2[1]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    else:
                        continue

                    for p2p3 in p2p_total:
                        if p2p3[0] == 'buy' and currency2 == p2p3[2] and position2 == p2p3[-1]:
                            position3 = position2
                            currency3 = p2p3[1]
                            current_balance3 = current_balance2 * p2p3[3]
                            exchange_path3 = exchange_path2 + f'3. На бирже {position3} как МЕЙКЕР продаем наши {currency2} за ' \
                                                              f'{currency3} по курсу {p2p3[3]}. Баланс: {current_balance3}\n'
                            if start_balance != 0:
                                profit = round((current_balance3 - start_balance) / start_balance * 100, 2)
                                if profit > 0:
                                    db_data.append((profit, position1, position3,
                                                    start_currency, currency3,
                                                    f'{currency1}>спот>{currency2}',
                                                    'тейкер-мейкер',
                                                    start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>{p2p3[3]}', 'RUB', exchange_path3))

                    for p2p4 in p2p_total:
                        if p2p4[0] == 'sell' and currency2 == p2p4[2] and position2 == p2p4[
                            -1] and ((start_balance >= p2p4[4] and start_balance <= p2p4[5]) or (p2p4[4] >= start_balance and p2p4[4] <= max_balance)):
                            position4 = position2
                            currency4 = p2p4[1]
                            current_balance4 = current_balance2 * p2p4[3]
                            exchange_path4 = exchange_path2 + f'3. На бирже {position4} как ТЕЙКЕР продаем наши {currency2} за ' \
                                                              f'{currency4} по курсу {p2p4[3]}. Баланс: {current_balance4}\n'
                            if start_balance != 0:
                                profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                                if p2p4[5] < max_balance:
                                    max_balance = p2p4[5]
                                if profit > 0:
                                    if p2p4[4] > start_balance:
                                        db_data.append((profit, position1, position4,
                                                        start_currency, currency4,
                                                        f'{currency1}>спот>{currency2}',
                                                        'тейкер-тейкер',
                                                        p2p4[4], round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>{p2p4[3]}', 'RUB', exchange_path4))
                                    else:
                                        db_data.append((profit, position1, position4,
                                                    start_currency, currency4,
                                                    f'{currency1}>спот>{currency2}',
                                                    'тейкер-тейкер',
                                                    start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>{p2p4[3]}', 'RUB', exchange_path4))
    #Внутрибирж без обмена
    for p2p1 in p2p_total:
        if p2p1[0] == 'buy':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000 * i, (max_balance // 3) * i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как ТЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'
                # обмен на споте исключаю но порядковый номер пропускает единицу
                for p2p3 in p2p_total:
                    if p2p3[0] == 'buy' and currency1 == p2p3[2] and position1 == p2p3[-1]:
                        position3 = position1
                        currency3 = p2p3[1]
                        current_balance3 = current_balance1 * p2p3[3]
                        exchange_path3 = exchange_path1 + f'2. На бирже {position3} как МЕЙКЕР продаем наши {currency1} за ' \
                                                          f'{currency3} по курсу {p2p3[3]}. Баланс: {current_balance3}\n'
                        if start_balance != 0:
                            profit = round((current_balance3 - start_balance) / start_balance * 100, 2)
                            if profit > 0:
                                db_data.append((profit, position1, position3,
                                                start_currency, currency3,
                                                f'{currency1}',
                                                'тейкер-мейкер',
                                                start_balance, round(max_balance), f'{p2p1[3]}>{p2p3[3]}', 'RUB', exchange_path3))

                for p2p4 in p2p_total:
                    if p2p4[0] == 'sell' and currency1 == p2p4[2] and position1 == p2p4[
                        -1] and ((start_balance >= p2p4[4] and start_balance <= p2p4[5]) or (
                            p2p4[4] >= start_balance and p2p4[4] <= max_balance)):
                        position4 = position1
                        currency4 = p2p4[1]
                        current_balance4 = current_balance1 * p2p4[3]
                        exchange_path4 = exchange_path1 + f'2. На бирже {position4} как ТЕЙКЕР продаем наши {currency1} за ' \
                                                          f'{currency4} по курсу {p2p4[3]}. Баланс: {current_balance4}\n'
                        if start_balance != 0:
                            profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                            if p2p4[5] < max_balance:
                                max_balance = p2p4[5]
                            if profit > 0:
                                if p2p4[4] > start_balance:
                                    db_data.append((profit, position1, position4,
                                                    start_currency, currency4,
                                                    f'{currency1}',
                                                    'тейкер-тейкер',
                                                    p2p4[4], round(max_balance), f'{p2p1[3]}>{p2p4[3]}', 'RUB', exchange_path4))
                                else:
                                    db_data.append((profit, position1, position4,
                                                start_currency, currency4,
                                                f'{currency1}',
                                                'тейкер-тейкер',
                                                start_balance, round(max_balance), f'{p2p1[3]}>{p2p4[3]}', 'RUB', exchange_path4))


    """Начинaю как МЕЙКЕР"""
    # без обмена на споте
    for p2p1 in p2p_total:
        if p2p1[0] == 'sell':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000*i, (max_balance // 3)*i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как МЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'

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
                                                                              f' через сеть {v_in_1} с комиссией {k_in_1}. Баланс: {current_balance2}\n'

                                            for p2p3 in p2p_total:
                                                if p2p3[0] == 'buy' and currency2 == p2p3[2] and position2 == p2p3[-1] \
                                                        and max_balance > p2p3[4]:
                                                    position3 = position2
                                                    currency3 = p2p3[1]
                                                    current_balance3 = current_balance2 * p2p3[3]
                                                    exchange_path3 = exchange_path2 + f'3. На бирже {position3} как МЕЙКЕР продаем наши {currency2} за ' \
                                                                                      f'{currency3} по курсу {p2p3[3]}.\n'
                                                    profit = round((current_balance3 - start_balance) / start_balance * 100, 2)
                                                    if profit > 0:
                                                        db_data.append((profit, position1, position3, start_currency, currency3,
                                                                    f'{currency1}>сеть {v_in_1}>{currency2}', 'мейкер-мейкер',
                                                                    start_balance, round(max_balance), f'{p2p1[3]}>комис.{k_in_1}>{p2p3[3]}', 'RUB', exchange_path3))

                                            for p2p4 in p2p_total:
                                                if p2p4[0] == 'sell' and currency2 == p2p4[2] and position2 == p2p4[-1] \
                                                        and start_balance >= p2p4[4] and start_balance <= p2p4[5]:
                                                    position4 = position2
                                                    currency4 = p2p4[1]
                                                    current_balance4 = current_balance2 * p2p4[3]
                                                    exchange_path4 = exchange_path2 + f'3. На бирже {position4} как ТЕЙКЕР продаем наши {currency2} за ' \
                                                                                      f'{currency4} по курсу {p2p4[3]}.\n'
                                                    profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                                                    max_balance = p2p4[5]
                                                    if profit > 0:
                                                        db_data.append((profit, position1, position4, start_currency, currency4,
                                                                    f'{currency1}>сеть {v_in_1}>{currency2}', 'мейкер-тейкер',
                                                                    start_balance, round(max_balance), f'{p2p1[3]}>комис. {k_in_1}>{p2p4[3]}', 'RUB', exchange_path4))

    # 1 обмен на 1 бирже
    for p2p1 in p2p_total:
        if p2p1[0] == 'sell':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000*i, (max_balance // 3)*i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как МЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'

                for spot2 in spot_total:
                    if currency1 == spot2[1] and position1 == spot2[-1]:
                        if spot2[2] != 0:
                            current_balance2 = current_balance1 / spot2[2] * (1 - spot_comission[position1])
                        else:
                            continue
                        currency2 = spot2[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    elif currency1 == spot2[0] and position1 == spot2[-1]:
                        current_balance2 = current_balance1 * spot2[2] * (1 - spot_comission[position1])
                        currency2 = spot2[1]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    else:
                        continue

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
                                                                                  f' через сеть {v_in_1} с комиссией {k_in_1}. Баланс: {current_balance3}\n'

                                                for p2p4 in p2p_total:
                                                    if p2p4[0] == 'buy' and currency3 == p2p4[2] and position3 == p2p4[-1]:
                                                        position4 = position3
                                                        currency4 = p2p4[1]
                                                        current_balance4 = current_balance3 * p2p4[3]
                                                        exchange_path4 = exchange_path3 + f'4. На бирже {position4} как МЕЙКЕР продаем наши {currency3} за ' \
                                                                                          f'{currency4} по курсу {p2p4[3]}. Баланс: {current_balance4}\n'
                                                        if start_balance != 0:
                                                            profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                                                            if profit > 0:
                                                                db_data.append((profit, position1, position4, start_currency, currency4,
                                                                            f'{currency1}>спот {currency2}>сеть {v_in_1}>{currency3}', 'мейкер-мейкер',
                                                                            start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>комис. {k_in_1}>{p2p4[3]}', 'RUB', exchange_path4))

                                                for p2p5 in p2p_total:
                                                    if p2p5[0] == 'sell' and currency3 == p2p5[2] and position3 == p2p5[-1] \
                                                            and start_balance >= p2p5[4] and start_balance <= p2p5[5]:
                                                        position5 = position3
                                                        currency5 = p2p5[1]
                                                        current_balance5 = current_balance3 * p2p5[3]
                                                        exchange_path5 = exchange_path3 + f'4. На бирже {position5} как ТЕЙКЕР продаем наши {currency3} за ' \
                                                                                          f'{currency5} по курсу {p2p5[3]}. Баланс: {current_balance5}\n'
                                                        if start_balance != 0:
                                                            profit = round((current_balance5 - start_balance) / start_balance * 100, 2)
                                                            max_balance = p2p5[5]
                                                            if profit > 0:
                                                                db_data.append((profit, position1, position5, start_currency, currency5,
                                                                            f'{currency1}>спот {currency2}>сеть {v_in_1}>{currency3}', 'мейкер-тейкер',
                                                                            start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>комис. {k_in_1}>{p2p5[3]}', 'RUB', exchange_path5))
    # 1 обмен на 2 бирже
    for p2p1 in p2p_total:
        if p2p1[0] == 'sell':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000*i, (max_balance // 3)*i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как МЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'

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
                                                                              f' через сеть {v_in_1} с комиссией {k_in_1}. Баланс: {current_balance2}\n'

                                            for spot3 in spot_total:
                                                if currency2 == spot3[1] and position2 == spot3[-1]:
                                                    if spot3[2] != 0:
                                                        current_balance3 = current_balance2 / spot3[2] * (
                                                                    1 - spot_comission[position2])
                                                    else:
                                                        continue
                                                    currency3 = spot3[0]
                                                    position3 = position2
                                                    exchange_path3 = exchange_path2 + f'3. Наши {currency2} на споте меняем на {currency3} по курсу {spot3[2]}.Баланс: {current_balance3}\n'
                                                elif currency2 == spot3[0] and position2 == spot3[-1]:
                                                    current_balance3 = current_balance2 * spot3[2] * (
                                                                1 - spot_comission[position2])
                                                    currency3 = spot3[1]
                                                    position3 = position2
                                                    exchange_path3 = exchange_path2 + f'3. Наши {currency2} на споте меняем на {currency3} по курсу {spot3[2]}.Баланс: {current_balance3}\n'
                                                else:
                                                    continue

                                                for p2p4 in p2p_total:
                                                    if p2p4[0] == 'buy' and currency3 == p2p4[2] and position3 == p2p4[-1]:
                                                        position4 = position3
                                                        currency4 = p2p4[1]
                                                        current_balance4 = current_balance3 * p2p4[3]
                                                        exchange_path4 = exchange_path3 + f'4. На бирже {position4} как МЕЙКЕР продаем наши {currency3} за ' \
                                                                                          f'{currency4} по курсу {p2p4[3]}. Баланс: {current_balance4}\n'
                                                        if start_balance != 0:
                                                            profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                                                            if profit > 0:
                                                                db_data.append((profit, position1, position4, start_currency, currency4,
                                                                            f'{currency1}>сеть {v_in_1}>спот {currency2}>{currency3}', 'мейкер-мейкер',
                                                                            start_balance, round(max_balance), f'{p2p1[3]}>комис. {k_in_1}>спот {spot3[2]}>{p2p4[3]}', 'RUB', exchange_path4))

                                                for p2p5 in p2p_total:
                                                    if p2p5[0] == 'sell' and currency3 == p2p5[2] and position3 == p2p5[-1] \
                                                            and start_balance >= p2p5[4] and start_balance <= p2p5[5]:
                                                        position5 = position3
                                                        currency5 = p2p5[1]
                                                        current_balance5 = current_balance3 * p2p5[3]
                                                        exchange_path5 = exchange_path3 + f'4. На бирже {position5} как ТЕЙКЕР продаем наши {currency3} за ' \
                                                                                          f'{currency5} по курсу {p2p5[3]}. Баланс: {current_balance5}\n'
                                                        if start_balance != 0:
                                                            profit = round((current_balance5 - start_balance) / start_balance * 100, 2)
                                                            max_balance = p2p5[5]
                                                            if profit > 0:
                                                                db_data.append((profit, position1, position5, start_currency, currency5,
                                                                            f'{currency1}>сеть {v_in_1}>спот {currency2}>{currency3}', 'мейкер-тейкер',
                                                                            start_balance, round(max_balance), f'{p2p1[3]}>комис. {k_in_1}>спот {spot3[2]}>{p2p5[3]}', 'RUB', exchange_path5))
    # 2 обмена на каждой из бирж
    for p2p1 in p2p_total:
        if p2p1[0] == 'sell':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000 * i, (max_balance // 3) * i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как МЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'

                for spot2 in spot_total:
                    if currency1 == spot2[1] and position1 == spot2[-1]:
                        if spot2[2] != 0:
                            current_balance2 = current_balance1 / spot2[2] * (1 - spot_comission[position1])
                        else:
                            continue
                        currency2 = spot2[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    elif currency1 == spot2[0] and position1 == spot2[-1]:
                        current_balance2 = current_balance1 * spot2[2] * (1 - spot_comission[position1])
                        currency2 = spot2[1]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    else:
                        continue

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
                                                                                  f' через сеть {v_in_1} с комиссией {k_in_1}. Баланс: {current_balance3}\n '

                                                for spot4 in spot_total:
                                                    if currency3 == spot4[1] and position3 == spot4[-1]:
                                                        if spot4[2] != 0:
                                                            current_balance4 = current_balance3 / spot4[2] * (
                                                                    1 - spot_comission[position3])
                                                        else:
                                                            continue
                                                        currency4 = spot4[0]
                                                        position4 = position3
                                                        exchange_path4 = exchange_path3 + f'4. Наши {currency3} на споте меняем на {currency4} по курсу {spot4[2]}.Баланс: {current_balance4}\n '
                                                    elif currency3 == spot4[0] and position3 == spot4[-1]:
                                                        current_balance4 = current_balance3 * spot4[2] * (
                                                                1 - spot_comission[position3])
                                                        currency4 = spot4[1]
                                                        position4 = position3
                                                        exchange_path4 = exchange_path3 + f'4. Наши {currency3} на споте меняем на {currency4} по курсу {spot4[2]}.Баланс: {current_balance4}\n '
                                                    else:
                                                        continue

                                                    for p2p5 in p2p_total:
                                                        if p2p5[0] == 'buy' and currency4 == p2p5[2] and position4 == p2p5[-1]:
                                                            position5 = position4
                                                            currency5 = p2p5[1]
                                                            current_balance5 = current_balance4 * p2p5[3]
                                                            exchange_path5 = exchange_path4 + f'5. На бирже {position5} как МЕЙКЕР продаем наши {currency4} за ' \
                                                                                              f'{currency5} по курсу {p2p5[3]}. Баланс: {current_balance5}\n'
                                                            if start_balance != 0:
                                                                profit = round((current_balance5 - start_balance) / start_balance * 100, 2)
                                                                if profit > 0:
                                                                    db_data.append((profit, position1, position5,
                                                                                    start_currency, currency5,
                                                                                    f'{currency1}>спот {currency2}>сеть {v_in_1}>спот {currency3}>{currency4}',
                                                                                    'мейкер-мейкер',
                                                                                    start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>комис. {k_in_1}>спот {spot4[2]}>{p2p5[3]}', 'RUB', exchange_path5))

                                                    for p2p6 in p2p_total:
                                                        if p2p6[0] == 'sell' and currency4 == p2p6[2] and position4 == p2p6[-1] \
                                                                and start_balance >= p2p6[4] and start_balance <= p2p6[5]:
                                                            position6 = position4
                                                            currency6 = p2p6[1]
                                                            current_balance6 = current_balance4 * p2p6[3]
                                                            exchange_path6 = exchange_path4 + f'5. На бирже {position6} как ТЕЙКЕР продаем наши {currency4} за ' \
                                                                                              f'{currency6} по курсу {p2p6[3]}. Баланс: {current_balance6}\n'
                                                            if start_balance != 0:
                                                                profit = round((current_balance6 - start_balance) / start_balance * 100, 2)
                                                                max_balance = p2p6[5]
                                                                if profit > 0:
                                                                    db_data.append((profit, position1, position6,
                                                                                    start_currency, currency6,
                                                                                    f'{currency1}>спот {currency2}>сеть {v_in_1}>спот {currency3}>{currency4}',
                                                                                    'мейкер-тейкер',
                                                                                    start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>комис. {k_in_1}>спот {spot4[2]}>{p2p6[3]}', 'RUB', exchange_path6))
    # Внутрибирж с обменом
    for p2p1 in p2p_total:
        if p2p1[0] == 'sell':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000 * i, (max_balance // 3) * i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как МЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'

                for spot2 in spot_total:
                    if currency1 == spot2[1] and position1 == spot2[-1]:
                        if spot2[2] != 0:
                            current_balance2 = current_balance1 / spot2[2] * (1 - spot_comission[position1])
                        else:
                            continue
                        currency2 = spot2[0]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    elif currency1 == spot2[0] and position1 == spot2[-1]:
                        current_balance2 = current_balance1 * spot2[2] * (1 - spot_comission[position1])
                        currency2 = spot2[1]
                        position2 = position1
                        exchange_path2 = exchange_path1 + f'2. Наши {currency1} на споте меняем на {currency2} по курсу {spot2[2]}.Баланс: {current_balance2}\n'
                    else:
                        continue

                    for p2p3 in p2p_total:
                        if p2p3[0] == 'buy' and currency2 == p2p3[2] and position2 == p2p3[-1]:
                            position3 = position2
                            currency3 = p2p3[1]
                            current_balance3 = current_balance2 * p2p3[3]
                            exchange_path3 = exchange_path2 + f'3. На бирже {position3} как МЕЙКЕР продаем наши {currency2} за ' \
                                                              f'{currency3} по курсу {p2p3[3]}. Баланс: {current_balance3}\n'
                            if start_balance != 0:
                                profit = round((current_balance3 - start_balance) / start_balance * 100, 2)
                                if profit > 0:
                                    db_data.append((profit, position1, position3,
                                                    start_currency, currency3,
                                                    f'{currency1}>спот>{currency2}',
                                                    'мейкер-мейкер',
                                                    start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>{p2p3[3]}', 'RUB', exchange_path3))

                    for p2p4 in p2p_total:
                        if p2p4[0] == 'sell' and currency2 == p2p4[2] and position2 == p2p4[-1] \
                                and start_balance >= p2p4[4] and start_balance <= p2p4[5]:
                            position4 = position2
                            currency4 = p2p4[1]
                            current_balance4 = current_balance2 * p2p4[3]
                            exchange_path4 = exchange_path2 + f'3. На бирже {position4} как ТЕЙКЕР продаем наши {currency2} за ' \
                                                              f'{currency4} по курсу {p2p4[3]}. Баланс: {current_balance4}\n'
                            if start_balance != 0:
                                profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                                max_balance = p2p4[5]
                                if profit > 0:
                                    db_data.append((profit, position1, position4,
                                                    start_currency, currency4,
                                                    f'{currency1}>спот>{currency2}',
                                                    'мейкер-тейкер',
                                                    start_balance, round(max_balance), f'{p2p1[3]}>спот {spot2[2]}>{p2p4[3]}', 'RUB', exchange_path4))
    # Внутрибирж без обмена на споте
    for p2p1 in p2p_total:
        if p2p1[0] == 'sell':
            position1 = p2p1[-1]
            start_currency = p2p1[1]
            currency1 = p2p1[2]
            max_balance = p2p1[5] if p2p1[5] != 0 else 1
            for i in range(3):
                start_balance = round(max(500, p2p1[4]) + max(1000 * i, (max_balance // 3) * i), 0)
                if start_balance > max_balance:
                    break
                if p2p1[3] != 0:
                    current_balance1 = start_balance / p2p1[3]
                else:
                    continue
                exchange_path1 = f'1. На бирже {position1} как МЕЙКЕР за {start_currency} ' \
                                 f'покупаем {currency1} по курсу {p2p1[3]}. Баланс: {current_balance1}\n'

                for p2p3 in p2p_total:
                    if p2p3[0] == 'buy' and currency1 == p2p3[2] and position1 == p2p3[-1]:
                        position3 = position1
                        currency3 = p2p3[1]
                        current_balance3 = current_balance1 * p2p3[3]
                        exchange_path3 = exchange_path1 + f'2. На бирже {position3} как МЕЙКЕР продаем наши {currency1} за ' \
                                                          f'{currency3} по курсу {p2p3[3]}. Баланс: {current_balance3}\n'
                        if start_balance != 0:
                            profit = round((current_balance3 - start_balance) / start_balance * 100, 2)
                            if profit > 0:
                                db_data.append((profit, position1, position3,
                                                start_currency, currency3,
                                                f'{currency1}',
                                                'мейкер-мейкер',
                                                start_balance, round(max_balance), f'{p2p1[3]}>{p2p3[3]}', 'RUB', exchange_path3))

                for p2p4 in p2p_total:
                    if p2p4[0] == 'sell' and currency1 == p2p4[2] and position1 == p2p4[-1] \
                            and start_balance >= p2p4[4] and start_balance <= p2p4[5]:
                        position4 = position1
                        currency4 = p2p4[1]
                        current_balance4 = current_balance1 * p2p4[3]
                        exchange_path4 = exchange_path1 + f'2. На бирже {position4} как ТЕЙКЕР продаем наши {currency1} за ' \
                                                          f'{currency4} по курсу {p2p4[3]}. Баланс: {current_balance4}\n'
                        if start_balance != 0:
                            profit = round((current_balance4 - start_balance) / start_balance * 100, 2)
                            max_balance = p2p4[5]
                            if profit > 0:
                                db_data.append((profit, position1, position4,
                                                start_currency, currency4,
                                                f'{currency1}',
                                                'мейкер-тейкер',
                                                start_balance, round(max_balance), f'{p2p1[3]}>{p2p4[3]}', 'RUB', exchange_path4))



    db_arbitrage.clear_table()
    db_arbitrage.add_trade(db_data)




