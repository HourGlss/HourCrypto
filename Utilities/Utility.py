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

def buildpow(index,timestamp,effort,data,previous_hash):
    m = hashlib.sha256()
    m.update((str(index) + str(timestamp) + str(effort) + str(data) + str(previous_hash)).encode('utf-8'))
    return m

def validate(block):
    #TODO THIS IS A HUGE TODO
    return True


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