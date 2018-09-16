import time
import hashlib
import sys
import json

import os
import secrets
import string
import base64


import ecdsa
import secrets
import string
import logging

# Node's blockchain copy

""" Stores the transactions that this node has in a list.
If the node you sent the transaction adds a block
it will get accepted, but there is a chance it gets
discarded and your transaction goes back as if it was never
processed"""
NODE_PENDING_TRANSACTIONS = []
BLOCKCHAIN = []
ROOT = False
if len(PEER_NODES) == 0:
    ROOT = True
    BLOCKCHAIN.append(create_genesis_block())

def proof_of_work(a,last_block, data):
    start_time = time.time()
    global ROOT
    if ROOT:
        new_block_index = last_block.index + 1
        new_block_timestamp = time.time()

    NODE_PENDING_TRANSACTIONS = []



    lead = 0
    if ROOT:
        effort, pow_hash = genhash()

        global WORK
        lead = leadingzeroes(pow_hash.digest())
    while lead < WORK:
        if len(BLOCKCHAIN) == 0:
            ROOT = False
        # Check if any node found the solution every 60 seconds
        if not ROOT or int((time.time() - start_time) % 60) == 0:
            ROOT = True
            # If any other node got the proof, stop searching
            new_blockchain = consensus(a)
            if new_blockchain:
                return False, new_blockchain
        # generate new hash for next time
        effort, pow_hash = genhash()
        lead = leadingzeroes(pow_hash.digest())
        if not a.empty():
            qget = a.get()

            qfrom = qget[0]
            new_block = qget[1]
            print("received a block",qfrom)
            if validate(new_block) and new_block.previous_hash == BLOCKCHAIN[len(BLOCKCHAIN) - 1].previous_hash:
                BLOCKCHAIN.append(new_block)
                return False, BLOCKCHAIN

    # Once that hash is found, we can return it as a proof of our work
    mined_block = Block(new_block_index, new_block_timestamp, pow_hash.hexdigest(),effort, data, last_block.hash)
    return True, mined_block


def mine(a, blockchain, node_pending_transactions):
    global BLOCKCHAIN
    global WORK
    NODE_PENDING_TRANSACTIONS = node_pending_transactions
    while True:
        """Mining is the only way that new coins can be created.
        In order to prevent too many coins to be created, the process
        is slowed down by a proof of work algorithm.
        """
        # Get the last proof of work
        last_block = None
        new_block_data = None
        if ROOT:
            last_block = BLOCKCHAIN[len(BLOCKCHAIN) - 1]

            NODE_PENDING_TRANSACTIONS = requests.get(
                "http://" + MINER_NODE_URL + ":" + str(PORT) + "/txion?update=" + user.public_key).content
            NODE_PENDING_TRANSACTIONS = json.loads(NODE_PENDING_TRANSACTIONS)

            # Then we add the mining reward
            NODE_PENDING_TRANSACTIONS.append({
                "from": "network",
                "to": user.public_key,
                "amount": 1.0})

            new_block_data = {"transactions": list(NODE_PENDING_TRANSACTIONS)}
        proof = proof_of_work(a,last_block, new_block_data)
        if not proof[0]:
            BLOCKCHAIN = proof[1]
            continue
        else:
            mined_block = proof[1]

            '''
            String
            '''
            print("#",mined_block)
            '''
            String
            '''
            '''
            REPR
            '''
            # print("b{} = ".format(mined_block.index), repr(mined_block))
            # if last_block.index == 1:
            #     print('work = {}'.format(work))
            #     print("blockchain = [", end="")
            #     for i in range(0, len(BLOCKCHAIN)+1):
            #         print("b{}".format(i), end=",")
            #     print("]")
            #     sys.exit()

            '''
            END REPR
            '''

            BLOCKCHAIN.append(mined_block)
            a.put(["mined_lower",BLOCKCHAIN])
            requests.get("http://" + MINER_NODE_URL + ":" + str(PORT) + "/blocks?update=" + user.public_key)

            for node in PEER_NODES:
                url = "http://" + node + ":" + str(PORT) + "/block"
                headers = {"Content-Type": "application/json"}
                data = mined_block.exportjson();
                requests.post(url,json = data, headers = headers)















