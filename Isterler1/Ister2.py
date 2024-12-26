from Heap1.Heap import Heap


class Ister2:

    @staticmethod
    def preority_Queue(queue):
        priority_Queue = []
        Heap.heapPush(priority_Queue,len(priority_Queue),(len(queue["A"]),"A"))
        for q in queue["A"]:
            print(type(queue))
            Heap.heapPush(priority_Queue, len(priority_Queue), (queue["A"][q], q))

        print(priority_Queue)
        while priority_Queue:
            yazar, value = Heap.heapPop(priority_Queue, len(priority_Queue), 0)
            print(f"yazar: {yazar}, value: {value}")
        return priority_Queue