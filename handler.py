import os
from save_money import Abb, ParamsAbb, Calculator

AURORA_URL = 'https://easyview.auroravision.net'
AURORA_EIDS = os.environ.get('AURORA_EIDS')
AURORA_USER = os.environ.get('AURORA_USER')
AURORA_PASS = os.environ.get('AURORA_PASS')


def how_much_money_i_saved(event, context):
    params = ParamsAbb(
        AURORA_URL,
        AURORA_USER,
        AURORA_PASS,
        AURORA_EIDS
    )

    abb = Abb(params)
    calculator = Calculator.build(Calculator.LIGHT)
    saved = calculator.calc(abb.getSummary().getMonthly())

    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'You saved {} reais'.format(saved),
            }
        }
    }


if __name__ == "__main__":
    print(how_much_money_i_saved('', ''))