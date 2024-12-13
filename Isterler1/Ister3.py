import matplotlib.pyplot as plt
import networkx as nx

# Binary Search Tree düğüm sınıfı
class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# BST sınıfı
class BST:
    def __init__(self):
        self.root = None

    # Düğüm ekleme
    def insert(self, key):
        if self.root is None:
            self.root = TreeNode(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key)
            else:
                self._insert(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = TreeNode(key)
            else:
                self._insert(node.right, key)

    # Düğüm silme
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

            min_larger_node = self._min_value_node(node.right)
            node.key = min_larger_node.key
            node.right = self._delete(node.right, min_larger_node.key)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current


    # grafik gösterim kısmı
    def visualize(self):
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
        plt.show()


author_queue = [5, 3, 8, 2, 4, 7, 9]


bst = BST()
for author_id in author_queue:
    bst.insert(author_id)


print("Başlangıç ağacı:")
bst.visualize()


author_to_remove = int(input("Ağaçtan silmek istediğiniz yazar ID'sini girin: "))
bst.delete(author_to_remove)


print("Güncellenmiş ağaç:")
bst.visualize()