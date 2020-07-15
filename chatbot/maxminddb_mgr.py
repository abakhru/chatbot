#!/usr/bin/env python
import json
import subprocess
from pathlib import Path

import maxminddb

from chatbot import LOGGER


class MaxmindDBManager:
    LICENSE_KEY = ''

    def __init__(self):
        self.app_home = Path(__file__).parent.parent
        self.maxmind_db_files = list(self.app_home.joinpath('data').rglob('*.mmdb'))
        self.download_latest()
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
        if not len(self.maxmind_db_files):
            cmd = (f'geoipupdate '
                   f'-f {self.app_home}/config/GeoIP.conf '
                   f'-d {self.app_home}/data -v')
            subprocess.check_output(cmd, shell=True)
            self.maxmind_db_files = list(self.app_home.joinpath('data').rglob('*.mmdb'))

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
