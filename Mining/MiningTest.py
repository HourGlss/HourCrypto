import logging
FORMAT = "[{%(levelname)s} %(filename)s:%(lineno)s 	- %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='scratch.log', level=logging.INFO, format=FORMAT)
from Mining.Block import Block
import time
import User.User as User
import Utilities.Utility as Utility
WORK = 3
BLOCKCHAIN = []
BLOCKCHAIN.append(Utility.create_genesis_block())
while True:
    if len(BLOCKCHAIN) == 2500:
        break
    last_block = BLOCKCHAIN[len(BLOCKCHAIN)-1]
    now = time.time()
    data = [{
            "from": "network",
            "to": User.public_key,
            "amount": 1.0}]
    done = False
    block = None
    while not done:
        effort, pow_hash_object = Utility.genhash(last_block.index + 1, now, data, last_block.hash)
        leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
        if leading_zeroes >= WORK:
            done = True
    block = Block(last_block.index + 1, now, pow_hash_object.hexdigest(), effort, data, last_block.hash)
    BLOCKCHAIN.append(block)
Utility.validate_blockchain(BLOCKCHAIN)