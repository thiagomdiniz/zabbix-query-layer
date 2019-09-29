from app.common.zql_zabbix_api import ZqlZabbixAPI

class ZqlEngine():

    def __init__(self, server, username, password, ssl_verify):
        self.zbx_api = ZqlZabbixAPI(server, username, password, ssl_verify)


    def subIterate(self, dictionary, zquery, action, pk=None, result=[]):
        for idx, z in enumerate(zquery):
            result = []
            has_filter = has_pk = None

            for key, value in dictionary.items():
                if not has_filter and "filter" in dictionary:
                    has_filter = 1
                    fvalue = {**dictionary['filter'], **{dictionary['fk']:z[pk]}}
                    sub_zquery = self.zbx_api.makeApiRequest(action, fvalue)
                    zquery[idx][action] = sub_zquery
                    result += zquery
                if not has_pk and "pk" in dictionary:
                    has_pk = 1
                    self.pk = dictionary['pk']
                if key != "filter" and isinstance(value, dict):
                    self.subIterate(value, sub_zquery, key, self.pk)
                    continue

        return result


    def iterate(self, dictionary, zbx_version_key="zabbix-version"):
        self.result = []

        try:
            if zbx_version_key in dictionary["options"]:
                self.result.append({zbx_version_key:self.zbx_api.makeApiRequest('apiinfo.version', auth=False)})
                dictionary.pop("options", None)
            else:
                dictionary.pop("options", None)
        except Exception:
            pass

        for key, value in dictionary.items():
            item = {}
            if "filter" in value:
                zquery = self.zbx_api.makeApiRequest(key, value['filter'])
                item[key] = zquery
            if "pk" in value:
                pk = value['pk']
                value.pop('filter', None)
                value.pop('pk', None)
                for idx, action in enumerate(list(value)):
                    item[key] = self.subIterate(value[action], zquery, action, pk)


            self.result.append(item)

        return self.result


    def logout(self):
        self.zbx_api.logout()


