class Ister2:

    @staticmethod
    def preority_Queue():
        priority_Queue = []
        for q in queue["A"]:
            heapPush(priority_Queue, len(priority_Queue), (queue["A"][q], q))

        print(priority_Queue)
        while priority_Queue:
            yazar, value = heapPop(priority_Queue, len(priority_Queue), 0)
            print(f"yazar: {yazar}, value: {value}")
