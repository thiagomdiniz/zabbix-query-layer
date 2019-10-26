from app.common.zql_zabbix_api import ZqlZabbixAPI

class ZqlEngine():

    def __init__(self, server, username, password, ssl_verify, http_auth):
        self.zbx_api = ZqlZabbixAPI(server, username, password, ssl_verify, http_auth)


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


    def iterate(self, dictionary, zbx_version_key="zabbix-version"):
        self.result = {}

        try:
            if zbx_version_key in dictionary["options"]:
                self.result[zbx_version_key] = self.zbx_api.makeApiRequest('apiinfo.version', auth=False)
                dictionary.pop("options", None)
            else:
                dictionary.pop("options", None)
        except Exception:
            pass

        for key, value in dictionary.items():
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


    def logout(self):
        self.zbx_api.logout()

