import requests
import inspect
import Mining.Mining as Mining
import Mining.Variables as variables
import Web.Endpoints as Web
import logging
from multiprocessing import Process, Queue
def welcome_msg():

    print("""       =========================================\n
        HOUR COIN v1.0.0 - BLOCKCHAIN SYSTEM\n
       =========================================\n\n
       """)

if __name__ == '__main__':
    logging.debug("Display welcome")
    welcome_msg()
    logging.debug("Make a Q")
    a = Queue()
    p2 = Process(target=Web.start, args=(a,))
    logging.debug("Starting the web")
    p2.start()
    logging.debug("Web started")

    p1 = Process(target=Mining.mine, args = (a,))
    logging.debug("Starting to mine")
    p1.start()
    logging.debug("Mining Started")