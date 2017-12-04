import os
from flask import Flask, request
from flask_pymongo import PyMongo
from flask_pymongo import MongoClient
from datetime import datetime
import json
from bson import BSON
from bson import json_util

app = Flask('bot')


DB_NAME = "lukercio"
DB_HOST = "ds155325.mlab.com"
DB_PORT = 55325
DB_USER = "bot" 
DB_PASS = "luk100994"

connection = MongoClient(DB_HOST, DB_PORT)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)

token = 'a1s2d3f4'
#def bot():
	#print 'olar'
	

@app.route('/luizalabs/get-test', methods=['GET'])
def get_test():
	statusCode = 200

	return "Servico teste", statusCode

@app.route('/luizalabs/mensagens', methods=['GET', 'POST'])
def recebe_msg():
	if request.method == 'GET':
		if request.args.get('hub.verify_token') == token:
			return request.args.get('hub.challenge'), 200

		return "Token incorreto"

	elif request.method == 'POST':
		statusCode = 200
		retorno = 'Sucesso'

		try:
			r = db.log.insert(request.json)
		except:
			retorno = 'Erro'
			statusCode = 500

		return retorno, statusCode
		#json.dumps(r, default=json_util.default), statusCode
		#return json.dumps(restaurantes, sort_keys=True, indent=4, default=json_util.default), 200


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
