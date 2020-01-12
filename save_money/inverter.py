import abc
import http
import requests
from requests.auth import HTTPBasicAuth


class Params:
    __metaclass__ = abc.ABCMeta

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password


class Inverter:
    __metaclass__ = abc.ABCMeta

    def __init__(self, params: Params):
        self._params = params

    @abc.abstractmethod
    def getSummary(self):
        pass
    
    @property
    def params(self):
        return self._params


class ParamsAbb(Params):
    
    def __init__(self, url, user, password, eids):
        self.eids = eids
        super(ParamsAbb, self).__init__(url, user, password)
    
    @property
    def url_summary(self):
        address = "{}/easyview/services/gmi/summary/PlantEnergy.json?eids={}"
        return address.format(self.url, self.eids)


class Summary:
    __metaclass__ = abc.ABCMeta

    def __init__(self, response):
        self._response = response

    @abc.abstractmethod
    def getMonthly(self):
        pass


class SummaryAbb(Summary):

    def getMonthly(self):
        for field in self._response['fields']:
            if field['label'] == 'month':
                return float(field['value'])
    

class Abb(Inverter):
    
    def getSummary(self):
        basic_auth = HTTPBasicAuth(self.params.user, self.params.password)
        response = requests.get(self.params.url_summary, auth=basic_auth)

        if response.status_code == http.HTTPStatus.OK:
            return SummaryAbb(response.json())
        response.raise_for_status()