class Node:
    def __init__(self, name = None):
        self.right = None
        self.left = None
        self.children = [self.left, self.right]
        self.parent = None
        self.name = name
        self.threshold = None
        self.values  = set()
    def add_left(self, node_obj):
        print("Node {1} is added as left child to Node {0}".format(self.name, node_obj.name))
        node_obj.parent = self
        self.left  = node_obj
        self.children = [self.left, self.right]
    def add_right(self, node_obj):
        print("Node {1} is added as right child to Node {0}".format(self.name, node_obj.name))
        node_obj.parent = self
        self.right = node_obj
        self.children = [self.left, self.right]
    def compute_threshold(self):
        pass

    def compute(self):
        pass

class Tree:
    def __init__(self, root = None):
        if root == None:
            self.root = Node(name="Root")
        else:
            self.root = root
    def add_child(self, child, parent = None, side = None):
        if parent == None:
            parent = self.root
        if side == None:
            self.add_child(child, parent, side = 'left')
        elif side=='left':
            if parent.left != None:
                print("Warning left child is being overwritten!")
            parent.add_left(child)
        elif side=='right':
            if parent.right != None:
                print("Warning right child is being overwritten!")
            parent.add_right(child)



class DecisionTree(Tree):
    def __init__(self, x, max_depth=4):
        root = Node(name='root')
        super().__init__(root=root)
        self.max_depth = max_depth
        self.compute(x, root,0)
    def compute(self, x , parent, depth):
        if len(x) <= 2 or depth >= self.max_depth:
            return
        import numpy as np
        threshold = np.mean(x)
        print(threshold)
        parent.threshold = threshold
        threshold_index =  [1 if xi >= threshold else 0 for i,xi in enumerate(x)].index(1)
        x_left = x[:threshold_index]
        x_right = x[threshold_index:]
        depth += 1
        print(x_left)
        print(x_right)
        print("Count {0}".format(depth))
        left_child = Node(name="{0}_left".format(depth))
        right_child = Node(name="{0}_right".format(depth))
        self.add_child(left_child, parent = parent, side='left')
        self.add_child(right_child, parent = parent, side='right')
        self.compute(x_left, left_child,depth)
        self.compute(x_right, right_child,depth)

    def predict(self, x, node=None):
        if not node:
            node = self.root
            print("Root is Used")
        if node.threshold:
            if node.threshold >=x:
                if node.left:
                    print("left exists")
                    node = node.left
                    return(self.predict(x,node))
                else:
                    return(node.parent.threshold)
            elif node.threshold < x:
                if node.right:
                    print("right exists")
                    node = node.right
                    return(self.predict(x,node))
                else:
                    return(node.parent.threshold)
            else:
                print("Error")
        else:
            print("threshold do not exist")
            print(node.parent.threshold)
            if node.parent.threshold:
                print("parent threshold exists")
            else:
                print("Alas")
            return(node.parent.threshold)


x = [3, 33, 146, 227, 342, 351, 353, 444, 556, 571, 709, 759, 836, 860, 968, 1056, 1726, 1846, 1872, 1986, 2311, 2366, 2608, 2676, 3098, 3278, 3288, 4434, 5034, 5049, 5085, 5089, 5089, 5097, 5324, 5389, 5565, 5623, 6080, 6380, 6477, 6740, 7192, 7447, 7644, 7837, 7843, 7922, 8738, 10089, 10237, 10258, 10491, 10625, 10982, 11175, 11411, 11442, 11811, 12559, 12559, 12791, 13121, 13486, 14708, 15251, 15261, 15277, 15806, 16185, 16229, 16358, 17168, 17458, 17758, 18287, 18568, 18728, 19556, 20567, 21012, 21308, 23063, 24127, 25910, 26770, 27753, 28460, 28493, 29361, 30085, 32408, 35338, 36799, 37642, 37654, 37915, 39715, 40580, 42015, 42045, 42188, 42296, 42296, 45406, 46653, 47596, 48296, 49171, 49416, 50145, 52042, 52489, 52875, 53321, 53443, 54433, 55381, 56463, 56485, 56560, 57042, 62551, 62651, 62661, 63732, 64103, 64893, 71043, 74364, 75409,76057, 81542, 82702, 84566, 88682]

dt = DecisionTree(x, max_depth = 10)

import numpy as np
import matplotlib.pyplot as plt
y = np.arange(len(x))
plt.plot(x,y)

pred_y = np.asarray([dt.predict(i) for i in x])
plt.plot(pred_y,y)
