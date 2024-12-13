class Heap:

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

            Heap.heapify(arr, n, smallest)

    @staticmethod
    def heapSort(arr, i, n):
        arr[i], arr[n - 1] = arr[n - 1], arr[i]

        Heap.heapify(arr, n - 1, i)

    @staticmethod
    def heapPop(arr, n, i):
        if n == 0:
            return None

        arr[i], arr[n - 1] = arr[n - 1], arr[i]

        Heap.heapify(arr, n - 1, i)
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
