import sys

from Heap1.Heap import Heap


class Ister1:

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
            Heap.heapPop(min_heap, len(min_heap), 0)

            if temp == dest:
                print(type(node_Data[dest]["path"]))
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