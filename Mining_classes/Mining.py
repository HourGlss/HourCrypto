import requests
import time
import xmltodict
from Blockchain_classes.Block import Block
import Mining_classes.Variables as variables
import Utilities.Utility as Utility
import User_classes.User as User
import sys

import inspect
import logging
def proof_of_work(last_block, data):
    index_to_use = last_block.index + 1
    func = inspect.currentframe().f_back.f_code
    logging.info("Starting proof of work")
    done = False
    while not done:
        now = time.time()
        effort, pow_hash_object = Utility.genhash(index_to_use, now, data, last_block.hash)
        leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
        if leading_zeroes >= variables.WORK:
            done = True
    retBlock = Block(index_to_use, now, pow_hash_object.hexdigest(), effort, data, last_block.hash)
    logging.info("Farmed a block returning: {}".format(retBlock))
    return retBlock


def mine():
    func = inspect.currentframe().f_back.f_code
    logging.info("Starting to mine")
    # See if other blockchains exist
    #TODO add consensus back
    i = 0
    while i < 10:
        url = "http://" + variables.MINER_NODE_URL + ":" + str(variables.PORT) + "/lastblock"
        last_block_xml = requests.post(url)
        parsed = xmltodict.parse(last_block_xml.content)
        print(last_block_xml.content.decode('utf-8'))
        last_block = Block()
        last_block.importXml(parsed['block'])
        transactions = {"from":"network","to":User.public_key,"amount":1}
        pow_output = proof_of_work(last_block,transactions)
        url = "http://" + variables.MINER_NODE_URL + ":" + str(variables.PORT) + "/block"
        xml = pow_output.exportXml()
        headers = {'Content-Type': 'application/xml'}
        requests.post(url, data=xml, headers=headers).text
        sys.exit()
        i+=1
