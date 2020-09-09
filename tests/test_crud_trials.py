#!/usr/bin/env python
import json
from unittest import TestCase

import requests

from chatbot import LOGGER

headers = {
    "Content-Type": "application/json",
    "cache-control": "no-cache",
    "Postman-Token": "578dd394-fd6f-4547-af23-4ae465d35a6a",
}


class TestCRUDTrials(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.session = requests.Session()
        cls.base_url = "http://0.0.0.0:8000"
        cls.payload = {"Name": "AAAAAAA"}

    def test_1_create(self):
        response = self.session.post(
            url=f"{self.base_url}/create",
            data=json.dumps(self.payload),
            headers=headers,
        )
        LOGGER.debug(f"Response: {response.text}")
        assert response.status_code == 200
        assert response.json()["Message"] == "Success"

    def test_2_read(self):
        response = self.session.get(url=f"{self.base_url}/read", headers=headers)
        LOGGER.debug(f"Response: {response.text}")
        assert response.status_code == 200
        assert response.json()["Name"][0] == self.payload["Name"]

    def test_3_update(self):
        self.payload["Name"] = "BBBBB"
        response = self.session.put(
            url=f"{self.base_url}/update",
            data=json.dumps(self.payload),
            headers=headers,
        )
        LOGGER.debug(f"Response: {response.text}")
        assert response.status_code == 200
        assert response.json()["Message"] == "Success"

    def test_4_delete(self):
        self.payload["Name"] = "BBBBB"
        response = self.session.delete(
            url=f"{self.base_url}/delete",
            data=json.dumps(self.payload),
            headers=headers,
        )
        LOGGER.debug(f"Response: {response.text}")
        assert response.status_code == 200
        assert response.json()["Message"] == "Success"
