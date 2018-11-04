from flask import Flask, request
import json
import requests
import logging
import xmltodict
import inspect
from Blockchain_classes.Blockchain import Blockchain
from Blockchain_classes.Block import Block
import Utilities.Utility as Utility
import User_classes.User as User
import Mining_classes.Variables as variables
blockchain = None
node = Flask(__name__)
def start():
    global node,blockchain
    genesis = Utility.create_genesis_block()
    blockchain = Blockchain(genesis.index,genesis.timemade,genesis.proof_of_work,genesis.effort,genesis.transactions,genesis.previous_hash)
    node.config['SECRET_KEY'] = Utility.createHexdigest(User.password)
    node.run(host="0.0.0.0", port=variables.PORT)






log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@node.route('/lastblock', methods=['GET','POST'])
def lastblock():
    global blockchain
    block = blockchain.last_added()
    return block.exportXml()

@node.route('/numblocks', methods=['POST'])
def numblocks():
    global blockchain
    return blockchain.num_added()

@node.route('/block', methods=['GET','POST'])
def block():
    global blockchain
    ip = request.remote_addr
    if request.method == 'POST':

        raw = request.data.decode('utf-8')
        parsed = xmltodict.parse(raw)
        b = Block()
        b.importXml(parsed['block'])
        blockchain.add(b.index,b.timemade,b.proof_of_work,b.effort,b.transactions,b.previous_hash)

    else:
        block_number = str(int(request.args['block_number']))
        print(ip, block_number)

    return "0\n"