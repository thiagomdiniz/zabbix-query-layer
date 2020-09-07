import requests
import time
from base64 import b64encode

class ZqlZabbixAPI():

    JSONRPC_URL = '/api_jsonrpc.php'
    _basic_auth = None
    _auth_token = None

    def __init__(self, address, username, password, ssl_verify=True, http_auth=False, date_format=None, timestamp_fields=[]):
        self._url = address + self.JSONRPC_URL
        self._ssl_verify = ssl_verify
        self.setDateFormat(date_format)
        self.setTimestampFields(timestamp_fields)
        if http_auth:
            self._basic_auth = b64encode(bytes(username + ':' + password, "utf-8")).decode("ascii")
        self._auth_token = self.login(username, password)


    def login(self, username, password):
        if username and password:
            try:
                token = self.makeApiRequest('user.login',
                            {'user': username, 'password': password},
                            auth=False)
                return token

            except Exception as e:
                raise Exception(e)

        else:
            raise Exception('Please pass a username and password!')


    def logout(self):
        self.makeApiRequest('user.logout')


    def getApiRequest(self, method, params={}, auth=True, jsonrpc='2.0', id=1):
        if method:
            if self._date_format:
                for key, value in params.items():
                    if key in self._timestamp_fields:
                        params[key] = int(time.mktime(time.strptime(value, self._date_format)))

            request = {'jsonrpc': jsonrpc,
                        'method': method,
                        'params': params,
                        'auth': self._auth_token,
                        'id': id}
            if not auth:
                del request['auth']

            return request
        else:
            raise Exception('API method name is missing!')


    def doApiRequest(self, payload):
        headers = {'Content-Type': 'application/json-rpc',
                    'User-Agent': 'python/zql'}
        if self._basic_auth:
            headers['Authorization'] = 'Basic %s' % self._basic_auth

        if payload:
            try:
                r = requests.post(self._url, headers=headers, json=payload, verify=self._ssl_verify)
                result = r.json()['result']
                if self._timestamp_fields:
                    result = self.clockFieldsConverter(result)

                return result
            except KeyError as e:
                raise Exception(r.json())
            except Exception as e:
                raise Exception(e)

        #if r.status_code != requests.codes.ok:
        #    raise Exception('API request returns status code ' + r.status_code)


    def makeApiRequest(self, method, params={}, auth=True):
        r = self.getApiRequest(method, params, auth)
        return self.doApiRequest(r)


    def getZabbixApiMethodName(self, name):
        """
        Transform "hostgroup.get" into "hostgroup_get"
        """
        return name.replace(".", "_")


    def setDateFormat(self, format):
        self._date_format = format


    def setTimestampFields(self, fields):
        self._timestamp_fields = fields


    def dateToTimestamp(self, date):
        return int(time.mktime(time.strptime(date, self._date_format)))


    def timestampToDate(self, timestamp):
        return time.strftime(self._date_format, time.localtime(int(timestamp)))


    def clockFieldsConverter(self, result):
        try:
            for idx, item in enumerate(result):
                for key, value in dict(item).items():
                    if key in self._timestamp_fields:
                        result[idx][key] = self.timestampToDate(value)
                    if isinstance(value, list):
                        result[idx][key] = self.clockFieldsConverter(value)

        except Exception as e:
            pass

        return result

