import time
import matplotlib.pyplot as plt


class Worker:
    def __init__(self, name, post, subdivision, salary):
        self.name = name
        self.post = post
        self.subdivision = subdivision
        self.salary = salary

    def __lt__(self, other):
        if self.subdivision < other.subdivision:
            return True
        elif self.subdivision > other.subdivision:
            return False
        else:
            if self.name < other.name:
                return True
            elif self.name > other.name:
                return False
            else:
                if self.salary < other.salary:
                    return True
                else:
                    return False

    def __gt__(self, other):
        return not self.__lt__(other)

    def __ge__(self, other):
        if self.subdivision > other.subdivision:
            return True
        elif self.subdivision < other.subdivision:
            return False
        else:
            if self.name > other.name:
                return True
            elif self.name < other.name:
                return False
            else:
                return self.salary >= other.salary

    def __le__(self, other):
        return not self.__ge__(other)

    def __eq__(self, other):
        return self.subdivision == other.subdivision and self.name == other.name and self.salary == other.salary

    def pr(self):
        s = f"{self.name}, {self.post}, {self.subdivision}, {self.salary}"
        return s


unsorted_data = list()
with open('Names.csv', encoding="utf-8") as file:
    next(file)
    for row in file:
        r = row.split(";")
        w = Worker(r[0], r[1], r[2], int(r[3]))
        unsorted_data.append(w)


def sort_insert(lst):
    N = len(lst)
    for i in range(1, N):
        for j in range(i, 0, -1):
            if lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
            else:
                break
    return lst


def cocktail_sort(l):
    for i in range(len(l) - 1, 0, -1):
        swapped = False

        for j in range(i, 0, -1):
            if l[j] < l[j - 1]:
                l[j], l[j - 1] = l[j - 1], l[j]
                swapped = True

        for j in range(i):
            if l[j] > l[j + 1]:
                l[j], l[j + 1] = l[j + 1], l[j]
                swapped = True

        if not swapped:
            return l


def merge_list(a, b):
    c = []
    N = len(a)
    M = len(b)

    i = 0
    j = 0
    while i < N and j < M:
        if a[i] <= b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1

    c += a[i:] + b[j:]
    return c


def split_and_merge_list(a):
    N1 = len(a) // 2
    a1 = a[:N1]
    a2 = a[N1:]

    if len(a1) > 1:
        a1 = split_and_merge_list(a1)
    if len(a2) > 1:
        a2 = split_and_merge_list(a2)

    return merge_list(a1, a2)


def make_output(output_name, sorted_data):
    with open(output_name, 'w') as file:
        for i in sorted_data:
            file.write(i.pr())
            file.write('\n')


def make_graph(data, filename, color):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel('Размер выборки')
    ax1.set_ylabel('Время(сек.)')

    x = [point[0] for point in data]
    y = [point[1] for point in data]
    plt.plot(x, y, marker=".", color=color)
    plt.savefig(f"{filename}")


def read_sort_write(sort_alg, color):
    time_list = list()
    for i in range(1, 8):
        unsorted_data = list()
        with open(f'Data_{i}.csv') as file:
            next(file)
            for row in file:
                r = row.split(",")
                w = Worker(r[0], r[1], r[2], int(r[3]))
                unsorted_data.append(w)

        start = time.time()
        sorted_data = sort_alg(unsorted_data)
        end = time.time()

        time_list.append((len(sorted_data), end - start))
        make_output(f'{sort_alg.__name__}_{i}.csv', sorted_data)

    make_graph(time_list, f"{sort_alg.__name__}.png", color)


read_sort_write(sort_insert, 'red')
read_sort_write(cocktail_sort, 'green')
read_sort_write(split_and_merge_list, 'blue')
