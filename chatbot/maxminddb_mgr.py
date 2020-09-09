#!/usr/bin/env python
import json
import re
import subprocess

import maxminddb

from chatbot import LOGGER, ROOT_DIR


class MaxmindDBManager:

    LICENSE_KEY = ""

    def __init__(self):
        self.maxmind_db_files = list(ROOT_DIR.joinpath("data").rglob("*.mmdb"))
        self.download_latest()
        self.reader = dict()
        for _file in self.maxmind_db_files:
            if "city" in _file.name.lower():
                self.reader.update(
                    {
                        "city": {
                            "file": _file,
                            "reader": maxminddb.open_database(str(_file)),
                        }
                    }
                )
            if "country" in _file.name.lower():
                self.reader.update(
                    {
                        "country": {
                            "file": _file,
                            "reader": maxminddb.open_database(str(_file)),
                        }
                    }
                )
            if "asn" in _file.name.lower():
                self.reader.update(
                    {
                        "asn": {
                            "file": _file,
                            "reader": maxminddb.open_database(str(_file)),
                        }
                    }
                )

    def close(self):
        for _, v in self.reader.items():
            v["reader"].close()

    def download_latest(self):
        if not len(self.maxmind_db_files):
            cmd = (
                f"geoipupdate "
                f"-f {ROOT_DIR}/config/GeoIP.conf "
                f"--database-directory {ROOT_DIR}/data -v"
            )
            subprocess.check_output(cmd, shell=True)
            self.maxmind_db_files = list(ROOT_DIR.joinpath("data").rglob("*.mmdb"))
        assert len(self.maxmind_db_files) > 2

    def maxmind_search(self, query):
        """

        :param query: ip=1.1.1.1
        :return:
        """
        result = self.reader["city"]["reader"].get(query)
        # result = self.reader['asn']['reader'].get(query)
        # result = self.reader['country']['reader'].get(query)
        return result

    def geoip_lookup(self, _input):
        """geoip lookup"""
        # extract IPv4 address from the string
        reg_ex = re.search(
            r"""((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.){3}(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)))""",
            _input,
        )
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                LOGGER.debug(f"topic: {topic}")
                return self.maxmind_search(topic)
        except Exception as e:
            LOGGER.error(e)
            LOGGER.warning(f"No valid IP {reg_ex.group(1)} has been found")

    @staticmethod
    def check_ip(_ip):
        # regex for validating an Ip-address
        regex = r"""^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                        25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)"""

        if re.search(regex, _ip):
            return True
        else:
            return False

    def check_if_url_domain_ip(self, request_data):
        _response = None
        if self.check_ip(request_data):
            _response = f"ip_address={request_data}"
        if request_data == "domain":
            _response = f"domain={request_data}"
        if request_data == "url":
            _response = f"url={request_data}"
        return _response.split("=")[0], _response


if __name__ == "__main__":
    p = MaxmindDBManager()
    LOGGER.info(json.dumps(p.find("1.1.1.1"), indent=4, sort_keys=True))
    p.close()
