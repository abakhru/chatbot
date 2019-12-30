#!/usr/bin/env python
import json
from pathlib import Path

import maxminddb

from chatbot import LOGGER


class MaxmindDBManager:
    LICENSE_KEY = ''

    def __init__(self):
        self.maxmind_db_files = list(Path(__file__).parent.parent.joinpath('data').rglob('*.mmdb'))
        LOGGER.debug(f'maxmind files: {self.maxmind_db_files}')
        self.reader = dict()
        for _file in self.maxmind_db_files:
            if 'city' in _file.name.lower():
                self.reader.update({'city': {'file': _file,
                                             'reader': maxminddb.open_database(str(_file))}})
            if 'country' in _file.name.lower():
                self.reader.update({'country': {'file': _file,
                                                'reader': maxminddb.open_database(str(_file))}})
            if 'asn' in _file.name.lower():
                self.reader.update({'asn': {'file': _file,
                                            'reader': maxminddb.open_database(str(_file))}})
        LOGGER.debug(f'Readers dict: {self.reader}')

    def close(self):
        for _, v in self.reader.items():
            v['reader'].close()

    def download_latest(self):
        pass

    def find(self, query):
        """

        :param query: ip=1.1.1.1
        :return:
        """
        result = self.reader['city']['reader'].get(query)
        # result = self.reader['asn']['reader'].get(query)
        # result = self.reader['country']['reader'].get(query)
        return result


if __name__ == '__main__':
    p = MaxmindDBManager()
    LOGGER.info(json.dumps(p.find('2.2.2.2'), indent=4, sort_keys=True))
