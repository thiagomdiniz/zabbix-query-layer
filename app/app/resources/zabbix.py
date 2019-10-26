from flask import request
from flask_restful import Resource, abort
from app.common.zql_engine import ZqlEngine

class Zabbix(Resource):

    __ssl_verify__ = True
    __http_auth__ = False

    def post(self):
        try:
            username = request.authorization.username
            password = request.authorization.password
        except Exception as e:
            abort(401, message="Username and Password for Basic Auth is missing! " + str(e))

        content = request.get_json()
        if not "server" in content:
            abort(400, message="Zabbix server address is missing!")
        if "options" in content:
            if "no-ssl-verify" in content["options"]:
                self.__ssl_verify__ = False
            if "http-auth" in content["options"]:
                self.__http_auth__ = True

        try:
            zql = ZqlEngine(content['server'], username, password, self.__ssl_verify__, self.__http_auth__)
        except Exception as e:
            abort(401, message="Zabbix authentication failed! " + str(e))

        content.pop('server', None)
        try:
            result = {}
            result['result'] = zql.iterate(content)
            zql.logout()
            return result
        except Exception as e:
            abort(400, message=str(e))
