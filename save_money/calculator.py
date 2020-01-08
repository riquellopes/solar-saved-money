import abc
import os
import requests
from math import ceil
from lxml import html
from urllib.parse import urlparse
from fake_useragent import UserAgent

SIMULATOR = os.environ.get('SIMULATOR')


class BaseCalculator:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calc(self, volts: float):
        """
            Method to calculator the money to be saved.
        """
        pass


class LightCalculator:
   
    def calc(self, volts: float) -> float:
        result = self._request(volts)[0]
        return float(result.replace(',', '.'))
   
    def _request(self, volts: float) -> str:
        ua = UserAgent()
        
        payload = {
           "mesRef": self._month_reference,
           "_action": 'conta',
           "classeConsumo": "Residencial",
           "medidorTipo": 50,
           "consumoAtual": ceil(volts),
           "hidresultado": "sim"
        }

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'User-Agent': ua.random,
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': urlparse(SIMULATOR).hostname,
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "101",
            'Cookie': "ASPSESSIONIDQSTDQAAB=OLMPFHNBKHNALCAIHKIGAPHH",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        response = requests.request(
            "POST", SIMULATOR, data=payload, headers=headers)

        return [e.text_content().strip() for e in html.fromstring(
            response.text).xpath('//td[@id = "total-a-pagar-valor"]')]

    @property
    def _month_reference(self):
        base_month = 20238
        return base_month


class Calculator:
    """
        Example:
            Calculator::build(Calculator.LIGHT, 300.00)
    """
    LIGHT = 'light'

    @staticmethod
    def build(type: str) -> BaseCalculator:
        return LightCalculator()