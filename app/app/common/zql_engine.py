from app.common.zql_zabbix_api import ZqlZabbixAPI

class ZqlEngine():

    _ssl_verify = True
    _http_auth = False

    def __init__(self, conf_parameters):
        self._server = conf_parameters['server']
        conf_parameters.pop('server', None)
        if "options" in conf_parameters:
            if "no-ssl-verify" in conf_parameters["options"]:
                self._ssl_verify = False
            if "http-auth" in conf_parameters["options"]:
                self._http_auth = True
        self._content = conf_parameters


    def connectOnZabbix(self, username, password):
        self.zbx_api = ZqlZabbixAPI(self._server, username, password, self._ssl_verify, self._http_auth)


    def subIterate(self, dictionary, zquery, action, pk=None, result=[]):
        for idx, z in enumerate(zquery):
            result = []
            has_params = has_pk = None
            sub_zquery = {}

            for key, value in dictionary.items():
                if not has_params and "params" in dictionary:
                    has_params = 1
                    fvalue = {**dictionary['params'], **{dictionary['fk']:z[pk]}}
                    sub_zquery = self.zbx_api.makeApiRequest(action, fvalue)
                    zquery[idx][self.zbx_api.getZabbixApiMethodName(action)] = sub_zquery
                    result += zquery
                if not has_pk and "pk" in dictionary:
                    has_pk = 1
                    self.pk = dictionary['pk']
                if key != "params" and isinstance(value, dict):
                    self.subIterate(value, sub_zquery, key, self.pk)
                    continue

        return result


    def execute(self, zbx_version_key="zabbix-version"):
        self.result = {}

        try:
            if zbx_version_key in self._content["options"]:
                self.result[zbx_version_key] = self.zbx_api.makeApiRequest('apiinfo.version', auth=False)
                self._content.pop("options", None)
            else:
                self._content.pop("options", None)
        except Exception:
            pass

        if "date-format" in self._content:
            self.zbx_api.setDateFormat(self._content["date-format"])
            self._content.pop('date-format', None)
        if "timestamp-fields" in self._content:
            self.zbx_api.setTimestampFields(self._content["timestamp-fields"])
            self._content.pop('timestamp-fields', None)

        for key, value in self._content.items():
            zquery = {}
            if "params" in value:
                zquery = self.zbx_api.makeApiRequest(key, value['params'])
            if "pk" in value:
                pk = value['pk']
                value.pop('params', None)
                value.pop('pk', None)
                for idx, action in enumerate(list(value)):
                    self.result[self.zbx_api.getZabbixApiMethodName(key)] = self.subIterate(value[action], zquery, action, pk)


            self.result[self.zbx_api.getZabbixApiMethodName(key)] = zquery

        return self.result


    def logoutOfZabbix(self):
        self.zbx_api.logout()

