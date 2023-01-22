import aiohttp
import asyncio

from Kucoin.Kucoin_config import payments as banks

class Kucoin_p2p_price:

    def __init__(self, **kwargs):
        self.headers = {
            'authority': 'www.kucoin.com',
            'accept': 'application/json',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cs;q=0.6',
            # Requests sorts cookies= alphabetically
            # 'cookie': '_ga=GA1.2.1386239327.1655827799; _fbp=fb.1.1655827899914.1606590646; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22157332026%22%2C%22first_id%22%3A%221818707187d476-0fd9293a1535de8-26021b51-2073600-1818707187ec0a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_utm_source%22%3A%22af%22%7D%2C%22%24device_id%22%3A%221818707187d476-0fd9293a1535de8-26021b51-2073600-1818707187ec0a%22%7D; _uetvid=d50248e0f17c11ec9191c38d542b7780; X-TRACE=KgJ/FzMVGPjurIIY9KGBkfMyiQZP9xVttP40DAUMqGQ=; __cfruid=2ca54637d4d85f599781f720bf898763f680be9f-1657460312; _gid=GA1.2.915612650.1657460314; x-bullet-token=2neAiuYvAU5cbMXpmsXD5OJlewXCKryg8dSpDCgag8ZwbZpn3uIHi0A1AOtpCibAwoXOiOG0Q0GvVuAwBjvzEZ4T-PWYMvSiKP9skagWvgmEmBnqjWbDy6qRyqznCVt1whuoNZhpWWEV0AFi49kmpDIkkVy4oxRa.CrEs-_XSh1XhnUq1RKd30w==; __cf_bm=Usf8gebqBNdSUa.vWxJruGx2XtuBSCbm_Sn5e6a.4_0-1657460322-0-ATUSoyGnum03rNY4852YOHhHGsJBZHBI11s0sZDHIEdu8m4evR0OiKbTegvHNfHDCqRDw2ZgXM4NzyU5bZRmN0ZOxDMZ/i0hm6GPEL7uZvxruSuMz2tcazzxSm1cjOgEAg==; _gat=1; AWSALB=OyVhJD7UOWildrfl/e3jCyB4/VWw3FLvlyszEfsiHxnL8Jhm1uuhqd1qBw5vvKAbEmDTFtkVD9Gu9Owo6OzlRQhnsJQsjQNqr338vDgKpYfjKqi5GziHbEhFB8EO; AWSALBCORS=OyVhJD7UOWildrfl/e3jCyB4/VWw3FLvlyszEfsiHxnL8Jhm1uuhqd1qBw5vvKAbEmDTFtkVD9Gu9Owo6OzlRQhnsJQsjQNqr338vDgKpYfjKqi5GziHbEhFB8EO',
            'referer': 'https://www.kucoin.com/ru/otc/buy/USDT-RUB',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }

        self.params = {
            'currency': kwargs.get('currency'),
            'side': kwargs.get('side'),
            'legal': kwargs.get('legal'),
            'page': '1',
            'pageSize': '20',
            'status': 'PUTUP',
            'lang': 'ru_RU',
        }

        self.url = 'https://www.kucoin.com/_api/otc/ad/list'
        self.side = kwargs.get('side')
        self.fiat = f'{self.params["legal"]}-Kucoin'
        self.crypto = f"{self.params['currency']}-Kucoin"

    async def price(self, session):
        try:
            answer = []
            async with session.get(url=self.url, headers=self.headers, params=self.params) as response:
                data = await response.json()
                data_items = data['items']
                for bank in banks:
                    flag = False
                    for items in data_items:
                        if float(items['dealOrderRate'].rstrip('%')) > 85:
                            item_pyments = items['adPayTypes']
                            for payment in item_pyments:
                                if payment['payTypeCode'] == 'OTHER':
                                    for el in bank[:2]:
                                        if el in payment['reservedFields']:
                                            if self.side.lower() == 'sell':
                                                answer.append(['buy', bank[0], items["currency"], float(items['floatPrice']),
                                                               float(items['limitMinQuote']), float(items['limitMaxQuote']), 'Kucoin'])
                                            else:
                                                answer.append(['sell', bank[0], items["currency"], float(items['floatPrice']),
                                                               float(items['limitMinQuote']), float(items['limitMaxQuote']), 'Kucoin'])
                                    break
                                elif payment['payTypeCode'] == 'BANK':
                                    if payment['bankName'] != None and payment['bankName'] in bank:
                                        flag = True
                                        if self.side.lower() == 'sell':
                                            answer.append(['buy', bank[0], items["currency"], float(items['floatPrice']),
                                                           float(items['limitMinQuote']), float(items['limitMaxQuote']), 'Kucoin'])
                                        else:
                                            answer.append(['sell', bank[0], items["currency"], float(items['floatPrice']),
                                                           float(items['limitMinQuote']), float(items['limitMaxQuote']), 'Kucoin'])
                                    else:
                                        if self.side.lower() == 'sell':
                                            answer.append(['buy', payment["payTypeCode"], items["currency"], float(items['floatPrice']),
                                                           float(items['limitMinQuote']), float(items['limitMaxQuote']), 'Kucoin'])
                                        else:
                                            answer.append(['sell', payment["payTypeCode"], items["currency"], float(items['floatPrice']),
                                                           float(items['limitMinQuote']), float(items['limitMaxQuote']), 'Kucoin'])
                                    flag = True
                                    break
                                elif payment['payTypeCode'] in bank:
                                    if self.side.lower() == 'sell':
                                        answer.append(['buy', payment["payTypeCode"], items["currency"], float(items['floatPrice']),
                                                       float(items['limitMinQuote']), float(items['limitMaxQuote']), 'Kucoin'])
                                    else:
                                        answer.append(['sell', payment["payTypeCode"], items["currency"], float(items['floatPrice']),
                                                       float(items['limitMinQuote']), float(items['limitMaxQuote']), 'Kucoin'])
                                    flag = True
                                    break


                            if flag:
                                break

            return answer
        except Exception:
            return None
