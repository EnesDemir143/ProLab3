import networkx as nx  # type: ignore
import matplotlib  # type: ignore
matplotlib.use('Agg')  # GUI yerine arka planda çalışır
import matplotlib.pyplot as plt  # type: ignore

class AVLTree:
    class Node:
        def __init__(self, data):
            self.data = data  # Tuple: (id, object)
            self.id = data[0]  # ID is the first element of tuple
            self.left = None
            self.right = None
            self.height = 1  # Height of node for balancing

    def __init__(self):
        self.root = None

    def insert(self, data):
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, tuple):
                    raise ValueError("Each item in the list must be a tuple")
                self.root = self._insert(self.root, item)
        elif isinstance(data, tuple):
            self.root = self._insert(self.root, data)
        else:
            raise ValueError("Data must be a tuple or a list of tuples")

    def _insert(self, node, data):
        if node is None:
            return self.Node(data)

        id = data[0]  # Compare by ID
        if id < node.id:
            node.left = self._insert(node.left, data)
        else:
            node.right = self._insert(node.right, data)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and id < node.left.id:
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and id > node.right.id:
            return self._left_rotate(node)

        # Left Right Case
        if balance > 1 and id > node.left.id:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left Case
        if balance < -1 and id < node.right.id:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def delete(self, data):
        if isinstance(data, tuple):
            id = data[0]  # Eğer data tuple ise id'yi al
        else:
            node_to_delete = self._search_by_object(self.root, data)
            if node_to_delete is None:
                raise ValueError(f"Object '{data}' not found in the tree.")
            id = node_to_delete.id  # Nesnenin id'sini al
        self.root = self._delete(self.root, id)

    def _delete(self, node, id):
        if node is None:
            return node

        if id < node.id:
            node.left = self._delete(node.left, id)
        elif id > node.id:
            node.right = self._delete(node.right, id)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._min_value_node(node.right)
            node.data = temp.data
            node.id = temp.id
            node.right = self._delete(node.right, temp.id)

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

    def _search_by_object(self, node, obj):
        if node is None:
            return None
        if node.data[1] == obj:
            return node
        left_result = self._search_by_object(node.left, obj)
        if left_result is not None:
            return left_result
        return self._search_by_object(node.right, obj)
    def visualize(self, orcidauthor, output_file=None):
        G = nx.DiGraph()
        pos = {}
        
        def add_edges(node, x=0, y=0, level=0):
            if node is not None:
                # Get ORCID and name for current node
                current_orcid = getattr(node.data[1], 'orcid', 'Unknown')
                current_name = getattr(node.data[1], 'name', 'Unknown')
                
                # Use ORCID as node identifier but display name as label
                G.add_node(current_orcid, label=current_name)
                pos[current_orcid] = (x, -y)
                
                if node.left:
                    left_orcid = getattr(node.left.data[1], 'orcid', 'Unknown')
                    G.add_edge(current_orcid, left_orcid)
                    add_edges(node.left, x - 2 ** (-level - 1), y + 1, level + 1)
                    
                if node.right:
                    right_orcid = getattr(node.right.data[1], 'orcid', 'Unknown')
                    G.add_edge(current_orcid, right_orcid)
                    add_edges(node.right, x + 2 ** (-level - 1), y + 1, level + 1)

        add_edges(self.root)
        
        plt.figure(figsize=(12, 8))
        
        # Get the name labels from node attributes
        labels = nx.get_node_attributes(G, 'label')
        
        # Draw the graph with names as labels
        nx.draw(G, pos, 
                labels=labels,  # Use names as labels
                with_labels=True, 
                node_color="lightblue",
                node_size=2000, 
                font_size=8, 
                font_weight="bold", 
                arrows=False)
        
        if output_file:
            plt.savefig(output_file)
        else:
            plt.show()