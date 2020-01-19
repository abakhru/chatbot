import json

from chatbot import LOGGER
from chatbot.httpdriver import HttpDriver


class CurrencyRates:
    def __init__(self):
        self.base_url = '/v1'
        self.user = 'jadiy75895@etopmail.com'
        self.url_dict = {
            'latest': f'{self.base_url}/latest',
            'historical': f'{self.base_url}/historical',
            'timeseries': f':{self.base_url}/timeseries',
            'currencies': f'{self.base_url}/currencies',
            'convert': f'{self.base_url}/convert',
        }
        self.api_key = 'e7054350fcdd8a91da79c8ffb58a4ed3'
        self.auth_param = {'api_key': self.api_key}
        self.client = HttpDriver(host='api.currencyscoop.com', port=443, protocol='https')

    def __get__(self, url, params):
        _params = self.auth_param
        _params.update(params)
        result = self.client.Get(url=url, params=_params).json()['response']
        LOGGER.debug(f'Result:\n{json.dumps(result, indent=4, sort_keys=True)}')
        return result

    def get_exchange_rate(self, base='USD'):
        return self.__get__(url=self.url_dict['latest'], params={'base': base})

    def convert_currency(self, src_cur='USD', dest_cur='INR', amount=1):
        params = {'base': src_cur, 'to': dest_cur, 'amount': amount}
        return self.__get__(url=self.url_dict['convert'], params=params)

    def get_historical_data(self, base='USD', date='2010-01-01', symbols='USD'):
        _params = {'base': base, 'date': date, 'symbols': symbols}
        return self.__get__(url=self.url_dict['historical'], params=_params)


if __name__ == '__main__':
    p = CurrencyRates()
    # p.get_exchange_rate(base_currency='INR')
    # p.convert_currency(src_cur='USD', dest_cur='INR', amount=1)
    p.get_historical_data(base='INR')
