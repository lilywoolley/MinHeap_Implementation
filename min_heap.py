# Name: Lily Woolley
# OSU Email: woolleyw@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5
# Due Date: 2/28/22
# Description: Implentation of a Min Heap Data Structure

# Import DynamicArray from Assignment 2
from itertools import count
from os import remove
from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self.heap[i] for i in range(self.heap.length())]
        return 'HEAP ' + str(heap_data)

    def is_empty(self) -> bool:
        """
        Returns true if the length is 0, otherwise returns false
        """
        if self.heap.length() == 0:
            return True
        else:
            return False

    def parent(self, index):
        """
        Finds the index of the parent
        """
        return (index - 1) // 2

    def swap(self, first_index: int, new_index: int) -> None:
        """
        Swaps the values of two different indexes
        """
        holder = self.heap[new_index]
        
        self.heap[new_index] = self.heap[first_index]
        self.heap[first_index] = holder
        return

    def percolate_up(self, index) -> None:
        """
        Compares the child value to the parent value, swaps them if true and changes the index for comparison
        """
        while (index != 0 and self.heap[self.parent(index)] >= self.heap[index]):
            self.swap(index, self.parent(index))
            index = self.parent(index)

    def add(self, node: object) -> None:
        """
        Inserts a new node into the heap and re-establishes proper heap structure
        """
        self.heap.append(node)
        childIndex = self.heap.length() - 1

        #Stops here if the heap was empty before the add
        if self.heap.length() == 1:
            return
        #Calls percolate to do the comparison and swapping neccesary for proper heap structure
        else:
            self.percolate_up(childIndex)
            return
    
    def get_min(self) -> object:
        """
        Returns the value of the root, which is the smallest value
        """
        if self.heap.length() == 0:
            raise MinHeapException
        else:
            return self.heap[0]

    def left_child(self, index) -> int:
            """
            Finds the index of the left child
            """
            return 2 * index + 1

    def right_child(self, index) -> int:
        """
        Finds the index of the right child
        """
        return 2 * index + 2
    
    def percolate_down(self, index, removedNode) -> None:           
        """
        Compares the value of the parent to it's left and right child, performs the appropriate swap if true
        """                       
        while (self.heap[index] >= self.heap[self.left_child(index)] or self.heap[index] >= self.heap[self.right_child(index)]):                                                                           
            #If the children's values are equal
            if self.heap[self.left_child(index)] == self.heap[self.right_child(index)]:
                self.swap(index, self.left_child(index))
                index = self.left_child(index)
            #If the left is smaller than the right
            elif self.heap[self.left_child(index)] < self.heap[self.right_child(index)]:
                self.swap(index, self.left_child(index))
                index = self.left_child(index)
            #If the right is smaller than the left
            else:
                self.swap(index, self.right_child(index))
                index = self.right_child(index)
            #If after first percolation right index is outside the array
            if (self.left_child(index) < self.heap.length() and self.right_child(index) >= self.heap.length()) and self.heap[index] >= self.heap[self.left_child(index)]:                            
                self.swap(index, self.left_child(index))
                index = self.left_child(index)
                break
            if self.left_child(index) >= self.heap.length() or self.right_child(index) >= self.heap.length():
                break

    def remove_min(self) -> object:
        """
        Replaces the root node with the last node in the heap, percolates that node until proper heap structure is re-established
        Returns the removed root value
        """
        #If the heap is empty
        if self.heap.length() == 0:
            raise MinHeapException
        removedNode = self.heap.pop_front()
        #If the heap is empty after removal, stops here
        if self.heap.length() == 0:
            return removedNode
        #If the heap has exactly one node after removal, stops here
        elif self.heap.length() == 1:
            return removedNode       
        #Otherwise, percolates the replacement value down
        else:
            self.heap.push(self.heap[self.heap.length() - 1])
            self.heap.pop_back()       
            newIndex = 0 
            #Checks if there is a left child without a right child
            if (self.left_child(newIndex) < self.heap.length() and self.right_child(newIndex) >= self.heap.length()) and self.heap[newIndex] >= self.heap[self.left_child(newIndex)]:                            
                    self.swap(newIndex, self.left_child(newIndex))
                    return removedNode
            #Checks if both children exist
            elif self.left_child(newIndex) < self.heap.length() and self.right_child(newIndex) < self.heap.length():
                #If they do and one is smaller than the new root, percolates
                if self.heap[newIndex] >= self.heap[self.left_child(newIndex)] or self.heap[newIndex] >= self.heap[self.right_child(newIndex)]:
                    self.percolate_down(newIndex, removedNode)
                    return removedNode
                #If they're both bigger, no percolation needed
                else:
                    return removedNode
            #If there isn't a left child, there isn't a right child, stops
            else:
                return removedNode
    
    def find_first_nonleaf(self, number_of_nodes):
        return (number_of_nodes // 2) - 1
    
    def build_heap(self, da: DynamicArray) -> None:
        """
        Takes an unsorted dynamic array, and makes it into a proper Min Heap
        """
        self.heap = da       
        index = self.find_first_nonleaf(self.heap.length())
        #Checks the first possible nonleaf element and percolates down from there until it reaches the root    
        while index >= 0:            
            #Checks if there is a left child without a right child
            if (self.left_child(index) < self.heap.length() and self.right_child(index) >= self.heap.length()) and self.heap[index] >= self.heap[self.left_child(index)]:                            
                    self.swap(index, self.left_child(index))
                    index = index - 1
            #Checks if both children exist
            elif self.left_child(index) < self.heap.length() and self.right_child(index) < self.heap.length():
                #If they do and one is smaller than the new root, percolates
                if self.heap[index] >= self.heap[self.left_child(index)] or self.heap[index] >= self.heap[self.right_child(index)]:
                    self.percolate_down(index, None)
                    index = index - 1 
                #If they're both bigger, no percolation needed
                else:
                    index = index - 1 
            #If there isn't a left child, there isn't a right child, checks next index
            else:
                index = index - 1 
            
    def size(self) -> int:
        """
        Returns the number of values stored in the heap
        """
        return self.heap.length()

    def clear(self) -> None:
        """
        TODO: Write this implementation
        """
        emptyHeap = DynamicArray()
        self.heap = emptyHeap

    def percolate_down_heapsort_edition(self, index, counter) -> None:           
        """
        Compares the value of the parent to it's left and right child, performs the appropriate swap if true
        """                       
        while (self.heap[index] >= self.heap[self.left_child(index)] or self.heap[index] >= self.heap[self.right_child(index)]):                                                                           
            #If the children's values are equal
            if self.heap[self.left_child(index)] == self.heap[self.right_child(index)]:
                self.swap(index, self.left_child(index))
                index = self.left_child(index)
            #If the left is smaller than the right
            elif self.heap[self.left_child(index)] < self.heap[self.right_child(index)]:
                self.swap(index, self.left_child(index))
                index = self.left_child(index)
            #If the right is smaller than the left
            else:
                self.swap(index, self.right_child(index))
                index = self.right_child(index)
            #If after first percolation right index is outside the array
            if (self.left_child(index) <= counter and self.right_child(index) > counter) and self.heap[index] >= self.heap[self.left_child(index)]:                            
                self.swap(index, self.left_child(index))
                index = self.left_child(index)
                break
            if self.left_child(index) >= counter and self.right_child(index) >= counter:
                break

def heapsort(da: DynamicArray) -> None:
    """
    Takes and unsorted Dynamic Array, creates a min heap out of it using build_heap, then sorts the values of the heap in non-ascending order back into the Dynamic Array
    """
    heapedArray = MinHeap()
    heapedArray.build_heap(da)
    counter = heapedArray.heap.length() - 1
    
    while counter > 0:       
        heapedArray.swap(0, counter)
        counter = counter - 1
        
        #Checks if there is a left child without a right child
        if (heapedArray.left_child(0) < counter and heapedArray.right_child(0) >= counter) and heapedArray.heap[0] < heapedArray.heap[heapedArray.left_child(0)]:                            
            heapedArray.swap(0, heapedArray.left_child(0))
        #Checks if both children exist
        elif heapedArray.left_child(0) < counter and heapedArray.right_child(0) <= counter:
            #If they do and one is smaller than the new root, percolates
            if heapedArray.heap[0] >= heapedArray.heap[heapedArray.left_child(0)] or heapedArray.heap[0] >= heapedArray.heap[heapedArray.right_child(0)]:
                heapedArray.percolate_down_heapsort_edition(0, counter)
            #If they're both bigger, no percolation needed
            else:
                continue                
        #Special case for if the counter is 0 because nothing will be smaller than zero, does the comparison with the only possible child with a value smaller than the root
        elif counter == 0:
            if heapedArray.heap[0] <= heapedArray.heap[heapedArray.left_child(0)]:
                heapedArray.swap(0, heapedArray.left_child(0))                               
        #If there isn't a left child, there isn't a right child, checks next index
        else:
            continue        

# BASIC TESTING
if __name__ == '__main__':
    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap()
    h.heap = DynamicArray([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da[0] = 500
    print(da)
    print(h)

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)