from zabbix_api import ZabbixAPI
#import sys, json

class ZqlEngine():

    def __init__(self, server, username, password):
        self.login(server, username, password)


    def subIterate(self, dictionary, zquery, action, pk=None, result=[]):
        for idx, z in enumerate(zquery):
            result = []
            #print('\nSZ -> ', z, '\n', file=sys.stderr)
            has_filter = has_pk = has_instance = None

            for key, value in dictionary.items():
                if not has_filter and "filter" in dictionary:
                    has_filter = 1
                    fvalue = {**dictionary['filter'], **{dictionary['fk']:z[pk]}}
                    #print('\nSFILTER ',fvalue, '\n', file=sys.stderr)
                    sub_zquery = getattr(self.zapi, action).get(fvalue)
                    zquery[idx][action] = sub_zquery
                    result += zquery
                if not has_pk and "pk" in dictionary:
                    has_pk = 1
                    self.pk = dictionary['pk']
                if not has_instance and key != "filter" and isinstance(value, dict):
                    has_instance = 1
                    #print('\nSINSTANCE ',value, '\n', file=sys.stderr)
                    self.subIterate(value, sub_zquery, key, self.pk)
                    continue

        return result


    def iterate(self, dictionary, zbx_version_key="zabbix-version"):
        self.result = []

        if zbx_version_key in dictionary:
            self.result.append({zbx_version_key:self.zapi.api_version()})
            dictionary.pop(zbx_version_key, None)

        for key, value in dictionary.items():
            item = {}
            if "filter" in value:
                zquery = getattr(self.zapi, key).get(value['filter'])
                item[key] = zquery
            if "pk" in value:
                pk = value['pk']
                value.pop('filter', None)
                value.pop('pk', None)
                #print('\n',pk,' - ',list(value)[0],' - ',key,' - ',value[list(value)[0]],'\n', file=sys.stderr)
                item[key] = self.subIterate(value[list(value)[0]], zquery, list(value)[0], pk)

            self.result.append(item)

        return self.result


    def login(self, server, username, password):
        self.zapi = ZabbixAPI(server=server, log_level=30, timeout=60, r_query_len=10, validate_certs=False)
        self.zapi.login(username, password)


    def logout(self):
        self.zapi.logout()


