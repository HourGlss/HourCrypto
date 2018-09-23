import requests
import json
import time
from Mining.Block import Block
import Mining.Variables as variables
import Utilities.Utility as Utility
import User.User as User


def consensus():
    peers = variables.PEER_NODES
    if len(peers) == 0:
        return False


    # Get the blocks from other nodes
    other_chains = find_new_chains()
    if len(other_chains) == 0:
        print("no chains found")
        return False
    if type(other_chains[0]) != type([]):
        if len(other_chains) < len(variables.BLOCKCHAIN):
            return False
        else:
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
        return False
    return other_chains[longest]


def find_new_chains():
    # Get the blockchains of every other node
    peers = variables.PEER_NODES
    other_chains = []
    for node_url in peers:

        blockchain_json = None
        found_blockchain = []
        url = "http://" + node_url + ":" + str(variables.PORT) + "/blocks"
        blockchain_json = requests.post(url)
        # Convert the JSON object to a Python dictionary
        if blockchain_json is not None:
            blockchain_json = json.loads(blockchain_json.content)
            for block_json in blockchain_json:
                temp = Block()
                temp.importjson(block_json)
                if Utility.validate(temp):
                    found_blockchain.append(temp)
            # Verify other node block is correct
            validated = Utility.validate_blockchain(found_blockchain)
            if validated:
                other_chains.append(found_blockchain)
            continue
    return other_chains


def create_genesis_block():
    """To create each block, it needs the hash of the previous one. First
    block has no previous, so it must be created manually (with index zero
     and arbitrary previous hash)"""
    work_ez = int(variables.WORK / 4) + 1
    pow = "0" * work_ez
    pad = "1337"
    for i in range(4, 64):
        pow += pad[i % len(pad)]
    b = Block(0, time.time(), pow, "e", [],
              "0")
    b.data=[{"FROM": 0,"TO":0,"AMOUNT":0}]
    return b


def proof_of_work(a, last_block, data):
    start = time.time()
    interval = 20
    effort, pow_hash_object = Utility.genhash(last_block.index + 1, time.time(), data, last_block.hash)
    leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
    while leading_zeroes < variables.WORK:
        now = time.time() + 1
        if int(now - start) % interval + 1 == 0:
            messages = []
            while not a.empty():
                messages.append(a.get())
            for message in messages:
                if message[0] =="ip":
                    variables.PEER_NODES.append(str(messages[1]))
                    continue
                a.put(message)
            start = time.time()
            consensus = consensus()

            if consensus:
                return False, consensus
        effort, pow_hash_object = Utility.genhash(last_block.index + 1, now, data, last_block.hash)
        leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
    return True, Block(last_block.index + 1, now, pow_hash_object.hexdigest(), effort, data, last_block.hash)


def mine(a):
    # See if other blockchains exist
    blockchain = consensus()
    if not blockchain:
        print("need to make one")
        # We didn't find one, need to make one
        variables.BLOCKCHAIN.append(create_genesis_block())
    else:
        # See if we got any blocks from someone, save it
        variables.BLOCKCHAIN = blockchain
    a.put(Utility.buildmessage("blockchain", variables.BLOCKCHAIN))
    requests.post(
        "http://" + variables.MINER_NODE_URL + ":" + str(variables.PORT) + "/blocks?update=" + User.public_key)
    while True:
        last_block = variables.BLOCKCHAIN[len(variables.BLOCKCHAIN) - 1]
        #   -get transactions
        transactions = requests.get(
            "http://" + variables.MINER_NODE_URL + ":" + str(variables.PORT) + "/txion?update=" + User.public_key).content
        variables.PENDING_TRANSACTIONS = json.loads(transactions)
        variables.PENDING_TRANSACTIONS.append({
            "from": "network",
            "to": User.public_key,
            "amount": 1.0})
        # mine using the updated blockchain
        pow, pow_output = proof_of_work(a, last_block, variables.PENDING_TRANSACTIONS)
        variables.PENDING_TRANSACTIONS = []
        if pow:
            variables.BLOCKCHAIN.append(pow_output)
        else:
            variables.BLOCKCHAIN = pow_output
        a.put(["mine", variables.BLOCKCHAIN])
        requests.post(
            "http://" + variables.MINER_NODE_URL + ":" + str(variables.PORT) + "/blocks?update=" + User.public_key)
