#!/usr/bin/env python
import json
import re

import ijson
import requests

from chatbot import DATA_DIR, LOGGER


class QueryMitre:
    def __init__(self):
        self.mitre_data = None
        self.mitre_data_file_path = DATA_DIR.joinpath("mitre.txt")
        self.get_mitre_data()

    @staticmethod
    def get_external_id(_item):
        if isinstance(_item.get("external_references"), list):
            for refs in _item["external_references"]:
                if refs.get("external_id"):
                    return refs.get("external_id")

    def __build_response(self, _item):
        response = dict()
        topic = self.get_external_id(_item)
        name = _item.get("name")
        refs = [i["url"] for i in _item["external_references"]]
        response[topic] = {"Name": name, "External References": refs}
        return response

    def search_names(self, _name):
        named_related_ids = list()  # list of dict
        for _item in self.mitre_data:
            if _item.get("name"):
                if all(
                    [
                        _name in _item.get("name"),
                        isinstance(_item.get("external_references"), list),
                    ]
                ):
                    try:
                        topic = _item["external_references"][0]["external_id"]
                        named_related_ids.append(topic)
                    except TypeError as _:
                        continue
        LOGGER.debug(f"Topics related to {_name}: {named_related_ids}")
        return named_related_ids

    def search_t_id(self, _id):
        for i in ijson.items(self.mitre_data_file_path.open(), "objects.item"):
            temp_id = self.get_external_id(i)
            if temp_id == _id:
                LOGGER.debug(f'Returning {i.get("id")}')
                return i

    def get_mitre_data(self):
        urls = [
            "https://www.exabeam.com/information-security/what-is-mitre-attck-an-explainer/",
            (
                "https://raw.githubusercontent.com/mitre/cti/master/"
                "enterprise-attack/enterprise-attack.json"
            ),
        ]
        if not self.mitre_data_file_path.exists():
            r = requests.get(urls[-1])
            assert r.status_code == 200
            self.mitre_data_file_path.write_text(r.text)
        if not self.mitre_data:
            self.mitre_data = ijson.items(
                self.mitre_data_file_path.open(), "objects.item"
            )

    def search_mitre_data(self, _input):
        """mitre search"""
        reg_ex = re.search("mitre (.*)", _input)
        topic = reg_ex.group(1).capitalize()
        final_response = list()
        if topic.startswith("T"):
            final_response.append(self.__build_response(self.search_t_id(topic)))
        else:
            for _id in self.search_names(topic):
                LOGGER.debug(f"Processing response for {_id}")
                id_item = self.search_t_id(_id)
                if isinstance(id_item, dict):
                    LOGGER.debug(f"Found {id_item} for {_id}")
                    final_response.append(self.__build_response(id_item))
        return final_response


if __name__ == "__main__":
    p = QueryMitre()
    # LOGGER.info(json.dumps(p.search_t_id('T1134'), indent=4, sort_keys=True))
    LOGGER.info(
        json.dumps(p.search_mitre_data("mitre Manipulation"), indent=4, sort_keys=True)
    )
