import logging
FORMAT = "[{%(levelname)s} %(filename)s:%(lineno)s 	- %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='scratch.log', level=logging.DEBUG, format=FORMAT)
from Blockchain_classes.Block import Block
from Blockchain_classes.Blockchain import Blockchain
import time
import sqlite3
import User_classes.User as User
import Utilities.Utility as Utility
conn = sqlite3.connect('blockchain.db')
c = conn.cursor()
WORK = 8
genesis = Utility.create_genesis_block()
blockchain = Blockchain(genesis.index,genesis.timemade,genesis.proof_of_work,genesis.effort,genesis.transactions,genesis.previous_hash)
added = 0



def save(block):
    c.execute("INSERT INTO blocks VALUES (:index,:timemade,:proof_of_work,:effort,:transactions,:previous_hash,:hash)",block.getdict())

    conn.commit()


c.execute("DELETE FROM blocks")
conn.commit()
while added < 1000:
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
        leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
        if leading_zeroes >= WORK:
            done = True
    added +=1
    blockchain.add(last_block.index + 1, now, pow_hash_object.hexdigest(), effort, data, last_block.hash)
    need_to_save,to_store = blockchain.to_store()
    if need_to_save:
        for block in to_store:
            save(block)
print(str(blockchain))

