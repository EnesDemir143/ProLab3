from collections import defaultdict

from Heap1.Heap import Heap


class Ister4:

    @staticmethod
    def build_extended_collaboration_graph_by_id(start_orcid, orcid_to_author, name_to_author, collaboration_graph,
                                                 depth=2):

        start_author = orcid_to_author.get(start_orcid)
        if not start_author:
            raise ValueError(f"Başlangıç yazarı ORCID '{start_orcid}' bulunamadı.")

        # İşbirliği grafını kopyala (başlangıç grafını değiştirmemek için)
        extended_graph = defaultdict(lambda: defaultdict(int))

        # İşbirliklerinin işbirliklerini takip et
        visited = set()
        to_visit = {start_author}  # Başlangıç yazarıyla başla

        # Depth derecesi kadar gez (2. derece işbirliklerini de alacak)
        for _ in range(depth):
            next_to_visit = set()

            for author in to_visit:
                if author not in visited:
                    visited.add(author)

                    # Bu yazarın tüm işbirlikçileri
                    for coauthor in collaboration_graph[author]:
                        # İlgili işbirlikleri grafını güncelle
                        extended_graph[author][coauthor] = collaboration_graph[author][coauthor]
                        extended_graph[coauthor][author] = collaboration_graph[coauthor][author]
                        next_to_visit.add(coauthor)

            to_visit = next_to_visit

        return extended_graph

    @staticmethod
    def dijkstra(graph, src, dest):
        queue = []
        history = []
        import sys
        inf = sys.maxsize
        node_Data = {}
        for node in graph:
            node_Data[node] = {
                "cost": inf,
                "path": []
            }

        node_Data[src]["cost"] = 0
        node_Data[src]["path"].append(src)

        min_heap = []
        Heap.heapPush(min_heap, 0, (0, src))

        visited_Nodes = set()

        while min_heap:
            history.append({k: {"cost": v["cost"], "path": v["path"].copy()} for k, v in node_Data.items()})
            _ , temp = min_heap[0]
            queue.append(Heap.heapPop(min_heap, len(min_heap), 0))

            if temp == dest:
                return str(node_Data[dest]["cost"]), node_Data[dest]["path"], history,queue

            if temp in visited_Nodes:
                continue

            visited_Nodes.add(temp)
            for j in graph[temp]:
                if j not in visited_Nodes:
                    cost = node_Data[temp]["cost"] + graph[temp][j]
                    if cost < node_Data[j]["cost"]:
                        node_Data[j]["cost"] = cost
                        node_Data[j]["path"] = node_Data[temp]["path"] + [j]
                        Heap.heapPush(min_heap, len(min_heap), (cost, j))
        return "Yol yok", [], history,queue
    @staticmethod
    def print_shortest_paths(start_node, collaboration_graph, orcid_to_author):
        output = []
        for author in collaboration_graph:
            if author == start_node:
                continue
            path = Ister4.dijkstra(collaboration_graph, start_node, author)
            if path:
                cost, nodes, _, _ = path
                node_names = [orcid_to_author[node].name for node in nodes]
                output.append(f"Path from {orcid_to_author[start_node].name} to {orcid_to_author[author].name}: {' -> '.join(node_names)} with cost {cost}")
        return "\n".join(output)