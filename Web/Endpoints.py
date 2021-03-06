from flask import Flask, request, render_template
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
import Mining_classes.Mining as Mining

from multiprocessing import Process

blockchain = None
node = Flask(__name__)
mining_process = None
event = None

def consensus():
    global blockchain
    max = 0
    max_ip = None
    for ip in Variables.PEER_NODES:
        url = "http://" + ip + ":" + str(Variables.PORT) + "/numblocks"
        numblocks = requests.post(url)
        numblocks = int(numblocks.content.decode('utf-8'))
        if numblocks > max:
            max = numblocks
            max_ip = ip
    for i in range(0,max):
        url = "http://" + max_ip + ":" + str(Variables.PORT) + "/block?block_number={}".format(i)
        block_xml = requests.post(url)
        parsed = xmltodict.parse(block_xml.content)
        block = Block()
        block.import_from_xml(parsed['block'])
        if blockchain is None:
            blockchain = Blockchain(block)
        else:
            blockchain.add(block)




def start(e):
    global node, blockchain,mining_process,event
    if not len(Variables.PEER_NODES) > 0:
        genesis = Utility.create_genesis_block()
        blockchain = Blockchain(genesis)
    else:
        consensus()

    event = e
    mining_process = Process(target=Mining.mine, args=(event,))
    mining_process.start()
    logging.debug("Mining_classes Started")
    node.config['SECRET_KEY'] = Utility.createHexdigest(User.password)
    node.run(host="0.0.0.0", port=Variables.PORT)


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@node.route('/numblocks', methods=['GET','POST'])
def numblocks():
    ip = request.remote_addr
    if ip != "127.0.0.1" and ip not in Variables.PEER_NODES:
        Variables.PEER_NODES.append(ip)
    global blockchain
    return str(blockchain.num_added())

@node.route('/lastblock', methods=['GET', 'POST'])
def lastblock():
    global blockchain
    ip = request.remote_addr
    if ip != "127.0.0.1" and ip not in Variables.PEER_NODES:
        Variables.PEER_NODES.append(ip)
    if ip == "127.0.0.1":
        block = blockchain.last_added()
        return block.export_to_xml()
    return "0"

@node.route('/block', methods=['POST'])
def block():

    global blockchain
    ip = request.remote_addr
    if ip != "127.0.0.1" and ip not in Variables.PEER_NODES:
        Variables.PEER_NODES.append(ip)
    if ip == '127.0.0.1':
        raw = request.data.decode('utf-8')
        parsed = xmltodict.parse(raw)
        b = Block()
        b.import_from_xml(parsed['block'])
        print("I made", b)
        blockchain.add(b)

        #Distribute the block to our peers

        for peer in Variables.PEER_NODES:
            try:
                url = "http://" + peer + ":" + str(Variables.PORT) + "/block"
                xml = b.export_to_xml()
                headers = {'Content-Type': 'application/xml'}
                resp = requests.post(url, data=xml, headers=headers).text
            except:
                Variables.PEER_NODES.remove(peer)
    else:
        block_number = None

        try:
            block_number = int(request.args['block_number'])
        except:
            pass
        if block_number is not None:
            return blockchain.get(block_number).export_to_xml()
        else:
            raw = request.data.decode('utf-8')
            parsed = xmltodict.parse(raw)
            b = Block()
            b.import_from_xml(parsed['block'])
            print("receiv", b)
            if Utility.validate(b):
                blockchain.add(b)
                global event
                event.set()
            else:
                print("Block did not validate",ip)
    return "0"
