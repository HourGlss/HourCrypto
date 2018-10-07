from anytree import Node, RenderTree, search, LevelOrderIter, PostOrderIter
from Blockchain_classes.Block import Block


class Blockchain():
    __root = None
    stored = []
    __last_added = None

    def __init__(self, index=-1, timestamp=-1, proof_of_work_input=-1, effort=-1, data=-1, previous_hash=-1):
        self.__root = Block(index, timestamp, proof_of_work_input, effort, data, previous_hash)
        self.__last_added = self.__root

    def add(self, index=-1, timestamp=-1, proof_of_work_input=-1, effort=-1, data=-1, previous_hash=-1):

        found = search.find(self.__root, lambda node: node.hash == previous_hash)
        added = Block(index, timestamp, proof_of_work_input, effort, data, previous_hash, parent=found)
        self.__last_added = added
        self.__analyze()

    def __str__(self):
        to_return = ""
        for block in self.stored:
            to_return += str(block) + "\n"
        to_return += "\n"
        for pre, fill, block in RenderTree(self.__root):
            to_return += "{}{}".format(pre, block.hash)
        return to_return

    def last_added(self):
        return self.last_added

    def __remove_branches(self, node, leafs):
        branch_length = {}
        for leaf in leafs:
            done = False
            current = leaf
            steps = 0
            while not done:
                if current.parent.name == node.name:
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
                if current.parent.name == node.name:
                    current.parent = None
                    done = True
                else:
                    temp = current
                    current = current.parent
                    temp.parent = None

    def __analyze(self):

        # Remove branches
        for node in PostOrderIter(self.__root):
            children = node.children
            if len(children) > 1:
                leafs = []
                for find_leaf in PostOrderIter(self.__root):
                    if find_leaf.is_leaf and find_leaf.name in [n.name for n in node.descendants]:
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

                if current.parent.name == self.__root.name:
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
        for pre, fill, node in RenderTree(self.__root):
            print("{}{}".format(pre, node.name))
