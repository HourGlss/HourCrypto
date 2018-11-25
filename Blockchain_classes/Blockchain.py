from anytree import  RenderTree, search, LevelOrderIter, PostOrderIter
from Blockchain_classes.Block import Block
import inspect
import logging
import sqlite3
import sys




class Blockchain():
    __root = None
    __stored = []
    __last_added = None
    __added_to_db = 0
    __delete_db = True

    def __check_delete(self):
        if self.__delete_db:
            self.cursor.execute("DELETE FROM verified_blocks")
            self.cursor.execute("DELETE FROM unverified_blocks")
            self.connection.commit()

    def __init__(self, block):
        func = inspect.currentframe().f_back.f_code
        self.connection = sqlite3.connect('blockchain.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.connection.commit()
        self.__check_delete()
        self.cursor.execute("SELECT hash FROM unverified_blocks WHERE `index`=0")
        unverified_response = self.cursor.fetchone()
        self.cursor.execute("SELECT hash FROM verified_blocks WHERE `index`=0")
        verified_response = self.cursor.fetchone()
        if  unverified_response is None and verified_response is None:
            self.add(block)
        else:
            self.cursor.execute("SELECT * FROM unverified_blocks")

            unverified_all = self.cursor.fetchall()
            for db_block_info in unverified_all:
                b = Block()
                b.import_from_database(db_block_info)
                self.add(b,update_db=False)
            self.cursor.execute("SELECT * FROM verified_blocks")
            verified_all = self.cursor.fetchall()
            if verified_all is not None:
                self.__added_to_db+=len(verified_all)
                self.__added_to_db += len(unverified_all)
                print("total of {}".format(self.__added_to_db))
            print("Done reloading")

    def get(self,number):
        self.cursor.execute("SELECT * FROM verified_blocks WHERE `index` = ?", (number,))
        verified_response = self.cursor.fetchone()
        if verified_response is not None:
            b = Block()
            b.import_from_database(verified_response)
            return b
        self.cursor.execute("SELECT * FROM unverified_blocks WHERE `index` = ?", (number,))
        unverified_response = self.cursor.fetchone()
        if unverified_response is not None:
            b = Block()
            b.import_from_database(unverified_response)
            return b

    def add(self,block,update_db = True):
        func = inspect.currentframe().f_back.f_code
        execute_sql = False
        if self.__root is None:
            execute_sql = True
            self.__root = block
        else:
            # print("trying to add {}".format(block))
            found = search.find(self.__root, lambda node: node.hash == block.previous_hash)
            if found != None:
                block.parent=found
                execute_sql = True
                self.__analyze()
            else:
                print("MAJOR PROBLEM couldn't find parent")

        self.__set_last_added(block)
        if execute_sql and update_db:
            dict_to_use = block.get_block_as_dictionary()
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
                logging.debug("Adding {} to verified".format(block.hash))
                self.cursor.execute(
                    "INSERT INTO verified_blocks VALUES (:index,:timemade,:proof_of_work,:effort,:transactions,:hash,:previous_hash)",
                    block.get_block_as_dictionary())
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
