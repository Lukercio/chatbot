import os
import requests
import traceback
import json
from flask import Flask, request
from flask_pymongo import PyMongo
from flask_pymongo import MongoClient
from datetime import datetime
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
tokenResposta = 'EAACJur8NjScBAAOJ4618XnXLHvenZAX5QM7ZAvlZCRljMzZCNjQDYQ58cbri6yr19d7abCncc8AyEbwsw1hISw0mZBZADXZBlbb61SbhNiZCZA4ZCSyQonvli6GvXkC6PfcjnVrt6oTmLkCVtHV19hetos6ZAxwcn5ZCA7ZAoiK5BFkzh4wZDZD'
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

			metadata = json.loads(request.data.decode())
			texto = metadata['entry'][0]['messaging'][0]['message']['text']
			remetente = metadata['entry'][0]['messaging'][0]['sender']['id']
			resposta = {'recipient': {'id': remetente}, 'message': {'text': "Como posso ajudar?"}}
			ret = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + tokenResposta, json=resposta)

		except:
			retorno = 'Erro'
			statusCode = 500

		return retorno, statusCode
		#json.dumps(r, default=json_util.default), statusCode
		#return json.dumps(restaurantes, sort_keys=True, indent=4, default=json_util.default), 200


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
