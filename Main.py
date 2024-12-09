import time
import pandas as pd

start = time.time()
df = pd.read_excel("/Users/enesdemir/Desktop/ProLab3/Data/PROLAB 3 - DATASET.xlsx")
end = time.time()

def heapify(arr,n,i):
    smallest = i
    left = 2*i+1
    right = 2*i+2

    if left < n and arr[left][0] < arr[smallest][0] :
        smallest = left

    if right < n and arr[right][0]  < arr[smallest][0] :
        smallest = right

    if smallest != i:
        arr[smallest], arr[i] = arr[i], arr[smallest]

        heapify(arr,n,smallest)

def heapSort(arr,i,n):
    arr[i],arr[n-1]=arr[n-1],arr[i]

    heapify(arr,n-1,i)

def heapPop(arr,n,i):
    if n == 0:
        return None

    arr[i],arr[n-1]=arr[n-1],arr[i]

    heapify(arr,n-1,i)
    return arr.pop()

def heapPush(arr,n,val):
    arr.append(val)

    while n>0:
        parent = (n - 1) // 2
        if arr[n][0] < arr[parent][0]:
            arr[parent], arr[n] = arr[n], arr[parent]
            n = parent
        else:
            break

def dijkstra(graph, src, dest):
    history=[]
    import  sys
    inf=sys.maxsize
    node_Data={}
    for node in graph:
        node_Data[node]= {
            "cost" :inf,
            "path":[]
        }

    node_Data[src]["cost"]=0
    node_Data[src]["path"].append(src)

    min_heap=[]
    heapPush(min_heap,0,(0,src))

    visited_Nodes=set()

    while min_heap:
        history.append({k: {"cost": v["cost"], "path": v["path"].copy()} for k, v in node_Data.items()})
        current_cost, temp = min_heap[0]
        heapPop(min_heap, len(min_heap), 0)

        if temp == dest:
            return str(node_Data[dest]["cost"]), node_Data[dest]["path"],history

        if temp in visited_Nodes:
            continue


        visited_Nodes.add(temp)
        for j in graph[temp]:
            if  j not in visited_Nodes:
                cost=node_Data[temp]["cost"]+graph[temp][j]
                if cost < node_Data[j]["cost"]:
                    node_Data[j]["cost"]=cost
                    node_Data[j]["path"]=node_Data[temp]["path"] + [j]
                    heapPush(min_heap,len(min_heap),(cost,j))


    return "Yol yok", [],history

def dfs_longest_path(graph, start_node, visited=None):
    if visited is None:
        visited = set()

    visited.add(start_node)
    max_path = [start_node]

    for neighbor in graph[start_node]:
        if neighbor not in visited:
            current_path = dfs_longest_path(graph, neighbor, visited.copy()) #Her yolı zaten kod aslında dönücek.Bu visited amacı sadece o yolda döngüye girmemesini sağlamak.

            candidate_path = [start_node] + current_path

            if len(candidate_path) > len(max_path):
                max_path = candidate_path

    return max_path

def en_cok_isbirligi_yapan_yazari_bul(graph):

    en_fazla_isbirligi = 0
    en_cok_isbirligi_yapan_yazar = None


    for yazar, ortak_yazarlar in graph.items():
        ortak_yazar_sayisi = len(ortak_yazarlar)


        if ortak_yazar_sayisi > en_fazla_isbirligi:
            en_fazla_isbirligi = ortak_yazar_sayisi
            en_cok_isbirligi_yapan_yazar = yazar

    return (en_cok_isbirligi_yapan_yazar, en_fazla_isbirligi)


graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 1, 'D': 5},
    'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
    'D': {'B': 5, 'C': 8, 'E': 2},
    'E': {'C': 10, 'D': 2}
}
start=time.time()
maliyet, yol ,history= dijkstra(graph, 'A', 'E')
end=time.time()
for i, step in enumerate(history, 1):
    print(f"\nAdım {i}:")
    for node, data in step.items():
        print(f"{node}: Maliyet = {data['cost']}, Yol = {data['path']}")
print(f"En kısa yol maliyeti: {maliyet}")
print(f"Yol: {' -> '.join(yol)}")
print(end-start)

graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 1, 'D': 5},
    'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
    'D': {'B': 5, 'C': 8, 'E': 2},
    'E': {'C': 10, 'D': 2},
}


print(list(graph["A"].keys()))

current_path = dfs_longest_path(graph, 'A')
print(f"Longest path: {current_path}")
print(f"Path length: {len(current_path)}")

x,y=en_cok_isbirligi_yapan_yazari_bul(graph)
print("En çok iş birliği yapan yazar:{}  || İş birliği sayısı:{}".format(x,y))


#Priority queue.
queue={
    "A":{
        "B": 4,
        "C": 2,
        "D": 5,
        "E": 10,
        "F": 7,
        "G": 3,
        "H": 11,
        "I": 9,
    }
}

priority_Queue=[]
for q in queue["A"]:
    heapPush(priority_Queue,len(priority_Queue),(queue["A"][q],q))

print(priority_Queue)
while priority_Queue:
    yazar,value=heapPop(priority_Queue,len(priority_Queue),0)
    print(f"yazar: {yazar}, value: {value}")



class Author:
    def __init__(self,name, id=0):
        self.name = name
        self.id = id
        self.article = set()

if __name__ == "__main__":
    ids = set()
    authorsObjects = []
    authorsObjectsNames = []
    articlesDict = {}
    for dois, paper in zip(df["doi"], df["paper_title"]):
        articlesDict[dois] = paper
    print(len(articlesDict))
    print(len(df["doi"]))

    author_to_id = {}
    author_to_name = {}
    for id, name in zip(df["orcid"], df["author_name"]):
        name =name.strip()
        if name in " A. Parandaman":
            print(len(name))
        if id not in ids:
            ids.add(id)
            author = Author(id,name)
            authorsObjects.append(author)
            author_to_id[id] = author
            author_to_name[name] = author
        elif id in ids:
            author_to_name[name]=author_to_id[id]
    print(len(author_to_name))
    print(len(authorsObjects))
    start = time.time()
    print("Makaleler işleniyor...")

    # Her makale için yazarları işle
    for coauthors_str, doi, index in zip(df["coauthors"], df["doi"],df["author_position"]):
        coauthors=coauthors_str.strip('[]').replace("'", "").split(',')
        coauthors=[name.strip() for name in coauthors]

        author_to_name[coauthors[index-1]].article.add(doi)

    print(author_to_id["0000-0003-0788-1499"].article)