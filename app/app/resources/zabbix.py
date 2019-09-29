from flask import request
from flask_restful import Resource, abort
from app.common.zql_engine import ZqlEngine

class Zabbix(Resource):

    def post(self):
        try:
            username = request.authorization.username
            password = request.authorization.password
        except:
            abort(401, message="Username and Password for Basic Auth is missing!")

        content = request.get_json()
        if not "server" in content:
            abort(500, message="Zabbix server address is missing!")

        try:
            zql = ZqlEngine(content['server'], username, password)
        except:
            abort(401, message="Zabbix authentication failed")

        content.pop('server', None)
        result = zql.iterate(content)
        zql.logout()
        return result
