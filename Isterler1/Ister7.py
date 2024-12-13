class Ister7:

    @staticmethod
    def dfs_longest_path(graph, start_node, visited=None):
        if visited is None:
            visited = set()

        visited.add(start_node)
        max_path = [start_node]

        for neighbor in graph[start_node]:
            if neighbor not in visited:
                current_path = Ister7.dfs_longest_path(graph, neighbor,
                                                visited.copy())  # Her yolı zaten kod aslında dönücek.Bu visited amacı sadece o yolda döngüye girmemesini sağlamak.

                candidate_path = [start_node] + current_path

                if len(candidate_path) > len(max_path):
                    max_path = candidate_path

        return max_path
