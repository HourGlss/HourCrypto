import logging
FORMAT = "[{%(levelname)s} %(filename)s:%(lineno)s 	- %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='scratch.log', level=logging.DEBUG, format=FORMAT)
from Blockchain_classes.Blockchain import Blockchain
import time
from Blockchain_classes.Block import Block
import User_classes.User as User
import Utilities.Utility as Utility

WORK = 5
genesis = Utility.create_genesis_block()

added = 0

blockchain = Blockchain(genesis)
while added < 100:
    last_block = blockchain.last_added()

    now = time.time()
    data = [{
            "from": "network",
            "to": User.public_key,
            "amount": 1.0}]
    done = False
    block = None
    while not done:
        effort, pow_hash_object = Utility.genhash(last_block.index + 1, now, data, last_block.hash)
        #this is a test ....
        leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
        if leading_zeroes >= WORK:
            done = True
    added +=1
    b = Block(last_block.index + 1, now, pow_hash_object.hexdigest(), effort, data, last_block.hash)
    blockchain.add(b)
    print("farmed",b)

print(str(blockchain))

