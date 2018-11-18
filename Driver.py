import logging
import time
FORMAT = "[{%(levelname)s} %(filename)s:%(lineno)s 	- %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='runlog.log', level=logging.DEBUG, format=FORMAT)
import Mining_classes.Mining as Mining
import Web.Endpoints as Web
from multiprocessing import Process, Queue
def welcome_msg():

    print("""       =========================================\n
        HOUR COIN v1.0.0 - BLOCKCHAIN SYSTEM\n
       =========================================\n\n
       """)

if __name__ == '__main__':

    logging.debug("Display welcome")
    welcome_msg()
    p2 = Process(target=Web.start)
    logging.debug("Starting the web")
    p2.start()
    logging.debug("Web started")

    time.sleep(10)
    p1 = Process(target=Mining.mine)
    p1.start()
    logging.debug("Mining_classes Started")