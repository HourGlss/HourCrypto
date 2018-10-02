import base64
import hashlib
import secrets
import string
import Mining.Variables as variables
import inspect
import time
from Mining.Block import Block
from ecdsa import ecdsa
import logging

def create_genesis_block():
    func = inspect.currentframe().f_back.f_code
    logging.info("Creating a genesis block")
    logging.debug("Work:{}".format(variables.WORK))
    work_ez = int(variables.WORK / 4) + 1
    proof_of_work = "0" * work_ez
    pad = "1337"
    for i in range(4, 64):
        proof_of_work += pad[i % len(pad)]
    b = Block(0, time.time(), proof_of_work, "e", [],
              "0")
    b.data = [{"FROM": 0, "TO": 0, "AMOUNT": 0}]
    logging.info("Returning block: {}".format(b))
    return b

def buildmessage(origin, data):
    func = inspect.currentframe().f_back.f_code
    logging.debug("type: {} data:{}".format(origin, data))
    return (origin, data)


def buildpow(index,timestamp,effort,data,previous_hash):
    m = hashlib.sha256()
    m.update((str(index) + str(timestamp) + str(effort) + str(data) + str(previous_hash)).encode('utf-8'))
    return m

def validate(block):
    func = inspect.currentframe().f_back.f_code

    logging.info("Validating block")
    if block.index == 0:
        logging.debug("Block validated good")
        return True
    generaged_proof_of_work = buildpow(block.index,block.timestamp,block.effort,block.data,block.previous_hash)
    if block.proof_of_work == generaged_proof_of_work.hexdigest():
        logging.debug("Block validated good")
        return True
    logging.warning("powhexdig:{} should have received: {}".format(generaged_proof_of_work.hexdigest(),block.proof_of_work))
    return False


def random_str():
    # Generate a random size string
    rand_str = ''
    for i in range(0, 1 + secrets.randbelow(25)):
        rand_str += string.ascii_lowercase[secrets.randbelow(26)]  # each char is a random downcase letter [a-z]
    return rand_str

def genhash(index,timestamp,data,last_hash):
    effort = random_str()
    return effort, buildpow(index,timestamp,effort,data,last_hash)

def leadingzeroes(digest):
    #TODO I'm almost positive there's a faster way to do this
    n = 0
    result = ''.join(format(x, '08b') for x in bytearray(digest))
    for c in result:
        if c == '0':
            n += 1
        else:
            break
    return n

def createHexdigest(s):
    m = hashlib.sha256()
    m.update(s.encode('utf-8'))
    secret_key = m.hexdigest()
    return secret_key

def validate_blockchain(blockchain):
    func = inspect.currentframe().f_back.f_code

    logging.info("Validating blockchain")
    previous = ""
    for i in range(0,len(blockchain)-1):
        block = blockchain[i]
        logging.debug("Evaluating block: {}".format(block))
        if block.index == 0:
            logging.debug("Genesis block found")
            previous = block.hash
            continue
        else:
            previous = blockchain[i-1].hash
        if not validate(block):
            logging.warning("Did not validate blockchain block did not validate")

            return False
        data = block.data
        for transaction in data:
            logging.debug("trans: {}".format(transaction))
            if transaction['from'] == "network" and transaction['amount'] != 1:
                logging.warning("Did not validate blockchain mining wrong")

                return False
        if previous != block.previous_hash:
            logging.debug("previous hash didn't validate previous:{} block.previous:{}".format(previous,block.previous_hash))
            logging.warning("Did not validate blockchain Previous hash incorrect")
            return False
    logging.info("Validated")
    return True

def validate_signature(public_key, signature, message):
    #TODO I have never tested this
    """Verifies if the signature is correct. This is used to prove
    it's you (and not someone else) trying to do a transaction with your
    address. Called when a user tries to submit a new transaction.
    """
    public_key = (base64.b64decode(public_key)).hex()
    signature = base64.b64decode(signature)
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
    # Try changing into an if/else statement as except is too broad.
    try:
        return vk.verify(signature, message.encode())
    except:
        return False