import base64
import hashlib
import secrets
import string
import Mining_classes.Variables as Variables
import inspect
import time
from Blockchain_classes.Block import Block
from ecdsa import ecdsa
import logging

def create_genesis_block():
    func = inspect.currentframe().f_back.f_code
    # logging.info("Creating a genesis block")
    # logging.debug("Work:{}".format(variables.WORK))
    work_ez = int(Variables.WORK / 4) + 1
    proof_of_work = "0" * work_ez
    pad = "1337"
    for i in range(4, 64):
        proof_of_work += pad[i % len(pad)]
    while len(proof_of_work) <64:
        proof_of_work += "1"
    b = Block(0, time.time(), proof_of_work, "e", [{"from": '0', "to": '0', "amount": '0'}],"0")
    # logging.info("Returning block: {}".format(b))
    return b

def buildpow(index,timestamp,proof_of_work,effort,data,previous_hash):
    m = hashlib.sha256()
    m.update((str(index) + str(timestamp) +str(proof_of_work)+ str(effort) + str(data) + str(previous_hash)).encode('utf-8'))
    return m

def validate(block):

    func = inspect.currentframe().f_back.f_code

    logging.info("Validating block")
    if block.index == 0:
        logging.debug("Block validated good")
        return True
    generated_hash = buildpow(block.index,block.timemade,block.proof_of_work,block.effort,block.transactions,block.previous_hash)

    if block.hash == generated_hash.hexdigest():
        logging.debug("Block validated good")
        return True
    logging.warning("powhexdig:{} should have received: {}".format(generated_hash.hexdigest(),block.hash))
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