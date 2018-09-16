import requests
import json
import time
from Mining.Block import Block
import Mining.Variables as variables
import Utilities as Utility
import User.user as User
def consensus(a,peers):
    if len(peers) == 0:
        return False
    global BLOCKCHAIN
    # Get the blocks from other nodes
    other_chains = find_new_chains()
    # If our chain isn't longest, then we store the longest chain
    if len(other_chains) == 1:
        BLOCKCHAIN = other_chains[0]
        a.put(["consensus",BLOCKCHAIN])
        requests.get("http://" + variables.MINER_NODE_URL + ":" + str(variables.PORT) + "/blocks?update=" + User.public_key)
        ROOT = True
        return BLOCKCHAIN
    return BLOCKCHAIN

def find_new_chains(peers):
    # Get the blockchains of every other node
    other_chains = []
    for node_url in peers:

        blockchain_json = None
        found_blockchain = []
        url = "http://"+node_url + ":" + str(variables.PORT) + "/blocks"
        blockchain_json = requests.get(url)

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
    global WORK
    work_ez = int(WORK / 4) + 1
    pow = "0" * work_ez
    pad = "1337"
    for i in range(4, 64):
        pow += pad[i % len(pad)]
    b = Block(0, time.time(), pow, "e", {
        "transactions": None},
              "0")
    return b

def mine(a):
    print("mine()")
    while True:
        if not a.empty():
            test = a.get()

            print(test)