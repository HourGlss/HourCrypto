import logging
logging.info("Loading Variables")
WORK = 18

PEER_NODES = []
MINER_NODE_URL = "127.0.0.1"
PORT = 5000
BLOCKCHAIN = []
PENDING_TRANSACTIONS = []
logging.debug("work: {} peers:{} node_url:{} port: {} blockchain: {} pending: {}".format(WORK,PEER_NODES,MINER_NODE_URL,PORT,BLOCKCHAIN,PENDING_TRANSACTIONS))
logging.info("Done loading Variables")