from anytree import  RenderTree, search, LevelOrderIter, PostOrderIter
from Blockchain_classes.Block import Block
import inspect
import logging

class Blockchain():
    __root = None
    stored = []
    __last_added = None

    def __init__(self, index=-1, timestamp=-1, proof_of_work_input=-1, effort=-1, data=-1, previous_hash=-1):
        func = inspect.currentframe().f_back.f_code
        block = Block(index, timestamp, proof_of_work_input, effort, data, previous_hash)
        logging.debug("Block added {}".format(str(block)))
        self.__root = block
        self.__last_added = self.__root

    def add(self, index=-1, timestamp=-1, proof_of_work_input=-1, effort=-1, data=-1, previous_hash=-1):
        func = inspect.currentframe().f_back.f_code
        logging.debug("Looking for {}".format(previous_hash))
        found = search.find(self.__root, lambda node: node.hash == previous_hash)
        if found != None:
            block = Block(index, timestamp, proof_of_work_input, effort, data, previous_hash, parent=found)
            logging.debug("Adding {} with parent {}".format(block.hash,found.hash))
            added = block

            self.__last_added = added
            self.__analyze()
        else:
            print("Couldn't find the block")

    def __str__(self):
        func = inspect.currentframe().f_back.f_code
        to_return = "stored\n"
        i = 0
        for block in self.stored:
            to_return += str(i)+" "+str(block) + "\n"
            i+=1
        to_return += "\ntree\n"
        for pre, fill, block in RenderTree(self.__root):
            to_return += "{}{} {}\n".format(pre, i,block)
            i+=1
        return to_return

    def last_added(self):
        func = inspect.currentframe().f_back.f_code
        return self.__last_added

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
                self.stored.append(to_store[i])

    def __show(self):
        func = inspect.currentframe().f_back.f_code
        for pre, fill, node in RenderTree(self.__root):
            print("{}{}".format(pre, node.hash))
