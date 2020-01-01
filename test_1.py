import resource
"""
array = list()
for _ in range(int(input())):
    array.append(int(input()))
"""
INTERVAL = 6
array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(len(array) - INTERVAL if len(array) - INTERVAL > 0 else 0):
    for num in array[INTERVAL + i:]:
        if (array[i] + num) % 3 == 0:
            print(array[i], num)
    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)