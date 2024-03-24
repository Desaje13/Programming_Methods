import sys
import timeit
import matplotlib.pyplot as plt

sys.setrecursionlimit(200000)


class Worker:
    def __init__(self, name, post, subdivision, salary):
        self.name = name
        self.post = post
        self.subdivision = subdivision
        self.salary = salary

    def get_info(self):
        print(f'{self.name}, {self.post}, {self.subdivision}, {self.salary}')

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


class TreeNode:
    def __init__(self, value=None, content=None):
        self.left = None
        self.right = None
        self.value = value
        self.content = content

    def insert(self, value, content=None):
        if self.value is None:
            self.value = value
            self.content = content
        elif value < self.value:
            if self.left is None:
                self.left = TreeNode(value, content)
            else:
                self.left.insert(value, content)
        else:
            if self.right is None:
                self.right = TreeNode(value, content)
            else:
                self.right.insert(value, content)

    def traversal(self):
        if self.left:
            self.left.traversal()
        print(self.value, self.content)
        if self.right:
            self.right.traversal()

    def find(self, value):
        if value < self.value:
            if self.left is None:
                raise Exception('error, node content is None')
                # return None
            else:
                return self.left.find(value)
        elif value > self.value:
            if self.right is None:
                raise Exception('error, node content is None')
                # return None
            else:
                return self.right.find(value)
        else:
            return self.content


class RBNode:
    def __init__(self, val, content=None):
        self.red = False
        self.parent = None
        self.val = val
        self.left = None
        self.right = None
        self.content = content


class RBTree:
    def __init__(self):
        self.nil = RBNode(0)
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil

    def insert(self, val, content=None):
        new_node = RBNode(val, content)
        new_node.parent = None
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.red = True
        parent = None
        current = self.root
        while current != self.nil:
            parent = current
            if new_node.val < current.val:
                current = current.left
            elif new_node.val > current.val:
                current = current.right
            else:
                return

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node

        self.fix_insert(new_node)

    def fix_insert(self, new_node):
        while new_node != self.root and new_node.parent.red:
            if new_node.parent == new_node.parent.parent.right:
                u = new_node.parent.parent.left
                if u.red:
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.rotate_left(new_node.parent.parent)
            else:
                u = new_node.parent.parent.right
                if u.red:
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    new_node = new_node.parent.parent

                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.rotate_right(new_node.parent.parent)

        self.root.red = False

    def exists(self, val):
        curr = self.root
        while curr != self.nil and val != curr.val:
            if val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        if curr.content is None:
            raise Exception('error, node content is None')
        else:
            return curr.content

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right

        if y.right != self.nil:
            y.right.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y

        elif x == x.parent.right:
            x.parent.right = y

        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def __repr__(self):
        lines = []
        print_tree(self.root, lines)
        return '\n'.join(lines)


def print_tree(node, lines, level=0):
    if node.val != 0:
        print_tree(node.left, lines, level + 1)
        print(node.val, node.content)
        print_tree(node.right, lines, level + 1)


class HashTable:
    __collisions = 0

    def __init__(self, n=100):
        self.MAX = n
        self.arr = [[] for i in range(self.MAX)]

    def __get_hash(self, key):
        h = 0
        for char in key:
            h += ord(char)
        return h % self.MAX

    def __setitem__(self, key, value):
        hsh = self.__get_hash(key)
        found = False
        for idx, element in enumerate(self.arr[hsh]):
            if len(element) == 2 and element[0] == key and element[1] == value:
                # self.arr[hsh][idx] = (key, value)
                found = True
                break
        if not found and len(self.arr[hsh]) > 0:
            self.arr[hsh].append((key, value))
            self.__collisions += 1
        elif not found:
            self.arr[hsh].append((key, value))

    def __getitem__(self, key):
        hsh = self.__get_hash(key)
        for element in self.arr[hsh]:
            if element[0] == key:
                return element[1]

        raise Exception(f"No {key} key in HashTable")

    def __delitem__(self, key):
        hsh = self.__get_hash(key)
        for idx, element in enumerate(self.arr[hsh]):
            if element[0] == key:
                del self.arr[hsh][idx]

    def get_collisions_number(self):
        return self.__collisions

    def pr(self):
        for i in self.arr:
            print(i)


trees_list = list()
rb_trees_list = list()
hash_tables_list = list()
dicts_list = list()
with open(f'Data_1.csv') as file:
    next(file)
    row_count = sum(1 for row in file)
    file.seek(0)
    next(file)
    tree_1 = TreeNode()
    rb_tree_1 = RBTree()
    table_1 = HashTable(1000)
    d_1 = dict()
    for row in file:
        r = row.split(",")
        w = Worker(r[0], r[1], r[2], int(r[3]))
        tree_1.insert(value=r[0], content=w)
        rb_tree_1.insert(val=r[0], content=w)
        table_1[r[0]] = w
        d_1[r[0]] = w

    trees_list.append(tree_1)
    rb_trees_list.append(rb_tree_1)
    hash_tables_list.append(table_1)
    dicts_list.append(d_1)

with open(f'Data_2.csv') as file:
    next(file)
    row_count = sum(1 for row in file)
    file.seek(0)
    next(file)
    tree_2 = TreeNode()
    rb_tree_2 = RBTree()
    table_2 = HashTable(1000)
    d_2 = dict()
    for row in file:
        r = row.split(",")
        w = Worker(r[0], r[1], r[2], int(r[3]))
        tree_2.insert(value=r[0], content=w)
        rb_tree_2.insert(val=r[0], content=w)
        table_2[r[0]] = w
        d_2[r[0]] = w

    trees_list.append(tree_2)
    rb_trees_list.append(rb_tree_2)
    hash_tables_list.append(table_2)
    dicts_list.append(d_2)

