import networkx as nx  # type: ignore
import matplotlib  # type: ignore
matplotlib.use('Agg')  # GUI yerine arka planda çalışır
import matplotlib.pyplot as plt  # type: ignore
from Objects.Author import Author
class AVLTree:
    class Node:
        def __init__(self, data):
            self.data = data  # Tuple: (index, Author object)
            self.cost = data[0]  # Index is used as cost for ordering
            self.left = None
            self.right = None
            self.height = 1

    def __init__(self):
        self.root = None

    def insert(self, data):
        """Insert a tuple of (index, Author object)"""
        if not isinstance(data, tuple):
            raise ValueError("Data must be a tuple of (index, Author)")
        self.root = self._insert(self.root, data)

    def _insert(self, node, data):
        if node is None:
            return self.Node(data)

        cost = data[0]  # Compare by index
        if cost < node.cost:
            node.left = self._insert(node.left, data)
        else:
            node.right = self._insert(node.right, data)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and cost < node.left.cost:
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and cost > node.right.cost:
            return self._left_rotate(node)

        # Left Right Case
        if balance > 1 and cost > node.left.cost:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left Case
        if balance < -1 and cost < node.right.cost:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def delete(self, author):
        """Delete by Author object"""
        node_to_delete = self._search_by_author(self.root, author)
        if node_to_delete is None:
            raise ValueError(f"Author not found in the tree")
        self.root = self._delete(self.root, node_to_delete.cost)

    def _delete(self, node, cost):
        if node is None:
            return node

        if cost < node.cost:
            node.left = self._delete(node.left, cost)
        elif cost > node.cost:
            node.right = self._delete(node.right, cost)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._min_value_node(node.right)
            node.data = temp.data
            node.cost = temp.cost
            node.right = self._delete(node.right, temp.cost)

        if node is None:
            return node

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)

        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)

        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _search_by_author(self, node, author):
        if node is None:
            return None
        if node.data[1] == author:
            return node
        left_result = self._search_by_author(node.left, author)
        if left_result is not None:
            return left_result
        return self._search_by_author(node.right, author)

    def visualize(self, output_file=None):
        G = nx.DiGraph()
        pos = {}

        def add_edges(node, x=0, y=0, level=0):
            if node is not None:
                author = node.data[1]
                node_label = f"{author.name}"  # Using author name for visualization

                G.add_node(node_label)
                pos[node_label] = (x, -y)
                if node.left:
                    left_label = f"{node.left.data[1].name}"
                    G.add_edge(node_label, left_label)
                    add_edges(node.left, x - 2 ** (-level - 1), y + 1, level + 1)
                if node.right:
                    right_label = f"{node.right.data[1].name}"
                    G.add_edge(node_label, right_label)
                    add_edges(node.right, x + 2 ** (-level - 1), y + 1, level + 1)

        add_edges(self.root)
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_color="lightblue",
                node_size=2000, font_size=8, font_weight="bold", arrows=False)
        if output_file:
            plt.savefig(output_file)
            plt.close()  # Close the figure to free memory
        else:
            plt.show()