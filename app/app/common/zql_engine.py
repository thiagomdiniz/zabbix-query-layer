from app.common.zql_zabbix_api import ZqlZabbixAPI

class ZqlEngine():

    _ssl_verify = True
    _http_auth = False

    def __init__(self, conf_parameters):
        self._content = conf_parameters


    def initProcess(self):
        try:
            if "zabbix-version" in self._content["options"]:
                self.result["zabbix-version"] = self.zbx_api.makeApiRequest('apiinfo.version', auth=False)
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


    def connectOnZabbix(self, username, password):
        self._server = self._content['server']
        self._content.pop('server', None)

        if "options" in self._content:
            if "no-ssl-verify" in self._content["options"]:
                self._ssl_verify = False
            if "http-auth" in self._content["options"]:
                self._http_auth = True

        self.zbx_api = ZqlZabbixAPI(self._server, username, password, self._ssl_verify, self._http_auth)


    def logoutOfZabbix(self):
        self.zbx_api.logout()


    def subIterate(self, dictionary, zbx_api_response, action, pk=None, fk_list=None, result=[]):
        if fk_list:
            result = []
            has_params = has_pk = None
            sub_zbx_api_response = {}

            for key, value in dictionary.items():
                if not has_params and "params" in dictionary:
                    has_params = 1
                    fvalue = {**dictionary['params'], **{dictionary['fk']:zbx_api_response}}
                    sub_zbx_api_response = self.zbx_api.makeApiRequest(action, fvalue)
                    if not "hidden" in dictionary:
                        result += sub_zbx_api_response
                if not has_pk and "pk" in dictionary:
                    has_pk = 1
                    self.pk = dictionary['pk']
                if key != "params" and isinstance(value, dict):
                    if "hidden" in dictionary:
                        zbx_api_response_ids_list = [k[self.pk] for k in sub_zbx_api_response]
                        self.top_result_method_name = self.zbx_api.getZabbixApiMethodName(key)
                        result += self.subIterate(value, zbx_api_response_ids_list, key, self.pk, fk_list=1)
                        continue
                    else:
                        self.subIterate(value, sub_zbx_api_response, key, self.pk)
                        continue
        else:
            for idx, z in enumerate(zbx_api_response):
                result = []
                has_params = has_pk = None
                sub_zbx_api_response = {}

                for key, value in dictionary.items():
                    if not has_params and "params" in dictionary:
                        has_params = 1
                        fvalue = {**dictionary['params'], **{dictionary['fk']:z[pk]}}
                        sub_zbx_api_response = self.zbx_api.makeApiRequest(action, fvalue)
                        if not "hidden" in dictionary:
                            zbx_api_response[idx][self.zbx_api.getZabbixApiMethodName(action)] = sub_zbx_api_response
                            result += zbx_api_response
                    if not has_pk and "pk" in dictionary:
                        has_pk = 1
                        self.pk = dictionary['pk']
                    if key != "params" and isinstance(value, dict):
                        if "hidden" in dictionary:
                            zbx_api_response_ids_list = [k[self.pk] for k in sub_zbx_api_response]
                            zbx_api_response[idx].update([(self.zbx_api.getZabbixApiMethodName(key), self.subIterate(value, zbx_api_response_ids_list, key, self.pk, fk_list=1))])
                            result += zbx_api_response
                            continue
                        else:
                            result += zbx_api_response
                            self.subIterate(value, sub_zbx_api_response, key, self.pk)
                            continue

        return result


    def execute(self):
        self.result = {}
        self.initProcess()

        for zbx_api_method, value in self._content.items():
            zbx_api_response = {}
            hidden = None
            if "hidden" in value:
                hidden = 1
                value.pop('hidden', None)
            if "params" in value:
                zbx_api_response = self.zbx_api.makeApiRequest(zbx_api_method, value['params'])
            if "pk" in value:
                pk = value['pk']
                value.pop('params', None)
                value.pop('pk', None)
                if hidden:
                    zbx_api_response_ids_list = [k[pk] for k in zbx_api_response]
                    for idx, action in enumerate(list(value)):
                        self.top_result_method_name = self.zbx_api.getZabbixApiMethodName(action)
                        result = self.subIterate(value[action], zbx_api_response_ids_list, action, pk, fk_list=1)
                        self.result.update([(self.top_result_method_name, result)])
                else:
                    for idx, action in enumerate(list(value)):
                        self.result[self.zbx_api.getZabbixApiMethodName(zbx_api_method)] = self.subIterate(value[action], zbx_api_response, action, pk)
            else:
                self.result[self.zbx_api.getZabbixApiMethodName(zbx_api_method)] = zbx_api_response

        return self.result

