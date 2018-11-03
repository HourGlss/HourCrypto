import requests
import json
import time
from Blockchain_classes.Block import Block
import Mining_classes.Variables as variables
import Utilities.Utility as Utility
import User_classes.User as User

import inspect
import logging


def consensus():
    #TODO Remake consensus, possible shift into endpoints
    pass


def find_new_chains():
    #TODO Remake find_new_chains using restructure
    pass





def proof_of_work(a, last_block, data):
    func = inspect.currentframe().f_back.f_code
    logging.info("Starting proof of work")
    start = time.time()

    interval = 5*60
    now = time.time() + 1
    effort, pow_hash_object = Utility.genhash(last_block.index + 1, time.time(), data, last_block.hash)
    leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
    while leading_zeroes <= variables.WORK:
        now = time.time() + 1
        if int(now - start) % interval + 1 == 0:
            start = time.time()
            consensus = consensus()
            if consensus:
                logging.info("Received a consensus while doing POW")
                return False, consensus
        effort, pow_hash_object = Utility.genhash(last_block.index + 1, now, data, last_block.hash)
        leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
    retBlock = Block(last_block.index + 1, now, pow_hash_object.hexdigest(), effort, data, last_block.hash)
    logging.info("Farmed a block returning: {}".format(retBlock))
    return True, retBlock


def mine():
    func = inspect.currentframe().f_back.f_code
    logging.info("Starting to mine")
    # See if other blockchains exist
    #TODO add consensus back
    while True:
        url = "http://" + variables.MINER_NODE_URL + ":" + str(variables.PORT) + "/lastblock"
        last_block_xml = requests.post(url)
        last_block = variables.BLOCKCHAIN[len(variables.BLOCKCHAIN) - 1]
        #   -get transactions
        url = "http://" + variables.MINER_NODE_URL + ":" + str(variables.PORT) + "/txion?update=" + User.public_key
        logging.debug("Getting transactions from {}".format(url))
        transactions = requests.get(url).content
        logging.debug("Done getting transactions")
        variables.PENDING_TRANSACTIONS = json.loads(transactions)
        logging.warning("type of transaction: {}".format(type(variables.PENDING_TRANSACTIONS)))
        variables.PENDING_TRANSACTIONS.append({
            "from": "network",
            "to": User.public_key,
            "amount": 1.0})
        # mine using the updated blockchain
        pow, pow_output = proof_of_work(a, last_block, variables.PENDING_TRANSACTIONS)
        variables.PENDING_TRANSACTIONS = []
        if pow:
            logging.info("Mined a block {}".format(pow_output))
            variables.BLOCKCHAIN.append(pow_output)
        else:
            logging.info("Consensus returned a blockchain {}".format(pow_output))
            variables.BLOCKCHAIN = pow_output
        logging.debug("Adding that blockchain to the Queue")
        a.put(["mine", variables.BLOCKCHAIN])
        url = "http://" + variables.MINER_NODE_URL + ":" + str(variables.PORT) + "/blocks?update=" + User.public_key
        logging.debug("accessing url via GET")
        requests.get(url)
        logging.debug("Done accessing url")
