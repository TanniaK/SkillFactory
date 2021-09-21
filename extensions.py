import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class APIException:
     @staticmethod
     def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать колличество {amount}')

        # quote_ticker, base_ticker = keys[quote], keys[base]
        r1 = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms=EUR')
        r2 = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms=EUR')
        r1_ = json.loads(r1.content)

        r2_ = json.loads(r2.content)

        total_base = round((r1_['EUR']) / (r2_['EUR']) * float(amount), 2)
        return total_base
