import os
import responses
from calculator import Calculator, SIMULATOR

DIRNAME = os.path.dirname(__file__)


@responses.activate
def test_should_get_the_money_saved_when_put_300_kwh():
    with open(DIRNAME+'/fixture/success.html', 'r') as html:
        responses.add(
            responses.POST, SIMULATOR, status=200, body=html.read())

    calculator = Calculator.build(Calculator.LIGHT)

    assert calculator.calc(300) == 237.61