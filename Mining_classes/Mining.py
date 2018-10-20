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
    func = inspect.currentframe().f_back.f_code
    logging.info("Starting Consensus")
    peers = variables.PEER_NODES
    logging.debug("Peers: {}".format(peers))
    if len(peers) == 0:
        logging.info("Ending consensus, we have no peers")
        return False

    # Get the blocks from other nodes
    other_chains = find_new_chains()
    if len(other_chains) == 0:
        logging.debug("no chains found")
        logging.info("Ending consensus, no other chains found")
        return False
    if type(other_chains[0]) != type([]):
        if len(other_chains) < len(variables.BLOCKCHAIN):
            logging.debug("Our blockchain is bigger")
            logging.info("Ending consensus, rejecting others")
            return False
        else:
            logging.info("Ending consensus, we have one peer with a longer blockchain")

            return other_chains
    # If our chain isn't longest, then we store the longest chain
    longest = 0
    max_length = 0
    for i in range(len(other_chains)):
        if Utility.validate_blockchain(other_chains[i]):
            chain_length = len(other_chains[i])
            if chain_length > max_length:
                max_length = chain_length
                longest = i
    if len(other_chains[longest]) == len(variables.BLOCKCHAIN):
        logging.debug("Our blockchain is the same size1")
        logging.info("Ending consensus, rejecting others")
        return False
    logging.info("Ending Consensus with a chain")
    logging.debug("Consensus returned: {}".format(other_chains[longest]))
    return other_chains[longest]


def find_new_chains():
    func = inspect.currentframe().f_back.f_code
    logging.info("Starting to find new chains")
    # Get the blockchains of every other node
    peers = variables.PEER_NODES
    logging.debug("peers: {}".format(len(peers)))
    other_chains = []
    for node_url in peers:

        blockchain_json = None
        found_blockchain = []

        url = "http://" + node_url + ":" + str(variables.PORT) + "/blocks"
        try:
            logging.debug("Attempting to access {}".format(node_url))
            blockchain_json = requests.post(url)
        except:
            logging.warning("Failed to access {}, removing from peers".format(node_url))
            variables.PEER_NODES.remove(node_url)
            continue
        # Convert the JSON object to a Python dictionary
        if blockchain_json is not None:
            blockchain_json = json.loads(blockchain_json.content)
            for block_json in blockchain_json:
                temp = Block()
                temp.importjson(block_json)
                if Utility.validate(temp):
                    logging.debug("Block validated, adding")
                    found_blockchain.append(temp)
                else:
                    logging.warning("Block NOT valid, next peer")
                    continue
            # Verify other node block is correct
            logging.debug("Attempting to validate this: {}".format(found_blockchain))
            validated = Utility.validate_blockchain(found_blockchain)
            if validated:
                logging.debug("Blockchain_classes did validate")
                other_chains.append(found_blockchain)
            else:
                logging.warning("Blockchain_classes did not validate")
            continue
    logging.info("Ending find new chains")
    return other_chains





def proof_of_work(a, last_block, data):
    func = inspect.currentframe().f_back.f_code
    logging.info("Starting proof of work")
    start = time.time()

    #TODO this should probably be... maybe 15 * 60
    interval = 20
    now = time.time() + 1
    effort, pow_hash_object = Utility.genhash(last_block.index + 1, time.time(), data, last_block.hash)
    leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
    while leading_zeroes <= variables.WORK:
        now = time.time() + 1
        if int(now - start) % interval + 1 == 0:
            logging.debug("Checking for messages")
            messages = []
            while not a.empty():
                obj = a.get()
                logging.debug("Got {} from queue".format(obj))
                messages.append(obj)
            for message in messages:
                if message[0] == "ip":
                    logging.debug("That's an ip {} adding to peers".format(message[1]))
                    variables.PEER_NODES.append(str(messages[1]))
                    continue
                logging.debug("not an IP, putting it back message:{}".format(message))
                a.put(message)
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


def mine(a):
    func = inspect.currentframe().f_back.f_code
    logging.info("Starting to mine")
    # See if other blockchains exist
    blockchain = consensus()
    if not blockchain:
        logging.info("Didn't receive a blockchain from anyone and need to make one")
        # We didn't find one, need to make one
        variables.BLOCKCHAIN.append(Utility.create_genesis_block())
    else:
        logging.info("Received a blockchain from the net")
        # See if we got any blocks from someone, save it
        variables.BLOCKCHAIN = blockchain
    message = Utility.buildmessage("blockchain", variables.BLOCKCHAIN)
    logging.debug("Adding {} to queue".format(message))
    a.put(message)
    url = "http://" + variables.MINER_NODE_URL + ":" + str(variables.PORT) + "/blocks?update=" + User.public_key
    logging.debug("accessing url via GET")
    requests.get(url)
    logging.debug("Done accessing url")
    while True:
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
