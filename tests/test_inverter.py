import os
import pytest
import responses
from requests.exceptions import HTTPError
from inverter import Abb, ParamsAbb

DIRNAME = os.path.dirname(__file__)


@responses.activate
def test_should_get_134_707_when_call_the_method_getMonthly():
    params_abb = ParamsAbb(
        'http://abb',
        'will',
        'xxxxxxx',
        '111111'
    )

    with open(DIRNAME+'/fixture/summary.json', 'r') as json:
        responses.add(
            responses.GET,
            params_abb.url_summary, status=200, body=json.read())

    abb = Abb(params_abb)
    assert abb.getSummary().getMonthly() == '134.707'


@responses.activate
def test_should_raise_a_http_exception():
    params_abb = ParamsAbb(
        'http://abb',
        'will',
        'xxxxxxx',
        '111111'
    )

    responses.add(
            responses.GET,
            params_abb.url_summary, status=403, json='{}')
    
    abb = Abb(params_abb)
    with pytest.raises(HTTPError):
        abb.getSummary().getMonthly()