with open(f'Data_3.csv') as file:
    next(file)
    row_count = sum(1 for row in file)
    file.seek(0)
    next(file)
    tree_3 = TreeNode()
    rb_tree_3 = RBTree()
    table_3 = HashTable(1000)
    d_3 = dict()
    for row in file:
        r = row.split(",")
        w = Worker(r[0], r[1], r[2], int(r[3]))
        tree_3.insert(value=r[0], content=w)
        rb_tree_3.insert(val=r[0], content=w)
        table_3[r[0]] = w
        d_3[r[0]] = w

    trees_list.append(tree_3)
    rb_trees_list.append(rb_tree_3)
    hash_tables_list.append(table_3)
    dicts_list.append(d_3)

with open(f'Data_4.csv') as file:
    next(file)
    row_count = sum(1 for row in file)
    file.seek(0)
    next(file)
    tree_4 = TreeNode()
    rb_tree_4 = RBTree()
    table_4 = HashTable(1000)
    d_4 = dict()
    for row in file:
        r = row.split(",")
        w = Worker(r[0], r[1], r[2], int(r[3]))
        tree_4.insert(value=r[0], content=w)
        rb_tree_4.insert(val=r[0], content=w)
        table_4[r[0]] = w
        d_4[r[0]] = w

    trees_list.append(tree_4)
    rb_trees_list.append(rb_tree_4)
    hash_tables_list.append(table_4)
    dicts_list.append(d_4)

with open(f'Data_5.csv') as file:
    next(file)
    row_count = sum(1 for row in file)
    file.seek(0)
    next(file)
    tree_5 = TreeNode()
    rb_tree_5 = RBTree()
    table_5 = HashTable(1000)
    d_5 = dict()
    for row in file:
        r = row.split(",")
        w = Worker(r[0], r[1], r[2], int(r[3]))
        tree_5.insert(value=r[0], content=w)
        rb_tree_5.insert(val=r[0], content=w)
        table_5[r[0]] = w
        d_5[r[0]] = w

    trees_list.append(tree_5)
    rb_trees_list.append(rb_tree_5)
    hash_tables_list.append(table_5)
    dicts_list.append(d_5)

with open(f'Data_6.csv') as file:
    next(file)
    row_count = sum(1 for row in file)
    file.seek(0)
    next(file)
    tree_6 = TreeNode()
    rb_tree_6 = RBTree()
    table_6 = HashTable(1000)
    d_6 = dict()
    for row in file:
        r = row.split(",")
        w = Worker(r[0], r[1], r[2], int(r[3]))
        tree_6.insert(value=r[0], content=w)
        rb_tree_6.insert(val=r[0], content=w)
        table_6[r[0]] = w
        d_6[r[0]] = w

    trees_list.append(tree_6)
    rb_trees_list.append(rb_tree_6)
    hash_tables_list.append(table_6)
    dicts_list.append(d_6)

with open(f'Data_7.csv') as file:
    next(file)
    row_count = sum(1 for row in file)
    file.seek(0)
    next(file)
    tree_7 = TreeNode()
    rb_tree_7 = RBTree()
    # table_7 = HashTable(row_count)
    table_7 = HashTable(10000)
    d_7 = dict()
    for row in file:
        r = row.split(",")
        w = Worker(r[0], r[1], r[2], int(r[3]))
        tree_7.insert(value=r[0], content=w)
        rb_tree_7.insert(val=r[0], content=w)
        table_7[r[0]] = w
        d_7[r[0]] = w

    trees_list.append(tree_7)
    rb_trees_list.append(rb_tree_7)
    hash_tables_list.append(table_7)
    dicts_list.append(d_7)


def make_graph(data, filename, color='red'):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel('Размер выборки')
    ax1.set_ylabel('Время(сек.)')

    x = [point[0] for point in data]
    y = [point[1] for point in data]
    plt.plot(x, y, marker=".", color=color)
    plt.savefig(f"{filename}")


print("Бинарные деревья:")
time_list = list()
c = 1
for i in trees_list:
    start = timeit.default_timer()
    i.find('Пётр Волков').get_info()
    end = timeit.default_timer()
    time_list.append((f"Data_{c}", end - start))
    print(f"Время работы для структуры данных №{c}: {end - start} \n")
    c += 1
make_graph(time_list, "Бинарные деревья.png")

print("Чёрно-красные бинарные деревья:")
time_list = list()
c = 1
for i in rb_trees_list:
    start = timeit.default_timer()
    i.exists('Пётр Волков').get_info()
    end = timeit.default_timer()
    time_list.append((f"Data_{c}", end - start))
    print(f"Время работы для структуры данных №{c}: {end - start} \n")
    c += 1
make_graph(time_list, "Чёрно-красные бинарные деревья.png")

print("Хэш таблицы:")
time_list = list()
c = 1
collisions_list = list()
for i in hash_tables_list:
    start = timeit.default_timer()
    i['Пётр Волков'].get_info()
    print(f"Коллизий: {i.get_collisions_number()}")
    collisions_list.append((f"Data_{c}", i.get_collisions_number()))
    end = timeit.default_timer()
    time_list.append((f"Data_{c}", end - start))
    print(f"Время работы для структуры данных №{c}: {end - start} \n")
    c += 1
make_graph(time_list, "Хэш таблицы.png")
make_graph(collisions_list, "Коллизии.png")

print("Стандартные словари:")
time_list = list()
c = 1
for i in dicts_list:
    start = timeit.default_timer()
    i['Пётр Волков'].get_info()
    end = timeit.default_timer()
    time_list.append((f"Data_{c}", end - start))
    print(f"Время работы для структуры данных №{c}: {end - start} \n")
    c += 1
make_graph(time_list, "Стандартные словари.png")
