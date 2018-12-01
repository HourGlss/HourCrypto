import requests
import time
import xmltodict
from Blockchain_classes.Block import Block
import Mining_classes.Variables as Variables
import Utilities.Utility as Utility
import User_classes.User as User

import inspect
import logging


def proof_of_work(last_block,data):
    func = inspect.currentframe().f_back.f_code
    done = False
    now = None
    pow_hash_object = None
    effort = None
    while not done:
        now = time.time()
        index_to_use = last_block.index + 1
        effort, pow_hash_object = Utility.genhash(index_to_use, now, data, last_block.hash)
        leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
        if leading_zeroes >= Variables.WORK:
            done = True
    return_block = Block(index_to_use, now, pow_hash_object.hexdigest(), effort, data, last_block.hash)
    return return_block


def get_last_block():
    url = "http://" + Variables.MINER_NODE_URL + ":" + str(Variables.PORT) + "/lastblock"
    last_block_xml = requests.post(url)
    parsed = xmltodict.parse(last_block_xml.content)
    last_block = Block()
    last_block.import_from_xml(parsed['block'])
    return last_block


def mine():
    func = inspect.currentframe().f_back.f_code
    while True:
        transactions = [{"from": "network", "to": User.public_key, "amount": 1}]
        # TODO get REAL transactions from transaction db
        last_block = get_last_block()
        pow_output = proof_of_work(last_block,transactions)
        transactions = [{}]
        url = "http://" + Variables.MINER_NODE_URL + ":" + str(Variables.PORT) + "/block"
        xml = pow_output.export_to_xml()
        headers = {'Content-Type': 'application/xml'}
        resp = requests.post(url, data=xml, headers=headers).text
