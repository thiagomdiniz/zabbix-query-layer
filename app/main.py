from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort
from zql_engine import ZqlEngine

app = Flask(__name__)
api = Api(app)

class Health(Resource):

    def get(self):
        return {'message': 'alive'}


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


api.add_resource(Health, '/health')
api.add_resource(Zabbix, '/zabbix')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

