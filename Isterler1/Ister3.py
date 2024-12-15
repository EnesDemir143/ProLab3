import networkx as nx
import matplotlib.pyplot as plt

class BST:
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = self.Node(key)
            else:
                self._insert(node.left, key)
        else:
            if node.right is None:
                node.right = self.Node(key)
            else:
                self._insert(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def visualize(self, output_file=None):
        G = nx.DiGraph()
        pos = {}

        def add_edges(node, x=0, y=0, level=0):
            if node is not None:
                G.add_node(node.key)
                pos[node.key] = (x, -y)
                if node.left:
                    G.add_edge(node.key, node.left.key)
                    add_edges(node.left, x - 2**(-level-1), y + 1, level + 1)
                if node.right:
                    G.add_edge(node.key, node.right.key)
                    add_edges(node.right, x + 2**(-level-1), y + 1, level + 1)

        add_edges(self.root)
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=10, font_weight="bold")
        if output_file:
            plt.savefig(output_file)
        else:
            plt.show()