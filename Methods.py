class Methods:

    @staticmethod
    def en_cok_isbirligi_yapan_yazari_bul(graph):

        en_fazla_isbirligi = 0
        en_cok_isbirligi_yapan_yazar = None

        for yazar, ortak_yazarlar in graph.items():
            ortak_yazar_sayisi = len(ortak_yazarlar)

            if ortak_yazar_sayisi > en_fazla_isbirligi:
                en_fazla_isbirligi = ortak_yazar_sayisi
                en_cok_isbirligi_yapan_yazar = yazar

        return (en_cok_isbirligi_yapan_yazar, en_fazla_isbirligi)

    @staticmethod
    def dfs_longest_path(graph, start_node, visited=None):
        if visited is None:
            visited = set()

        visited.add(start_node)
        max_path = [start_node]

        for neighbor in graph[start_node]:
            if neighbor not in visited:
                current_path = Methods.dfs_longest_path(graph, neighbor,
                                                visited.copy())  # Her yolı zaten kod aslında dönücek.Bu visited amacı sadece o yolda döngüye girmemesini sağlamak.

                candidate_path = [start_node] + current_path

                if len(candidate_path) > len(max_path):
                    max_path = candidate_path

        return max_path

    @staticmethod
    def dijkstra(graph, src, dest):
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
        Methods.heapPush(min_heap, 0, (0, src))

        visited_Nodes = set()

        while min_heap:
            history.append({k: {"cost": v["cost"], "path": v["path"].copy()} for k, v in node_Data.items()})
            current_cost, temp = min_heap[0]
            Methods.heapPop(min_heap, len(min_heap), 0)

            if temp == dest:
                return str(node_Data[dest]["cost"]), node_Data[dest]["path"], history

            if temp in visited_Nodes:
                continue

            visited_Nodes.add(temp)
            for j in graph[temp]:
                if j not in visited_Nodes:
                    cost = node_Data[temp]["cost"] + graph[temp][j]
                    if cost < node_Data[j]["cost"]:
                        node_Data[j]["cost"] = cost
                        node_Data[j]["path"] = node_Data[temp]["path"] + [j]
                        Methods.heapPush(min_heap, len(min_heap), (cost, j))

        return "Yol yok", [], history

    @staticmethod
    def heapify(arr, n, i):
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left][0] < arr[smallest][0]:
            smallest = left

        if right < n and arr[right][0] < arr[smallest][0]:
            smallest = right

        if smallest != i:
            arr[smallest], arr[i] = arr[i], arr[smallest]

            Methods.heapify(arr, n, smallest)

    @staticmethod
    def heapSort(arr, i, n):
        arr[i], arr[n - 1] = arr[n - 1], arr[i]

        Methods.heapify(arr, n - 1, i)

    @staticmethod
    def heapPop(arr, n, i):
        if n == 0:
            return None

        arr[i], arr[n - 1] = arr[n - 1], arr[i]

        Methods.heapify(arr, n - 1, i)
        return arr.pop()

    @staticmethod
    def heapPush(arr, n, val):
        arr.append(val)

        while n > 0:
            parent = (n - 1) // 2
            if arr[n][0] < arr[parent][0]:
                arr[parent], arr[n] = arr[n], arr[parent]
                n = parent
            else:
                break
