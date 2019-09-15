from __future__ import print_function
from flask_restful import abort
from zabbix_api import ZabbixAPI
import sys, json

class ZqlEngine():

    def subIterate(self, dictionary, zquery, action, pk=None, zzquery=[]):
        for idx, z in enumerate(zquery):
            zzquery = []
            print('\nSZ -> ', z, '\n', file=sys.stderr)
            hf = hp = hi = None

            for key, value in dictionary.items():
                if not hf and "filter" in dictionary:
                    hf = 1
                    fvalue = {**dictionary['filter'], **{dictionary['fk']:z[pk]}}
                    print('\nSFILTER ',fvalue, '\n', file=sys.stderr)
                    szquery = getattr(self.zapi, action).get(fvalue)
                    zquery[idx][action] = szquery
                    zzquery += zquery
                if not hp and "pk" in dictionary:
                    hp = 1
                    self.pk = dictionary['pk']
                if not hi and key != "filter" and isinstance(value, dict):
                    hi = 1
                    print('\nSINSTANCE ',value, '\n', file=sys.stderr)
                    self.subIterate(value, szquery, key, self.pk)
                    continue

        return zzquery


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
                print('\n',pk,' - ',list(value)[0],' - ',key,' - ',value[list(value)[0]],'\n', file=sys.stderr)
                item[key] = self.subIterate(value[list(value)[0]], zquery, list(value)[0], pk)

            self.result.append(item)

        return self.result


    def login(self, server, username, password):
        self.zapi = ZabbixAPI(server=server, log_level=30, timeout=60, r_query_len=10, validate_certs=False)
        try:
            self.zapi.login(username, password)
        except:
            abort(401, message="Zabbix authentication failed")


    def logout(self):
        self.zapi.logout()


