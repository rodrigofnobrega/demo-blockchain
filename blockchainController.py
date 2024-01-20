from time import time
from threading import Thread
from flask import Flask, request
from blockchain import Blockchain
import requests
import re

class Utils:
    @staticmethod
    def isValidURL(url):
        regex = r"((http|https)://(www\.)?)?([a-zA-Z0-9@:%._\+\~#?&//=]{2,256}\.[a-z]{2,6}\b|localhost)([-a-zA-Z0-9@:%._\+\~#?&//=]*)"
        
        p = re.compile(regex)

        if url is None:
            return False

        if re.search(p, url):
            return True
        else:
            return False
    
    @staticmethod
    def isValidNode(url):
        try:
            respose = requests.get(url)
            
            if respose.status_code == 200 and Utils.isValidURL(url) == True:
                return True
            else:
                return False
        except:
            return False

def apiEndPoints(app, blockchain):
    @app.route('/')
    def hello():
        return 'Blockchain'
    
    @app.route('/transactions/create', methods=['POST'])
    def createTransaction():
        tx = request.json
        
        sender = tx["sender"]
        recipient = tx["recipient"]    
        amount = tx["amount"]
        timestamp = int(time())
        privWifKey = tx["privWifKey"] 

        try:
            if (blockchain.getBitcoinAddressFromWifCompressed(privWifKey) == sender):
                blockchain.createTransaction(sender, recipient, amount, timestamp, privWifKey)
                tx["timestamp"] = timestamp

                return tx
            else:
                return "Remetente inválido"
        except AssertionError:
            return "Chave privada inválida"
        
    @app.route('/transactions/mempool', methods=['GET'])
    def getMempool():
        return blockchain.memPool
    
    @app.route('/mine', methods=['GET'])
    def mineBlock():
        blockchain.createBlock()
        blockchain.mineProofOfWork(blockchain.prevBlock)

        return blockchain.prevBlock

    @app.route('/chain', methods=['GET'])
    def getChain():
        return blockchain.chain
    
    @app.route('/nodes/register', methods=['POST'])
    def addNewNode():
        nodes_list = request.json

        for count, (key, value) in enumerate(nodes_list.items()):
            if Utils.isValidNode(value) == True:
                blockchain.nodes_api.add(value)
            else:
                return "Nó inválido"
        
        return "Nó registrado"
    
    @app.route('/nodes/list', methods=['GET'])
    def listNodes():
        available_nodes = dict()

        for count, value in enumerate(blockchain.nodes_api):
            available_nodes[count] = value
        
        return available_nodes

    @app.route('/nodes/resolve', methods=['GET'])
    def blockchainConsensus():
        tam_aux = len(blockchain.chain)
        if len(blockchain.nodes_api) == 0:
            return "Não há conexão com outros nós"
        else:
            blockchain.resolveConflicts()

        if len(blockchain.chain) > tam_aux:
            return "Chain substituída"
        else:
            return "Chain mantida"

def runApi(port):
    app = Flask(__name__)
    blockchain = Blockchain()

    apiEndPoints(app, blockchain)

    app.run(port=port)

if __name__ == '__main__':
    ports = [5000, 5001]

    threads = []  

    for port in ports:
        thread = Thread(target=runApi, args=(port,))
        
        threads.append(thread)

    for thread in threads:
        thread.start()
