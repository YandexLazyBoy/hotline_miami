axy = list(map(int, input().split()))  # через пробел вводятся ширина и длина
oxy = list(map(lambda s: int(s) - 1, input().split()))  # опять же через пробел координаты начала дырки
dxy = list(map(int, input().split()))  # координаты конца

array = list()
for y in range(axy[1]):
    if y == 0:
        array.append([1 if k < oxy[0] or k >= dxy[0] or oxy[1] > 0 else 0 for k in range(axy[0])])
    else:
        for x in range(axy[0]):
            if x == 0:
                array.append([1 if oxy[0] > 0 else 0])
            else:
                if y < oxy[1] or y >= dxy[1] or x < oxy[0] or x >= dxy[0]:
                    array[y].append(array[y][x - 1] + array[y - 1][x])
                else:
                    array[y].append(0)
print(*array, sep='\n')  # вывод массива (если не надо, просто удалите)
print(array[-1][-1])  # ответ, собсна
