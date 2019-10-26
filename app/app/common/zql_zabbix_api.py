import requests
from base64 import b64encode

class ZqlZabbixAPI():

    __jsonrpc_url__ = '/api_jsonrpc.php'
    __auth_token__ = None
    __url__ = None
    __ssl_verify__ = True
    __basic_auth__ = None

    def __init__(self, address, username, password, ssl_verify=True, http_auth=False):
        self.__url__ = address + self.__jsonrpc_url__
        self.__ssl_verify__ = ssl_verify
        if http_auth:
            self.__basic_auth__ = b64encode(bytes(username + ':' + password, "utf-8")).decode("ascii")
        self.__auth_token__ = self.login(username, password)


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
            request = {'jsonrpc': jsonrpc,
                        'method': method,
                        'params': params,
                        'auth': self.__auth_token__,
                        'id': id}
            if not auth:
                del request['auth']

            return request
        else:
            raise Exception('API method name is missing!')


    def doApiRequest(self, payload):
        headers = {'Content-Type': 'application/json-rpc',
                    'User-Agent': 'python/zql'}
        if self.__basic_auth__:
            headers['Authorization'] = 'Basic %s' % self.__basic_auth__

        if payload:
            try:
                r = requests.post(self.__url__, headers=headers, json=payload, verify=self.__ssl_verify__)
                return r.json()['result']
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
        Transform "hostgroup.get" into "hostgroup"
        """
        return name.split(".")[0]

