from unittest import TestCase

from parameterized import parameterized
from tabulate import tabulate

from chatbot import LOGGER
from chatbot.bot import ChatBot


class TestChatBot(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.bot = ChatBot()

    @parameterized.expand([
        ('whois google.com', 'GOOGLE INC.'),
        ('whois oracle.com', 'GODADDY.COM, LLC'),
        ('whois pepsi.com', 'GOOGLE INC.'),
        ])
    def test_whois(self, _input, expected_response):
        response = self.bot.respond(_input)
        LOGGER.debug(tabulate(response, tablefmt='sql'))
        import pdb;pdb.set_trace()
        assert expected_response in [i for i in response[2]]
