import requests
import Mining.Mining as Mining
import Mining.Variables as variables
import Web.Endpoints as Web
from multiprocessing import Process, Queue
def welcome_msg():
    print("""       =========================================\n
        HOUR COIN v1.0.0 - BLOCKCHAIN SYSTEM\n
       =========================================\n\n
       """)

if __name__ == '__main__':

    welcome_msg()

    a = Queue()
    p2 = Process(target=Web.start, args=(a,))
    p2.start()

    p1 = Process(target=Mining.mine, args = (a,))
    p1.start()