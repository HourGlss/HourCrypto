from multiprocessing import Process, Queue
import random
import hashlib
import string
import secrets
import time
import os


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
