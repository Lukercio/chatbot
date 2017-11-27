import os
from flask import Flask, jsonify, request

app = Flask(__name__)

data = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/luizalabs/get-test', methods=['GET'])
def get_test():
    return jsonify({'test': data})

@app.route('/luizalabs/mensagens', methods=['POST'])
def recebe_msg():
	if not request.json or not 'title' in request.json:
		abort(400)

#	request.json.append(request.json)

	return jsonify({'OK': request.json}), 201

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
