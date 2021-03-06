import abc
import os
import http
import requests
import re
from math import ceil
from datetime import datetime
from urllib.parse import urlparse
from fake_useragent import UserAgent

SIMULATOR = os.environ.get('SIMULATOR')
BASE_MONTH = os.environ.get('BASE_MONTH', 20238)


class BaseException(Exception):
    pass


class OutOfServiceException(BaseException):
    pass


class NotFoundException(BaseException):
    pass


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
        response = self._request(volts)
        if response:
            return float(response.replace(',', '.'))
        raise NotFoundException()
   
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
    
        if response.status_code == http.HTTPStatus.OK:
            compiled = re.compile("[\n\t\r]")
            sanitary = compiled.sub("", response.text)

            tags = sanitary.replace(
                " ", "").split('id="total-a-pagar-valor"')
            
            if(tags and len(tags) > 1):
                return tags[1].replace(
                    "><strong>", "").split("</strong>")[0]
            return None
        raise OutOfServiceException('')

    @property
    def _month_reference(self):
        return BASE_MONTH + datetime.now().month


class Calculator:
    """
        Example:
            Calculator::build(Calculator.LIGHT, 300.00)
    """
    LIGHT = 'light'

    @staticmethod
    def build(type: str) -> BaseCalculator:
        return LightCalculator()