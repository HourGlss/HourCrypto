from multiprocessing import Process, Queue
import random
import hashlib
import string
import secrets
import time
import os
'''
def proof_of_work(a, last_block, data):
    func = inspect.currentframe().f_back.f_code
    logging.info("Starting proof of work")
    start = time.time()
    interval = 20
    now = time.time() + 1
    effort, pow_hash_object = Utility.genhash(last_block.index + 1, time.time(), data, last_block.hash)
    leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
    while leading_zeroes <= variables.WORK:
        now = time.time() + 1
        if int(now - start) % interval + 1 == 0:
            logging.debug("Checking for messages")
            messages = []
            while not a.empty():
                obj = a.get()
                logging.debug("Got {} from queue".format(obj))
                messages.append(obj)
            for message in messages:
                if message[0] =="ip":
                    logging.debug("That's an ip {} adding to peers".format(message[1]))
                    variables.PEER_NODES.append(str(messages[1]))
                    continue
                logging.debug("not an IP, putting it back message:{}".format(message))
                a.put(message)
            start = time.time()
            consensus = consensus()

            if consensus:
                logging.info("Received a consensus while doing POW")
                return False, consensus
        effort, pow_hash_object = Utility.genhash(last_block.index + 1, now, data, last_block.hash)
        leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
    retBlock = Block(last_block.index + 1, now, pow_hash_object.hexdigest(), effort, data, last_block.hash)
    logging.info("returning: {}".format(retBlock))
    return True, retBlock

'''


def buildpow(index,timestamp,effort,data,previous_hash):
    m = hashlib.sha256()
    m.update((str(index) + str(timestamp) + str(effort) + str(data) + str(previous_hash)).encode('utf-8'))
    return m

def random_str():
    # Generate a random size string from 3 - 27 characters long
    rand_str = ''
    for i in range(0, 1 + secrets.randbelow(25)):
        rand_str += string.ascii_lowercase[secrets.randbelow(26)]  # each char is a random downcase letter [a-z]
    return rand_str

def leadingzeroes(digest):
    n = 0
    result = ''.join(format(x, '08b') for x in bytearray(digest))
    for c in result:
        if c == '0':
            n += 1
        else:
            break
    return n

def genhash(index,timestamp,data,last_hash):
    effort = random_str()
    return effort, buildpow(index,timestamp,effort,data,last_hash)


def foo(a,i):
    done = False
    pow_hash_object = None
    effort = None
    while a.empty():
        data = {"stuff":"done"}
        effort, pow_hash_object = genhash(1, time.time(), data, "0")
        leading_zeroes = leadingzeroes(pow_hash_object.digest())
        if leading_zeroes > 10:
            break
    if not a.empty():
        return False
    a.put((i,pow_hash_object.hexdigest()))
    return True

if __name__ == '__main__':
    a = Queue()
    processes = []
    for i in range(0,os.cpu_count()-2):
        processes.append(Process(target=foo, args=(a,i)))

    for i in range(len(processes)):
        processes[i].start()
    print(a.get())
