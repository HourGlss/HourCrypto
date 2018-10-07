import hashlib
import ast
import inspect
import logging
from anytree import NodeMixin
# The class for Block
class BaseBlock(object):
    def __init__(self, index=-1, timestamp=-1, proof_of_work_input=-1, effort=-1, data=-1, previous_hash=-1):
        print("BaseBlock", index)
        func = inspect.currentframe().f_back.f_code
        logging.info("Created a block i:{}".format(index))
        logging.debug("Block i:{} time:{} pow:{} effort:{} data:{} prev_hash:{}".format(index, timestamp, proof_of_work_input, effort, data, previous_hash))
        """Returns a new Block object. Each block is "chained" to its previous
        by calling its unique hash.

        Args:
            index (int): Block number.
            timestamp (float): Block creation timestamp.
            pow (str): Proof of work sha256 hexdigest, should start with a certain number of zeroes
            effort (str): random string that is used to pad the index, timestamp, pow, and previous block hash so that
                there is enough leading zeroes in the sha256 digest
            data (list): Transactional Data to be sent.
            previous_hash(str): String representing previous block unique hash.


        Attrib:
            index (int): Block number.
            timestamp (int): Block creation timestamp.
            data (dict): Data to be sent.
            previous_hash(str): String representing previous block unique hash.
            hash(str): Current block unique hash.

        """

        self.index = index
        self.timestamp = timestamp

        self.proof_of_work = proof_of_work_input
        self.effort = effort
        self.data = data
        '''
        data contains:
         transactions: list
        '''
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        """Creates the unique hash for the block. It uses sha256."""
        m = hashlib.sha256()
        m.update((str(self.index) + str(self.timestamp) + str(self.proof_of_work) + str(self.effort) + str(
            self.data) + str(self.previous_hash)).encode('utf-8'))
        logging.debug("Block's hash: {}".format(m.hexdigest()))
        return m.hexdigest()

    def exportjson(self):
        json_to_export = {
            "index": str(self.index),
            "timestamp": str(self.timestamp),
            "pow": str(self.proof_of_work),
            "effort": str(self.effort),
            "data": str(self.data),
            "previous": str(self.previous_hash),
            "hash": str(self.hash)
        }
        logging.debug("Exporting to json:{}".format(json_to_export))
        return json_to_export

    def importjson(self, json_to_import):
        logging.debug("Importing from json:{}".format(json_to_import))
        self.index = int(json_to_import['index'])
        self.timestamp = str(json_to_import['timestamp'])
        self.proof_of_work = str(json_to_import['pow'])
        self.effort = str(json_to_import['effort'])
        self.data = ast.literal_eval(json_to_import['data'])
        self.previous_hash = str(json_to_import['previous'])
        self.hash = self.hash_block()

    def __repr__(self):
        # def __init__(self, index, timestamp, pow, effort,data, previous_hash):
        return "Block({},{},'{}','{}',{},'{}')".format(self.index, self.timestamp, self.proof_of_work, self.effort,
                                                       self.data, self.previous_hash)

    def __str__(self):
        return "i: {} time: {} \tpow: {} effort: {} data: {} \tprevious: {} hash: {}".format(self.index, self.timestamp,
                                                                                             self.proof_of_work,
                                                                                             self.effort, self.data,
                                                                                             self.previous_hash,
                                                                                             self.hash)

class Block(BaseBlock,NodeMixin):
    def __init__(self, index=-1, timestamp=-1, proof_of_work_input=-1, effort=-1, data=-1, previous_hash=-1,parent = None):
        print("Block",index)
        NodeMixin.__init__(self)
        BaseBlock.__init__(self,index,timestamp,proof_of_work_input,effort,data,previous_hash)
        self.name = self.hash
