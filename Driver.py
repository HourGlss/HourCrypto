import logging
import time
FORMAT = "[{%(levelname)s} %(filename)s:%(lineno)s 	- %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='runlog.log', level=logging.DEBUG, format=FORMAT)

import Web.Endpoints as Web
from multiprocessing import Process, Event
import sys
def welcome_msg():

    print("""       =========================================\n
        HOUR COIN v1.0.0 - BLOCKCHAIN SYSTEM\n
       =========================================\n\n
       """)

if __name__ == '__main__':

    logging.debug("Display welcome")

    welcome_msg()
    e = Event()
    web_process = Process(target=Web.start,args=(e,))
    logging.debug("Starting the web")
    web_process.start()
    logging.debug("Web started")