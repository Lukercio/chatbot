import os
import traceback
import json
import io
import requests
import http.client, urllib.request, urllib.parse, urllib.error, base64, json
#import httplib, urllib, base64
#from nltk.chat.util import Chat, reflections
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
subscription_key = '29120edd1c5e49afb6a5c7ee489e264a'
uri_base = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0'


buscaML = 'http://www.magazineluiza.com.br/produtos/autocomplete/'

headers = {
	'Content-Type': 'application/json',
	'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.urlencode({
	'visualFeatures': 'description',
	'language': 'en',
})

GREETING_KEYWORDS = ("oi", "ola", "eae", "tudo bem", "?")
GREETING_RESPONSES = ["Ola, sou o vendedor virtual, me informe o nome de um produto ou uma imagem dele", "oi", "ola", "O que deseja comprar?"]
OTHER_RESPONSES = ("Desculpe, nao entendi.", "Por enquanto apenas ajudo na compra de produtos", "Desculpe, ainda nao realizo esse tipo de tarefa", "Desculpe, apenas consigo te auxiliar em uma compra")
NOPRODUCT_RESPONSES = ("Me informe um produto", "Nao sei se consigo ajudar, me informe um produto", "Qual produto deseja?", "Me mande uma foto do produto")

def identificaProduto(imagemUrl):
	headers = {
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': subscription_key,
	}

	params = urllib.urlencode({
		'visualFeatures': 'description',
		'language': 'en',
	})

	retorno = 'Desconhecido'
	body = "{'url': '" + imagemUrl + "'}"

	try: 
		# Verifica significado imagem
		conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
		conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
		response = conn.getresponse()
		data = response.read()

		parsed = json.loads(data)
		print ("Response:")
		print (json.dumps(parsed, sort_keys=False, indent=2))
		conn.close()

	except: 
		return 'erro'

	return json.dumps(parsed, sort_keys=False, indent=2)

def linkBuscaML(produto):
	busca_endpoint = linkBuscaML + produto + '.json'

def bot(texto, produto):

	if produto == None:
		retorno = random.choice(NOPRODUCT_RESPONSES)

	else:
		for word in texto.words:
			if word.lower() in GREETING_KEYWORDS:
				retorno = random.choice(GREETING_RESPONSES)

		link = linkBuscaML(produto)
		retorno = retorno + link


	return retorno


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
		#return identificaProduto('https://scontent-iad3-1.xx.fbcdn.net/v/t35.0-12/24726147_1641730655848963_260168319_o.jpg?_nc_ad=z-m&_nc_cid=0&oh=c85115f4a6bf04b5010027c07c3900a3&oe=5A26ABD8')

		try:
			print ('00000')
			r = db.log.insert(request.json)
			print ('0001')
			metadata = json.loads(request.data.decode())
			print ('00002')
			print (metadata)
			print (request.json)


			print ('00003')
			if metadata["object"] == "page":
				print ('00004')
				for entry in metadata["entry"]:
					print ('0005')
					for messaging_event in entry["messaging"]:
						print ('0006')
						if messaging_event.get("message"):  
							print ('0007')
						
			print ('0008')
			
			#produto = identificaProduto(imagemUrl)
			#print produto
			mensagem = "ola, tudo certo?"
			#mensagem = bot(texto, produto)

			print ('Lukercio')
			remetente = metadata['entry'][0]['messaging'][0]['sender']['id']
			print ('lukercio2')
			resposta = {'recipient': {'id': remetente}, 'message': {'text': mensagem}}
			print (resposta)
			print ('lukercio3')
			ret = request.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + tokenResposta, json=resposta)
			# headers = {
			# 	'Content-Type': 'application/json',
			# }

			# conn = httplib.HTTPSConnection('https://graph.facebook.com/v2.6/me/messages/?access_token=' + tokenResposta)
			# conn.request("POST", "%s" % tokenResposta, resposta, headers)
			# response = conn.getresponse()
			# data = response.read()

			# parsed = json.loads(data)
			# print ("Response:")
			# print (json.dumps(parsed, sort_keys=False, indent=2))
			# conn.close()


			print ('lukercio4')

		except Exception as e:
			retorno = 'Erro'
			statusCode = 500
			print (e)

		return retorno, statusCode
		#json.dumps(r, default=json_util.default), statusCode
		#return json.dumps(restaurantes, sort_keys=True, indent=4, default=json_util.default), 200


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
