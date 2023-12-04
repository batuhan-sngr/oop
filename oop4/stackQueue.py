from abc import ABC, abstractmethod

class Container(ABC):
    @abstractmethod
    def element(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def is_full(self):
        pass

class Stack(Container):
    @abstractmethod
    def push(self, element):
        pass

    @abstractmethod
    def pop(self):
        pass

class Queue(Container):
    @abstractmethod
    def enqueue(self, element):
        pass

    @abstractmethod
    def dequeue(self):
        pass

class ArrayUpStack(Stack, Queue):
    def __init__(self):
        self.size = 5
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

    def enqueue(self, element):
        self.push(element)

    def dequeue(self):
        return self.pop()

class ArrayDownStack(Stack, Queue):
    def __init__(self):
        self.size = 5
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

    def enqueue(self, element):
        self.push(element)

    def dequeue(self):
        return self.pop()

class LinkedStack(Stack, Queue):
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

    def __init__(self):
        self.size = 5
        self.top = None
        self.count = 0

    def push(self, element):
        if not self.is_full():
            new_node = self.Node(element)
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

    def enqueue(self, element):
        self.push(element)

    def dequeue(self):
        return self.pop()

class ArrayQueue(Queue):
    def __init__(self):
        self.size = 5
        self.queue = []

    def enqueue(self, element):
        if not self.is_full():
            self.queue.append(element)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)

    def element(self):
        if not self.is_empty():
            return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    def is_full(self):
        return len(self.queue) == self.size

array_up_stack = ArrayUpStack()
array_down_stack = ArrayDownStack()
linked_stack = LinkedStack()
array_queue = ArrayQueue()

# Push elements into the stacks and the queue
for i in range(1, 6):
    array_up_stack.enqueue(i * 2)
    array_down_stack.enqueue(i * 3)
    linked_stack.enqueue(i * 4)
    array_queue.enqueue(i * 5)

# Dequeue and print elements from the stacks and the queue
print("ArrayUpStack:")
while not array_up_stack.is_empty():
    print(array_up_stack.dequeue())

print("ArrayDownStack:")
while not array_down_stack.is_empty():
    print(array_down_stack.dequeue())

print("LinkedStack:")
while not linked_stack.is_empty():
    print(linked_stack.dequeue())

print("ArrayQueue:")
while not array_queue.is_empty():
    print(array_queue.dequeue())
