import aiohttp
import asyncio
import requests

from OKX.OKX_config import payments

class OKX_p2p_price:

    def __init__(self, **kwargs):

        if kwargs.get('side') == 'sell':
            self.cookies = {
                'first_ref': 'https%3A%2F%2Fwww.google.com%2F',
                'locale': 'ru_RU',
                '_ga': 'GA1.2.1016706193.1657383148',
                'u_pid': 'D6D6lm9rEC5jB70',
                'G_ENABLED_IDPS': 'google',
                'ftID': '521051424961848.0117319c7fd04f42c843c0ef97fcdefa84b41.1010L3o0.06A0FD813CD36D44',
                'x-lid': 'c85894ccc29bb9ca2688d549d326b0e886f746280cc77fa6ff50d880733406e4e6d5a63b',
                'isLogin': '1',
                '_gcl_au': '1.1.1479884061.1657458855',
                'amp_56bf9d': 'cUc4KGhAvEnMOlyh2lhM76.SnlaeStiUGxFdkJXTFNHbmVKNGVVQT09..1g7r1mcl4.1g7r37hqj.5a.g.5q',
                'amp_56bf9d_okx.com': 'cUc4KGhAvEnMOlyh2lhM76.SnlaeStiUGxFdkJXTFNHbmVKNGVVQT09..1g7r1mclf.1g7r37hqr.i.4.m',
            }

            self.headers = {
                'authority': 'www.okx.com',
                'accept': 'application/json',
                'accept-language': 'ru-RU',
                'app-type': 'web',
                # Requests sorts cookies= alphabetically
                # 'cookie': 'locale=ru_RU; first_ref=https%3A%2F%2Fwww.google.com%2F; _gcl_au=1.1.489115200.1657347940; _ga=GA1.2.1753334504.1657347941; _gid=GA1.2.529915200.1657347941; _gat_UA-35324627-3=1; amp_56bf9d=fTtXIFBYA3EwfDurIeHkOL...1g7gq57v4.1g7gqd09e.a.1.b',
                'devid': '843d3491-f670-45c6-a86b-96af2850fbc1',
                'referer': 'https://www.okx.com/ru/p2p-markets/rub/buy-usdt',
                'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                'x-cdn': 'https://static.okx.com',
                'x-utc': '3',
            }
            self.params = {

                'quoteCurrency': kwargs.get('quoteCurrency'),
                'baseCurrency': kwargs.get('baseCurrency'),
                'side': kwargs.get('side'),
                'paymentMethod': kwargs.get('paymentMethod'),
                'userType': 'all',
                'showTrade': 'false',
                'showFollow': 'false',
                'showAlreadyTraded': 'false',
                'isAbleFilter': 'false',
                'quoteMinAmountPerOrder': kwargs.get('quoteMinAmountPerOrder')
            }
        else:
            self.cookies = {
                'first_ref': 'https%3A%2F%2Fwww.google.com%2F',
                'locale': 'ru_RU',
                '_ga': 'GA1.2.1016706193.1657383148',
                'u_pid': 'D6D6lm9rEC5jB70',
                'G_ENABLED_IDPS': 'google',
                'ftID': '521051424961848.0117319c7fd04f42c843c0ef97fcdefa84b41.1010L3o0.06A0FD813CD36D44',
                'x-lid': 'c85894ccc29bb9ca2688d549d326b0e886f746280cc77fa6ff50d880733406e4e6d5a63b',
                'isLogin': '1',
                '_gcl_au': '1.1.1479884061.1657458855',
                'amp_56bf9d': 'cUc4KGhAvEnMOlyh2lhM76.SnlaeStiUGxFdkJXTFNHbmVKNGVVQT09..1g7r1mcl4.1g7r37hqj.5a.g.5q',
                'amp_56bf9d_okx.com': 'cUc4KGhAvEnMOlyh2lhM76.SnlaeStiUGxFdkJXTFNHbmVKNGVVQT09..1g7r1mclf.1g7r37hqr.i.4.m',
            }

            self.headers = {
                'authority': 'www.okx.com',
                'accept': 'application/json',
                'accept-language': 'ru-RU',
                'app-type': 'web',
                'authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJleDExMDE2NTczODMzMzgzODE1OEIyMkRDMjkxMjQxQjRDRndyVyIsInVpZCI6Imx4em04ZTBrbU5KLzRPaEpTdDJzTlE9PSIsInN0YSI6MCwibWlkIjoibHh6bThlMGttTkovNE9oSlN0MnNOUT09IiwiaWF0IjoxNjU3Njg2NzI3LCJleHAiOjE2NTgyOTE1MjcsImJpZCI6MCwiZG9tIjoid3d3Lm9reC5jb20iLCJpc3MiOiJva2NvaW4iLCJzdWIiOiIxNEZFNEQ4NTM4NEY3NjlDNUM2Mjk5MUFGQjVGRkRERiJ9.a6fJkbBIt4Cpdz_uODGFmfsZkOLpXl8sn-9u_PX8f6mQYPi-RuwuV5AqBb_e6sMyKxQ3BfYfPhYvxN8HvAcWYw',
                # Requests sorts cookies= alphabetically
                # 'cookie': 'first_ref=https%3A%2F%2Fwww.google.com%2F; locale=ru_RU; _ga=GA1.2.1016706193.1657383148; u_pid=D6D6lm9rEC5jB70; G_ENABLED_IDPS=google; ftID=521051424961848.0117319c7fd04f42c843c0ef97fcdefa84b41.1010L3o0.06A0FD813CD36D44; x-lid=c85894ccc29bb9ca2688d549d326b0e886f746280cc77fa6ff50d880733406e4e6d5a63b; isLogin=1; _gcl_au=1.1.1479884061.1657458855; amp_56bf9d=cUc4KGhAvEnMOlyh2lhM76.SnlaeStiUGxFdkJXTFNHbmVKNGVVQT09..1g7r1mcl4.1g7r37hqj.5a.g.5q; amp_56bf9d_okx.com=cUc4KGhAvEnMOlyh2lhM76.SnlaeStiUGxFdkJXTFNHbmVKNGVVQT09..1g7r1mclf.1g7r37hqr.i.4.m',
                'devid': '3b525e5f-9891-4fcc-ab43-fc4fc6b47778',
                'ftid': '521051424961848.0117319c7fd04f42c843c0ef97fcdefa84b41.1010L3o0.06A0FD813CD36D44',
                'referer': 'https://www.okx.com/ru/p2p-markets/rub/sell-usdt',
                'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                'x-cdn': 'https://static.okx.com',
                'x-utc': '3',
            }
            self.params = {
                'quoteCurrency': kwargs.get('quoteCurrency'),
                'baseCurrency': kwargs.get('baseCurrency'),
                'side': kwargs.get('side'),
                'paymentMethod': kwargs.get('paymentMethod'),
                'userType': 'all',
                'showTrade': 'false',
                'showFollow': 'false',
                'showAlreadyTraded': 'false',
                'isAbleFilter': 'false',
                'quoteMinAmountPerOrder': kwargs.get('quoteMinAmountPerOrder')
            }


        self.url = 'https://www.okx.com/v3/c2c/tradingOrders/books'
        self.fiat = payments[self.params["paymentMethod"]]
        self.crypto = self.params['baseCurrency']

    async def price(self, session):
        try:
            async with session.get(url=self.url, headers=self.headers, params=self.params) as response:
                data = await response.json()
                min_price = float(data['data']['sell'][0]['price'])
                if self.params['side'] == 'sell':
                    for i in range(min(3, len(data['data']['sell']))):
                        if float(data['data']['sell'][i]['completedRate']) > 0.85 and float(data['data']['sell'][i]['price']) < (min_price * 1.05):
                            return 'buy', self.fiat, self.crypto, float(data['data']['sell'][i]['price']), \
                                   float(data['data']['sell'][i]['quoteMinAmountPerOrder']), \
                                   float(data['data']['sell'][i]['quoteMaxAmountPerOrder']), 'OKX'
                else:
                    for i in range(min(3, len(data['data']['buy']))):
                        if float(data['data']['buy'][i]['completedRate']) > 0.85 and float(data['data']['sell'][i]['price']) < (min_price * 1.05):
                            return 'sell', self.fiat, self.crypto, float(data['data']['buy'][i]['price']), \
                                   float(data['data']['buy'][i]['quoteMinAmountPerOrder']), \
                                   float(data['data']['buy'][i]['quoteMaxAmountPerOrder']), 'OKX'

        except Exception:
            if self.params['side'] == 'sell':
                return 'buy', self.fiat, self.crypto, 0, 0, 0, 'OKX'
            else:
                return 'sell', self.fiat, self.crypto, 0, 0, 0, 'OKX'
