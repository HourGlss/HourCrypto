from anytree import  RenderTree, search, LevelOrderIter, PostOrderIter
from Blockchain_classes.Block import Block
import inspect
import logging
import sqlite3




class Blockchain():
    __root = None
    __stored = []
    __last_added = None
    __added_to_db = 0



    def __init__(self, index=-1, timemade=-1, proof_of_work_input=-1, effort=-1, transactions=-1, previous_hash=-1):
        func = inspect.currentframe().f_back.f_code
        self.connection = sqlite3.connect('blockchain.db')
        self.cursor = self.connection.cursor()
        self.connection.commit()
        self.cursor.execute("SELECT hash FROM unverified_blocks WHERE `index`=0")
        response = self.cursor.fetchone()
        if  response == None or len(str(response[0]))!= 64:
            self.add(index, timemade, proof_of_work_input, effort, transactions, previous_hash)
        else:
            self.cursor.execute("SELECT * FROM unverified_blocks")
            all = self.cursor.fetchall()
            for db_block_info in all:
                b = Block()
                b.import_from_db(db_block_info)
                self.add(b.index,b.timemade,b.proof_of_work,b.effort,b.transactions,b.previous_hash,update_db=False)




    def add(self,index=-1, timemade=-1, proof_of_work_input=-1, effort=-1, transactions=-1, previous_hash=-1,update_db = True):
        print("adding",index)
        func = inspect.currentframe().f_back.f_code
        block = Block(index, timemade, proof_of_work_input, effort, transactions, previous_hash)
        execute_sql = False
        if self.__root is None:
            execute_sql = True
            self.__root = block
        else:
            print("root is NOT None")
            found = search.find(self.__root, lambda node: node.hash == previous_hash)
            if found != None:
                print("Found last block")
                block.parent=found
                execute_sql = True
                self.__analyze()
        self.__set_last_added(block)
        if execute_sql and update_db:
            print("Block added {} into unverified ".format(block.hash))
            dict_to_use = block.getdict()
            self.cursor.execute(
                "INSERT INTO unverified_blocks VALUES (:index,:timemade,:proof_of_work,:effort,:transactions,:hash,:previous_hash)",
                dict_to_use)
            self.connection.commit()
            self.__added_to_db += 1
        self.__to_store()

    def __str__(self):
        func = inspect.currentframe().f_back.f_code
        to_return = "stored\n"
        i = 0
        for block in self.__stored:
            to_return += str(i)+" "+str(block) + "\n"
            i+=1
        to_return += "\ntree\n"
        for pre, fill, block in RenderTree(self.__root):
            to_return += "{}{} {}\n".format(pre, i,block)
            i+=1
        return to_return

    def __set_last_added(self,block):
        self.__last_added = block
        print("set",block.index,"as last block")

    def last_added(self):
        func = inspect.currentframe().f_back.f_code
        return self.__last_added

    def num_added(self):
        return self.__added_to_db

    def __remove_branches(self, node, leafs):
        func = inspect.currentframe().f_back.f_code
        branch_length = {}
        for leaf in leafs:
            done = False
            current = leaf
            steps = 0
            while not done:
                if current.parent.hash == node.hash:
                    done = True
                else:
                    steps += 1
                    current = current.parent
            branch_length[leaf] = steps
        max = 0
        for key, values in branch_length.items():
            if values > max:
                max = values
        for leaf, steps in branch_length.items():
            if max - steps < 4:
                continue
            current = leaf
            done = False
            while not done:
                if current.parent.hash == node.hash:
                    current.parent = None
                    done = True
                else:
                    temp = current
                    current = current.parent
                    temp.parent = None

    def __to_store(self):
        if len(self.__stored) > 0:
            for block in self.__stored:
                logging.debug("Deleting {} from unverified".format(block.hash))
                self.cursor.execute('DELETE FROM unverified_blocks WHERE hash=:hash',{'hash':block.hash})
                self.connection.commit()
                logging.debug("Adding {} to verified".format(block.hash))
                self.cursor.execute(
                    "INSERT INTO verified_blocks VALUES (:index,:timemade,:proof_of_work,:effort,:transactions,:hash,:previous_hash)",
                    block.getdict())
                self.connection.commit()
            self.__stored = []

    def __analyze(self):
        func = inspect.currentframe().f_back.f_code
        # Remove branches
        for node in PostOrderIter(self.__root):
            children = node.children
            if len(children) > 1:
                leafs = []
                for find_leaf in PostOrderIter(self.__root):
                    if find_leaf.is_leaf and find_leaf.hash in [n.hash for n in node.descendants]:
                        leafs.append(find_leaf)

                self.__remove_branches(node, leafs)
        # Store Verified
        starting = 0
        end = None
        for node in LevelOrderIter(self.__root):
            if len(node.children) > 1:
                break
            end = node
            starting += 1
        if starting > 7:
            to_store = []
            hinder = 3
            current = end
            done = False
            save_for_root = None
            while not done:

                if current.parent.hash == self.__root.hash:
                    current.parent = None
                    done = True
                else:
                    temp = current
                    current = current.parent

                    if hinder > 0:
                        if hinder == 1:
                            save_for_root = current
                        hinder -= 1
                    else:
                        to_store.append(current)
                        temp.parent = None

            to_store.append(self.__root)
            self.__root = save_for_root
            for i in range(len(to_store) - 1, -1, -1):
                logging.debug("Adding to store")
                self.__stored.append(to_store[i])

    def __show(self):
        func = inspect.currentframe().f_back.f_code
        for pre, fill, node in RenderTree(self.__root):
            print("{}{}".format(pre, node.hash))
