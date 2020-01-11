import os
import pytest
import responses
from freezegun import freeze_time
from calculator import (
    Calculator, SIMULATOR, OutOfServiceException, NotFoundException)

DIRNAME = os.path.dirname(__file__)


@responses.activate
def test_should_get_the_money_saved_when_put_300_kwh():
    with open(DIRNAME+'/fixture/success.html', 'r') as html:
        responses.add(
            responses.POST, SIMULATOR, status=200, body=html.read())

    calculator = Calculator.build(Calculator.LIGHT)

    assert calculator.calc(300) == 237.61


@responses.activate
def test_should_raise_not_found_exception_when_amount_not_found():
    responses.add(responses.POST, SIMULATOR, status=200, body='<html></html>')

    calculator = Calculator.build(Calculator.LIGHT)

    with pytest.raises(NotFoundException):
        calculator.calc(300)


@responses.activate
def test_should_raise_exception_when_status_not_equal_200():
    responses.add(responses.POST, SIMULATOR, status=500)
    calculator = Calculator.build(Calculator.LIGHT)

    with pytest.raises(OutOfServiceException):
        calculator.calc(300)


@freeze_time("2020-01-11")
def test_should_get_month_reference_equal_the_20239():
	calculator = Calculator.build(Calculator.LIGHT)
	assert calculator._month_reference == 20239