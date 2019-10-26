from flask import request
from flask_restful import Resource, abort
from app.common.zql_engine import ZqlEngine

class Zabbix(Resource):

    def post(self):
        try:
            username = request.authorization.username
            password = request.authorization.password
        except Exception as e:
            abort(401, message="Username and Password for Basic Auth is missing! " + str(e))

        content = request.get_json()
        if not "server" in content:
            abort(400, message="Zabbix server address is missing!")

        try:
            zql = ZqlEngine(content)
            zql.connectOnZabbix(username, password)
        except Exception as e:
            abort(401, message="Zabbix authentication failed! " + str(e))

        try:
            result = {}
            result['result'] = zql.execute()
            zql.logoutOfZabbix()
            return result
        except Exception as e:
            abort(400, message=str(e))
