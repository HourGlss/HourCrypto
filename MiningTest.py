import logging
FORMAT = "[{%(levelname)s} %(filename)s:%(lineno)s 	- %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='scratch.log', level=logging.DEBUG, format=FORMAT)
from Blockchain_classes.Block import Block
from Blockchain_classes.Blockchain import Blockchain
import time
import User.User as User
import Utilities.Utility as Utility

WORK = 3
genesis = Utility.create_genesis_block()
print("MiningTest", genesis.index)
blockchain = Blockchain(genesis.index,genesis.timestamp,genesis.proof_of_work,genesis.effort,genesis.data,genesis.previous_hash)
# while True:
#     if len(blockchain.stored) == 2500:
#         break
#     last_block = blockchain.last_added()
#     now = time.time()
#     data = [{
#             "from": "network",
#             "to": User.public_key,
#             "amount": 1.0}]
#     done = False
#     block = None
#     while not done:
#         effort, pow_hash_object = Utility.genhash(last_block.index + 1, now, data, last_block.hash)
#         leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
#         if leading_zeroes >= WORK:
#             done = True
#     blockchain.add(last_block.index + 1, now, pow_hash_object.hexdigest(), effort, data, last_block.hash)
print(str(blockchain))


