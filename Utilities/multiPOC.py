from multiprocessing import Process, Queue
import random
import hashlib
import string
import secrets
import time
import os
from Utilities import Utility


def foo(a,i):
    done = False
    pow_hash_object = None
    effort = None
    while a.empty():
        data = {"stuff":"done"}
        effort, pow_hash_object = Utility.genhash(1, time.time(), data, "0")
        leading_zeroes = Utility.leadingzeroes(pow_hash_object.digest())
        if leading_zeroes >= 20:
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
