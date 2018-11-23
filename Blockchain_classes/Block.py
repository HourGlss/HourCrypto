import hashlib
import xmltodict
import logging
import inspect
import pickle
from anytree import NodeMixin


# The class for Block
class BaseBlock(object):

    def __init__(self):
        logging.info("Created a block:{}".format(str(self)))

    def hash_block(self):
        func = inspect.currentframe().f_back.f_code
        """Creates the unique hash for the block. It uses sha256."""
        m = hashlib.sha256()
        m.update((str(self.index) + str(self.timemade) + str(self.proof_of_work) + str(self.effort) + str(
            self.transactions) + str(self.previous_hash)).encode('utf-8'))
        return_hash = m.hexdigest()
        return return_hash

    def import_from_xml(self, block_xml):
        for field in block_xml:
            if field != "transactions":
                self.set_field(field, block_xml[field])
            else:
                transaction_to_add = {}

                if not isinstance(block_xml[field]['trans'],type([])):
                    for transaction in block_xml[field]['trans']:
                        transaction_to_add[transaction] = block_xml[field]['trans'][transaction]
                    self.set_field("transaction", transaction_to_add)
                else:
                    for odict in block_xml[field]['trans']:
                        transaction_to_add = {}
                        for k in odict:
                            transaction_to_add[k] = odict[k]
                        self.set_field("transaction", transaction_to_add)
        self.hash = self.hash_block()

    def set_field(self, field, value):
        # index=-1, time=-1, proof_of_work_input=-1, effort=-1, data=-1, previous_hash=-1
        if field == 'index':
            try:
                self.index = int(value)
            except:
                pass
        elif field == 'timemade':
            try:
                self.timemade = float(value)
            except:
                pass
        elif field == 'proof_of_work':
            try:
                self.proof_of_work = str(value)
            except:
                pass
        elif field == 'effort':
            try:
                self.effort = str(value)
            except:
                pass
        elif field == 'previous_hash':
            try:
                self.previous_hash = str(value)
            except:
                pass
        elif field == 'transaction':
            try:
                if type(value) is type({}):
                    self.transactions.append(value)
            except:
                pass

    def export_to_xml(self):
        # index=-1, time=-1, proof_of_work_input=-1, effort=-1, transactions=-1, previous_hash=-1
        returnblock = {'block': {'index': int(self.index), 'timemade': float(self.timemade),
                                 'proof_of_work': str(self.proof_of_work),
                                 'effort': str(self.effort), 'transactions': {'trans': self.transactions},
                                 'previous_hash': str(self.previous_hash)}}
        return xmltodict.unparse(returnblock)

    def get_block_as_dictionary(self):
        gen_dict = {'index': self.index, 'timemade': self.timemade, 'proof_of_work': self.proof_of_work,
                    'effort': self.effort, 'transactions': pickle.dumps(self.transactions),
                    'previous_hash': self.previous_hash, 'hash': self.hash}
        return gen_dict

    def import_from_database(self, listinfo):
        self.index = int(listinfo[0])
        self.timemade = str(listinfo[1])
        self.proof_of_work = str(listinfo[2])
        self.effort = str(listinfo[3])
        self.transactions = pickle.loads(listinfo[4])
        self.previous_hash = str(listinfo[6])
        self.hash = self.hash_block()


    def __repr__(self):
        # def __init__(self, index, timemade, pow, effort,data, previous_hash):
        return "i:{},time:{},proof:{},effort:{},hash:{},previous:{})".format(self.index, self.timemade, self.proof_of_work, self.effort,
                                                             self.hash,self.previous_hash)

    def __str__(self):
        return repr(self)
        # return "hash: {} previous: {}".format(self.hash, self.previous_hash)

    '''
    def __str__(self):
        return "i: {} time: {} \tpow: {} effort: {} data: {} \tprevious: {} hash: {}".format(self.index, self.timemade,
                                                                                             self.proof_of_work,
                                                                                             self.effort, self.data,
                                                                                             self.previous_hash,
                                                                                             self.hash)
    '''


class Block(BaseBlock, NodeMixin):
    def __init__(self, index=-1, timemade=-1, proof_of_work_input=-1, effort=-1, transactions=None, previous_hash=-1,
                 parent=None):
        super(BaseBlock, self).__init__()
        self.parent = parent
        self.index = int(index)
        timemade = round(float(timemade),3)

        self.timemade = str(timemade)

        self.proof_of_work = str(proof_of_work_input)
        self.effort = str(effort)
        if transactions is None:
            self.transactions = []
        else:
            self.transactions = transactions

        '''
        data contains:
         transactions: list
        '''
        self.previous_hash = str(previous_hash)
        self.hash = self.hash_block()
        # NodeMixin.__init__(self)
        #
        # BaseBlock.__init__(self, index, timemade, proof_of_work_input, effort, data, previous_hash)
        # self.name = self.hash
        # if parent != None:
        #     self.parent(parent)

    def getBlock(self):
        return super
