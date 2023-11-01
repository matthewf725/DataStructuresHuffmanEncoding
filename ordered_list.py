class Node:
    '''Node for use with doubly-linked list'''
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        self.head = Node(None)
        self.tail = self.head
        self.head.next = self.tail
        self.tail.prev = self.head        

    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        return self.head.next == self.tail

    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance.  Assume that all items added to your 
           list can be compared using the < operator and can be compared for equality/inequality.
           Make no other assumptions about the items in your list'''
        new_node = Node(item)
        current = self.head.next

        while current != self.tail and current.item < item:
            current = current.next

        # Check if the item is already in the list
        if current != self.tail and current.item == item:
            return False

        new_node.next = current
        new_node.prev = current.prev
        current.prev.next = new_node
        current.prev = new_node
        return True

    def remove(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list) 
           returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance'''
        current = self.head.next

        while current != self.tail:
            if current.item == item:
                # Remove the node
                current.prev.next = current.next
                current.next.prev = current.prev
                return True

            current = current.next

        return False

    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''

        current = self.head.next
        index = 0

        while current != self.tail:
            if current.item == item:
                return index

            current = current.next
            index += 1

        return None

    def pop(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''

        if index < 0:
            raise IndexError("Index cannot be negative")

        current = self.head.next
        current_index = 0

        while current != self.tail and current_index < index:
            current = current.next
            current_index += 1

        if current == self.tail or current_index != index:
            raise IndexError("Index out of range")

        # Remove the node
        current.prev.next = current.next
        current.next.prev = current.prev

        return current.item

    def search(self, item):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance'''
        return self.searchHelper(self.head.next, item)

    def searchHelper(self, node, item):
        if node == self.tail:
            return False
        if node.item == item:
            return True
        return self.searchHelper(node.next, item)
    
    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        orderList = []
        node = self.head.next
        while node != self.tail:
            orderList.append(node.item)
            node = node.next
        return orderList

    def python_list_reversed(self):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        reversedList = []
        self.python_list_reversedHelper(self.tail.prev, reversedList)
        return reversedList
    
    def python_list_reversedHelper(self, node, reversedList):
        if node == self.head:
            return
        reversedList.append(node.item)
        self.python_list_reversedHelper(node.prev, reversedList)

    def size(self):
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        return self.sizeHelper(self.head.next)

    def sizeHelper(self, node):
        if node == self.tail:
            return 0
        return 1 + self.sizeHelper(node.next)