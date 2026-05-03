import random
import time


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.ops = 0

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        self.ops += 4
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        self.ops += 4
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, key):
        self.ops += 1
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        self.ops += 1
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        self.ops += 1
        return self.get_min_value_node(root.left)

    def delete(self, root, key):
        self.ops += 1
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                self.ops += 1
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                self.ops += 1
                temp = root.left
                root = None
                return temp
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if root is None:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        self.ops += 1
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, root, key):
        self.ops += 1
        if root is None or root.key == key:
            return root
        if root.key < key:
            return self.search(root.right, key)
        return self.search(root.left, key)


if __name__ == "__main__":
    random.seed(42)
    data = random.sample(range(1, 100000), 10000)

    tree = AVLTree()
    root = None

    insert_times, insert_ops = [], []
    search_times, search_ops = [], []
    delete_times, delete_ops = [], []

    for val in data:
        tree.ops = 0
        start_time = time.perf_counter()
        root = tree.insert(root, val)
        end_time = time.perf_counter()

        insert_times.append(end_time - start_time)
        insert_ops.append(tree.ops)

    search_data = random.sample(data, 100)
    for val in search_data:
        tree.ops = 0
        start_time = time.perf_counter()
        tree.search(root, val)
        end_time = time.perf_counter()

        search_times.append(end_time - start_time)
        search_ops.append(tree.ops)

    delete_data = random.sample(data, 1000)
    for val in delete_data:
        tree.ops = 0
        start_time = time.perf_counter()
        root = tree.delete(root, val)
        end_time = time.perf_counter()

        delete_times.append(end_time - start_time)
        delete_ops.append(tree.ops)

    print("=== РЕЗУЛЬТАТЫ ЗАМЕРОВ ===")
    print(
        f"Вставка (10000 эл.): Среднее время = {sum(insert_times) / len(insert_times):.8f} сек, Среднее число операций = {sum(insert_ops) / len(insert_ops):.2f}")
    print(
        f"Поиск (100 эл.):     Среднее время = {sum(search_times) / len(search_times):.8f} сек, Среднее число операций = {sum(search_ops) / len(search_ops):.2f}")
    print(
        f"Удаление (1000 эл.): Среднее время = {sum(delete_times) / len(delete_times):.8f} сек, Среднее число операций = {sum(delete_ops) / len(delete_ops):.2f}")