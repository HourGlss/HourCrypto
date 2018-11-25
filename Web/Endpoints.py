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
import Mining_classes.Variables as Variables

blockchain = None
node = Flask(__name__)


def consensus():
    for ip in Variables.PEER_NODES:
        pass


def start():
    global node, blockchain
    if not len(Variables.PEER_NODES) > 0:
        genesis = Utility.create_genesis_block()
        blockchain = Blockchain(genesis)
    else:
        blockchain = consensus()
    node.config['SECRET_KEY'] = Utility.createHexdigest(User.password)
    node.run(host="0.0.0.0", port=Variables.PORT)


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@node.route('/numblocks', methods=['GET','POST'])
def numblocks():
    global blockchain
    return str(blockchain.num_added())

@node.route('/lastblock', methods=['GET', 'POST'])
def lastblock():
    global blockchain
    block = blockchain.last_added()
    return block.export_to_xml()

@node.route('/block', methods=['GET', 'POST'])
def block():
    global blockchain
    ip = request.remote_addr
    if request.method == 'POST':

        raw = request.data.decode('utf-8')
        parsed = xmltodict.parse(raw)
        b = Block()
        b.import_from_xml(parsed['block'])
        blockchain.add(b)
    else:
        block_number = str(int(request.args['block_number']))

    return "0\n"
