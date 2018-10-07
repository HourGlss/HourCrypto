from anytree import Node, RenderTree, search, LevelOrderIter, PostOrderIter


class Tree():
    root = None
    stored = []

    def __init__(self, genesis):
        self.root = genesis

    def add(self, name_to_add, param):

        found = search.find(self.root, lambda node: node.name == param)
        Node(name_to_add, parent=found)
        self.__analyze()

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
        for node in PostOrderIter(self.root):
            children = node.children
            if len(children) > 1:
                leafs = []
                for find_leaf in PostOrderIter(self.root):
                    if find_leaf.is_leaf and find_leaf.name in [n.name for n in node.descendants]:
                        leafs.append(find_leaf)

                self.__remove_branches(node, leafs)
        # Store Verified
        starting = 0
        end = None
        for node in LevelOrderIter(self.root):
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

                if current.parent.name == self.root.name:
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

            to_store.append(self.root)
            self.root = save_for_root
            for i in range(len(to_store) - 1, -1, -1):
                self.stored.append(to_store[i])

    def __show(self):
        for pre, fill, node in RenderTree(self.root):
            print("{}{}".format(pre, node.name))


if __name__ == "__main__":
    tr = Tree(Node("a"))
    tr.add('b', 'a')
    tr.add('c', 'b')
    tr.add('d', 'c')
    tr.add('e', 'd')
    tr.add('f', 'd')
    tr.add('g', 'e')
    tr.add('h', 'f')
    tr.add('i', 'h')
    tr.add('j', 'i')
    tr.add('k', 'j')
    tr.add('m', 'b')
    tr.add('n', 'm')
    tr.add("l", "k")
    tr.add('o', 'l')
    tr.add('p', 'o')
    tr.add('q', 'p')
    tr.add('r', 'q')
    tr.add('s', 'r')
    tr.add('t', 's')
    tr.add('u', 't')
    tr.add('v', 'u')
    tr.add('w', 'v')
    tr.add('x', 'w')
    tr.add('y', 'x')
    tr.add('z', 'y')
    print(tr.stored)
