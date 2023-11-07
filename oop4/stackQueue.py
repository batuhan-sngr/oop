class Stack:
    def __init__(self, size):
        """
        Initialize a stack with a specified size.
        """
        pass
    def push(self, element):
        """
        Push an element onto the stack.
        """
        pass
    def pop(self):
        """
        Remove and return the top element from the stack.
        """
        pass
    def element(self):
        """
        Return the top element of the stack without removing it.
        """
        pass
    def is_empty(self):
        """
        Check if the stack is empty.
        """
        pass
    def is_full(self):
        """
        Check if the stack is full.
        """
        pass

class ArrayUpStack(Stack):
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
    
class ArrayDownStack(Stack):
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

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedStack(Stack):
    def __init__(self):
        self.size = 5
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

up_stack = ArrayUpStack()
down_stack = ArrayDownStack()
linked_stack = LinkedStack()

for i in range(1, 6):
    up_stack.push(i * 2)  
    down_stack.push(i * 3)  
    linked_stack.push(i * 4)  

print("ArrayUpStack:")
while not up_stack.is_empty():
    print(up_stack.pop())

print("ArrayDownStack:")
while not down_stack.is_empty():
    print(down_stack.pop())

print("LinkedStack:")
while not linked_stack.is_empty():
    print(linked_stack.pop())
