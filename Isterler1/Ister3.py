
class Node:
    def __init__(self, author, collaborators=None):
        self.author = author
        self.collaborators = collaborators if collaborators else {}
        self.left = None
        self.right = None

class Ister3:
    def __init__(self):
        self.root = None

    def insert(self, author, collaborators):
        """Insert an author into the BST, using ORCID as the key"""
        if not self.root:
            self.root = Node(author, collaborators)
        else:
            self._insert_recursive(self.root, author, collaborators)

    def _insert_recursive(self, node, author, collaborators):
        if author.orcid < node.author.orcid:
            if node.left is None:
                node.left = Node(author, collaborators)
            else:
                self._insert_recursive(node.left, author, collaborators)
        elif author.orcid > node.author.orcid:
            if node.right is None:
                node.right = Node(author, collaborators)
            else:
                self._insert_recursive(node.right, author, collaborators)

    def find_author(self, orcid):
        """Find author by ORCID"""
        return self._find_recursive(self.root, orcid)

    def _find_recursive(self, node, orcid):
        if node is None or node.author.orcid == orcid:
            return node
        if orcid < node.author.orcid:
            return self._find_recursive(node.left, orcid)
        return self._find_recursive(node.right, orcid)

    def build_from_graph(self):
        """Build BST using collaboration data from Graph class"""
        # First get the collaboration graph from Graph class
        orcid_to_author, name_to_author, collaboration_graph = build_author_graph(df)

        # Insert each author and their collaborators into BST
        for author, collaborators in collaboration_graph.items():
            self.insert(author, collaborators)

    def print_bst_statistics(self):
        """Print statistics about the BST structure"""
        print("\nBST Statistics:")

        def count_nodes(node):
            if not node:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)

        total_authors = count_nodes(self.root)
        print(f"Total number of authors in BST: {total_authors}")

        def print_author_details(node):
            if node:
                print(f"\nAuthor: {node.author.name} ({node.author.orcid})")
                print(f"Number of collaborators: {len(node.collaborators)}")
                for coauthor, weight in node.collaborators.items():
                    print(f"  - {coauthor.name}: {weight} collaboration(s)")
                print_author_details(node.left)
                print_author_details(node.right)

        print("\nAuthor Details (In-order traversal):")
        print_author_details(self.root)

    def inorder_traversal(self):
        """Perform inorder traversal of the BST"""
        result = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node.author)
                _inorder(node.right)
        _inorder(self.root)
        return result

    def get_author_collaborations(self, orcid):
        """Get collaborations for a specific author"""
        node = self.find_author(orcid)
        if node:
            return node.collaborators
        return None

if __name__ == "__main__":
    # Create BST instance
    bst = Ister3()

    # Build BST using collaboration graph
    bst.build_from_graph()

    # Print BST statistics
    bst.print_bst_statistics()

    # Example: Find specific author's collaborations
    # Replace with actual ORCID
    sample_orcid = "sample_orcid"
    collaborations = bst.get_author_collaborations(sample_orcid)
    if collaborations:
        print(f"\nCollaborations for author with ORCID {sample_orcid}:")
        for coauthor, count in collaborations.items():
            print(f"- {coauthor.name}: {count} collaboration(s)")