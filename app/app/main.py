from flask import Flask
from flask_restful import Api
from app.resources.health import Health
from app.resources.zabbix import Zabbix

app = Flask(__name__)
api = Api(app)

api.add_resource(Health, '/health')
api.add_resource(Zabbix, '/zabbix')

