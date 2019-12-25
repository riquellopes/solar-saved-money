import os
import http
import requests
from math import ceil
from lxml import html
from urllib.parse import urlparse
from requests.auth import HTTPBasicAuth
from fake_useragent import UserAgent

AURORA_ENERGY = 'https://easyview.auroravision.net/easyview/services/gmi/summary/PlantEnergy.json?eids={}'
AURORA_EIDS=os.environ.get('AURORA_EIDS')
AURORA_USER=os.environ.get('AURORA_USER')
AURORA_PASS=os.environ.get('AURORA_PASS')

SIMULATOR = os.environ.get('SIMULATOR')

def calculator(value):
    ua = UserAgent()
    value = float(value)
    payload = "mesRef=20238&_action=conta&classeConsumo=Residencial&medidorTipo=50&consumoAtual={}&hidresultado=sim"
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

    response = requests.request("POST", SIMULATOR, data=payload.format(ceil(value)), headers=headers)
    return [e.text_content().strip() for e in html.fromstring(response.text).xpath('//td[@id = "total-a-pagar-valor"]')]


def get_summary():
    basic_auth = HTTPBasicAuth(AURORA_USER, AURORA_PASS)
    response = requests.get(AURORA_ENERGY.format(AURORA_EIDS), auth=basic_auth)

    if response.status_code == http.HTTPStatus.OK:
        response_service = response.json()
        for fields in response_service['fields']:
            result = calculator(fields['value'])
            print(result, "{} Kwh".format(fields['value']), fields['label'])
    response.raise_for_status()


if __name__ == '__main__':
    getSummary()