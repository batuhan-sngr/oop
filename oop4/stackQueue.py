from abc import ABC, abstractmethod

class Queue(ABC):
    @abstractmethod
    def enqueue(self, element):
        pass

    @abstractmethod
    def dequeue(self):
        pass

    @abstractmethod
    def front(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def is_full(self):
        pass

class Stack(Collection):
    def __init__(self, size):
        self.size = size

    @abstractmethod
    def push(self, element):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def element(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def is_full(self):
        pass

class ArrayUpStack(Stack):
    def __init__(self):
        super().__init__(size=5)
        self.stack = []

    def push(self, element):
        if not self.is_full():
            self.stack.insert(0, element)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop(0)

    def element(self):
        if not self.is_empty():
            return self.stack[0]

    def is_empty(self):
        return len(self.stack) == 0

    def is_full(self):
        return len(self.stack) == self.size

class ArrayDownStack(Stack):
    def __init__(self):
        super().__init__(size=5)
        self.stack = []

    def push(self, element):
        if not self.is_full():
            self.stack.append(element)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()

    def element(self):
        if not self.is_empty():
            return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def is_full(self):
        return len(self.stack) == self.size

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedStack(Stack):
    def __init__(self):
        super().__init__(size=5)
        self.top = None
        self.count = 0

    def push(self, element):
        if not self.is_full():
            new_node = Node(element)
            new_node.next = self.top
            self.top = new_node
            self.count += 1

    def pop(self):
        if not self.is_empty():
            data = self.top.data
            self.top = self.top.next
            self.count -= 1
            return data

    def element(self):
        if not self.is_empty():
            return self.top.data

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == self.size

class ArrayUpQueue(Queue):
    def __init__(self):
        super().__init__()
        self.queue = []

    def enqueue(self, element):
        self.queue.append(element)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)

    def front(self):
        if not self.is_empty():
            return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    def is_full(self):
        return False

class ArrayDownQueue(Queue):
    def __init__(self):
        super().__init__()
        self.queue = []

    def enqueue(self, element):
        self.queue.append(element)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)

    def front(self):
        if not self.is_empty():
            return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    def is_full(self):
        return False

class LinkedQueue(Queue):
    def __init__(self):
        super().__init__()
        self.front_node = None
        self.rear_node = None
        self.count = 0

    def enqueue(self, element):
        new_node = Node(element)
        if self.is_empty():
            self.front_node = new_node
            self.rear_node = new_node
        else:
            self.rear_node.next = new_node
            self.rear_node = new_node
        self.count += 1

    def dequeue(self):
        if not self.is_empty():
            data = self.front_node.data
            self.front_node = self.front_node.next
            self.count -= 1
            return data

    def front(self):
        if not self.is_empty():
            return self.front_node.data

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return False

up_stack = ArrayUpStack()
down_stack = ArrayDownStack()
linked_stack = LinkedStack()

up_queue = ArrayUpQueue()
down_queue = ArrayDownQueue()
linked_queue = LinkedQueue()

for i in range(1, 6):
    up_stack.push(i * 2)
    down_stack.push(i * 3)
    linked_stack.push(i * 4)

    up_queue.enqueue(i * 2)
    down_queue.enqueue(i * 3)
    linked_queue.enqueue(i * 4)

print("ArrayUpStack:")
while not up_stack.is_empty():
    print(up_stack.pop())

print("ArrayDownStack:")
while not down_stack.is_empty():
    print(down_stack.pop())

print("LinkedStack:")
while not linked_stack.is_empty():
    print(linked_stack.pop())

print("ArrayUpQueue:")
while not up_queue.is_empty():
    print(up_queue.dequeue())

print("ArrayDownQueue:")
while not down_queue.is_empty():
    print(down_queue.dequeue())

print("LinkedQueue:")
while not linked_queue.is_empty():
    print(linked_queue.dequeue())
