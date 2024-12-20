import networkx as nx
import matplotlib.pyplot as plt


class BST:
    class Node:
        def __init__(self, data):
            self.data = data  # Tuple: (cost, object)
            self.cost = data[0]  # Cost is the first element of tuple
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def insert(self, data):
        if not isinstance(data, tuple):
            raise ValueError("Data must be a tuple")

        if self.root is None:
            self.root = self.Node(data)
        else:
            self._insert(self.root, data)

    def _insert(self, node, data):
        cost = data[0]  # Compare by cost
        if cost < node.cost:
            if node.left is None:
                node.left = self.Node(data)
            else:
                self._insert(node.left, data)
        else:
            if node.right is None:
                node.right = self.Node(data)
            else:
                self._insert(node.right, data)

    def delete(self, data):
        if isinstance(data, tuple):
            cost = data[0]  # Eğer data tuple ise cost'u al
        else:
            # Eğer direkt nesne gönderiliyorsa, ağacı dolaşıp ilgili düğümü bulmamız gerekiyor
            node_to_delete = self._search_by_object(self.root, data)
            if node_to_delete is None:
                raise ValueError(f"Object '{data}' not found in the tree.")
            cost = node_to_delete.cost  # Nesnenin maliyetini al
        self.root = self._delete(self.root, cost)

    def _search_by_object(self, node, obj):
        # Ağacı dolaşıp nesneyi arayan yardımcı bir fonksiyon
        if node is None:
            return None

        if node.data[1] == obj:  # Tuple'daki ikinci eleman nesneyi temsil ediyor
            return node

        # Hem sol hem sağ alt ağaçlarda arama yap
        left_result = self._search_by_object(node.left, obj)
        if left_result is not None:
            return left_result

        return self._search_by_object(node.right, obj)

    def _delete(self, node, cost):
        if node is None:
            return node

        if cost < node.cost:
            node.left = self._delete(node.left, cost)
        elif cost > node.cost:
            node.right = self._delete(node.right, cost)
        else:
            # Node to be deleted found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Replace with the smallest value in the right subtree
            temp = self._min_value_node(node.right)
            node.data = temp.data
            node.cost = temp.cost
            node.right = self._delete(node.right, temp.cost)
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
                # Düğümde yazılacak olan `orcid` bilgisi
                orcid = getattr(node.data[1], 'orcid', 'Unknown')  # Eğer orcid yoksa 'Unknown' yazsın
                node_label = f"ORCID: {orcid}"

                G.add_node(node_label)
                pos[node_label] = (x, -y)
                if node.left:
                    left_orcid = getattr(node.left.data[1], 'orcid', 'Unknown')
                    left_label = f"ORCID: {left_orcid}"
                    G.add_edge(node_label, left_label)
                    add_edges(node.left, x - 2 ** (-level - 1), y + 1, level + 1)
                if node.right:
                    right_orcid = getattr(node.right.data[1], 'orcid', 'Unknown')
                    right_label = f"ORCID: {right_orcid}"
                    G.add_edge(node_label, right_label)
                    add_edges(node.right, x + 2 ** (-level - 1), y + 1, level + 1)

        add_edges(self.root)
        nx.draw(G, pos, with_labels=True, node_color="lightblue",
                node_size=2000, font_size=8, font_weight="bold")
        if output_file:
            plt.savefig(output_file)
        else:
            plt.show()
    def search(self, cost):
        return self._search(self.root, cost)

    def _search(self, node, cost):
        if node is None or node.cost == cost:
            return node

        if cost < node.cost:
            return self._search(node.left, cost)
        return self._search(node.right, cost)