import datetime
import json
import hashlib
from flask import Flask, jsonify

class Blockchain:
	def __init__(self):
		self.chain = []
		self.createblock(proof = 1, prevhash = "0")

	def createblock(self, proof, prevhash):
		block = {'index': len(self.chain) + 1,
				 'timestamp': str(datetime.datetime.now()),
				 'proof': proof,
				 'prevhash': prevhash}

		self.chain.append(block)
		return block

	def getprevblock(self):
		return self.chain[-1]

	def proofofwork(self, prevproof):
		newproof = 1
		checkproof = False
		# Defining crypto puzzle for the miners and iterating until able to mine it
		while checkproof is False:
			op = hashlib.sha256(str(newproof**2 - prevproof**5).encode()).hexdigest()
			if op[:5] == "00000":
				checkproof = True
			else:
				newproof += 1
		return newproof

	def hash(self, block):
		encodedblock = json.dumps(block, sort_keys = True).encode()
		return hashlib.sha256(encodedblock).hexdigest()
	def ischainvalid(self, chain):
		prevblock = chain[0]   # Initilized to Genesis block
		blockindex = 1         # Initilized to Next block
		while blockindex < len(chain):

			currentblock = chain[blockindex]
			if currentblock['prevhash'] != self.hash(prevblock):
				return False

			prevproof = prevblock['proof']
			currentproof = currentblock['proof']
			op = hashlib.sha256(str(currentproof**2 - prevproof**5).encode()).hexdigest()

			if op[:5] != "00000":
				return True
			prevblock = currentblock
			blockindex += 1
		return True

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/', methods=['GET'])
def welcome():
	wl = '''
		<html>
		<head><title>Spyder</title></head>
		<body>
		<h1>Spyder Blockchain</h1>
		Welcome to our Blockchain Page
		<br>Lets Go !!!
		<br>
			<ul>
			<li>For Mining Blocks Visit : <a href="http://127.0.0.1:5000/mineblock">http://127.0.0.1:5000/mineblock</a></li>
			<li>For Viewing the Blockchain Visit : <a href="http://127.0.0.1:5000/getchain">http://127.0.0.1:5000/getchain</a></li>
			<li>For Validating Blockchain Visit : <a href="http://127.0.0.1:5000/validate">http://127.0.0.1:5000/validate</a></li>
			</ul>
		</body>
		</html>
		'''
	return wl

@app.route('/mineblock', methods=['GET'])
def mineblock():
	prevblock = blockchain.getprevblock()
	prevproof = prevblock['proof']
	proof = blockchain.proofofwork(prevproof)
	prevhash = blockchain.hash(prevblock)
	block = blockchain.createblock(proof, prevhash)
	response = {'message': "Congratulations, You just mined a block !",
				'index': block['index'],
				'timestamp': block['timestamp'],
				'proof': block['proof'],
				'prevhash': block['prevhash']}
	return jsonify(response), 200

@app.route('/getchain', methods=['GET'])
def getchain():
	response = {'chain': blockchain.chain,
				'len': len(blockchain.chain)}
	return jsonify(response), 200

@app.route('/validate', methods=['GET'])
def validate():
	if blockchain.ischainvalid(blockchain.chain):
		response = {'message': "The Blockchain is Valid"}
	else:
		response = {'message': "The Blockchain is Invalid"}
	return jsonify(response), 200

app.run(host='0.0.0.0', port=5000)