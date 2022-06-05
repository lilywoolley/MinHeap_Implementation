from static_array import *


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.size = 0
        self.capacity = 4
        self.data = StaticArray(self.capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self.size) + "/" + str(self.capacity) + ' ['
        out += ', '.join([str(self.data[_]) for _ in range(self.size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self.index]
        except DynamicArrayException:
            raise StopIteration
        self.index = self.index + 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self.size:
            raise DynamicArrayException
        return self.data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self.size:
            raise DynamicArrayException
        self.data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.size

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Implements a resize function that creates a new array with the desired capacity and copies the original data into the new larger array
        """
        #Checks to ensure the new capacity is greater than 0 and the size
        if new_capacity <= 0:
            return
        else:
            if new_capacity < self.size:
                return
            #Creates new array with the new capacity and rewrites the orginal elements to it
            else:
                newArr = StaticArray(new_capacity)
          
                for i in range(self.size):
                    newArr[i] = self.data[i]
          
            #Sets the original array to the new one and updates the capacity
            self.data = newArr
            self.capacity = new_capacity                
                
               
    def append(self, value: object) -> None:
        """
        Implements an append function that adds new elements to the array and doubles the capacity of the array if it cannot fit
        """
        #Normal append
        if self.size < self.capacity:
            self.data[self.size] =  value
            self.size = self.size + 1
        #Creates new array with double the capacity
        else:
            newArr = StaticArray(self.capacity * 2)
            #Sets the new array to contain the data of the original
            for i in range(self.size):
                newArr[i] = self.data[i]
          
            self.data = newArr
            self.capacity = self.capacity * 2
            #Continues with the normal append
            self.data[self.size] =  value
            self.size = self.size + 1

    
    def pop_front(self) -> object:
        """
        Removes and returns the first value in the array
        """
        holder = self.data[0]
        self.remove_at_index(0)
        return holder

    def pop_back(self) -> object:
        """
        Removes and returns the last value in the array
        """
        holder = self.data[self.size - 1]
        self.remove_at_index(self.size - 1)
        return holder

    def push(self, value) -> None:
        """
        Inserts a value at the front of the array and pushes the others back
        """
        self.insert_at_index(0, value)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Implements a function that allows you to insert an element at a specific index
        """
        #Checks to make sure the index is within the valid indices
        if index < 0 or index > self.size:
            raise DynamicArrayException
        #Increases the capacity of the array if needed
        if self.size == self.capacity:
            self.resize(self.capacity * 2)
        #Steps through the array backwards pushing what is in and in front of the desired index up one
        for i in range(self.size - 1, index - 1, -1):
            self.data[i + 1] = self.data[i]
        #Sets the desired value to the desired index
        self.data[index] = value
        self.size = self.size + 1


    def remove_at_index(self, index: int) -> None:
        """
        Implements a function that removes an element at a specific index and moves the remaining elements down to fill the space
        """
        #Checks to make sure the index is within the valid indices
        if index < 0 or index >= self.size:
            raise DynamicArrayException
        if self.capacity < 10:
            pass
        #Reduces the capacity of the array to double the size unless the capacity would become < 10
        elif self.size < self.capacity / 4 and self.capacity != 10:
            self.resize(self.size * 2)
            if self.capacity < 10:
                self.resize(10)
        #Checks to see if the desired index is the last element for easy deletion
        if index == self.size - 1:
            self.data[index] = None
            self.size = self.size - 1
        #Moves anything in front of the desired index back one
        else:
            for i in range(index, self.size - 1):
                self.data[i] = self.data[i + 1]                      
            
            self.size = self.size - 1

    def slice(self, start_index: int, size: int) -> object:
        """
        Implements a function that takes a slice of an array and returns that desired portion
        """
        #Checks to make sure both start_index and size are both valid
        if start_index < 0 or start_index >= self.size or size < 0 or size > self.size or size > self.size - start_index:
            raise DynamicArrayException
        #Creates a new array and appends the elements from the starting index to the length of the size
        slicedArr = DynamicArray()
        for i in range(start_index, start_index + size):
            slicedArr.append(self.data[i])

        return slicedArr

    def merge(self, second_da: object) -> None:
        """
        Function that combines two arrays
        """
        #Appends the second array onto the first
        for i in range(second_da.size):
            self.append(second_da.data[i])
        

    def map(self, map_func) -> object:
        """
        Implements a function that iterates through an array an applies the passed map function to each element
        """
        newArr = DynamicArray()
        #Iterates through the array and passes each element to the map function
        for i in range(self.size):
            math = map_func(self.data[i])
            newArr.append(math)
        return newArr
    
    
    def filter(self, filter_func) -> object:
        """
        Implements a function that creates a new array with the values that were received from the filter function
        """
        filteredArr = DynamicArray()
        #Iterates through the array and checks whether or not it is true with the filter function
        for i in range(self.size):
            if filter_func(self.data[i]) == True:
                filteredArr.append(self.data[i])
        return filteredArr

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Implements a function that performs a reduction on each element in an array based on the passed reduce_func
        """
        reducedArr = DynamicArray()
        reducedArr.size = reducedArr.size + 1
        #Checks for an initializer parameter
        if initializer == None:
            initializer = self.data[0]
            reducedArr[0] = self.data[0]
            #Performs the desired reduce of the reduce_func and sums it into a new array element
            for i in range(self.size - 1):
                reducedArr.data[0] = reduce_func(reducedArr.data[0], self.data[i + 1])
            return reducedArr[0]
        else:
            reducedArr[0] = initializer
            
            for j in range(self.size):
                reducedArr.data[0] = reduce_func(reducedArr.data[0], self.data[j])
            return reducedArr[0]
    
    

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()
    print(da.size, da.capacity, da.data)
    da.resize(8)
    print(da.size, da.capacity, da.data)
    da.resize(2)
    print(da.size, da.capacity, da.data)
    da.resize(0)
    print(da.size, da.capacity, da.data)


    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)


    print("\n# append - example 1")
    da = DynamicArray()
    print(da.size, da.capacity, da.data)
    da.append(1)
    print(da.size, da.capacity, da.data)
    print(da)


    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)


    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.size)
    print(da.capacity)


    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)


    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)


    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)


    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)


    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.size, da.capacity)
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)


    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.size, da.capacity)
    [da.append(1) for i in range(100)]          # step 1 - add 100 elements
    print(da.size, da.capacity)
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.size, da.capacity)
    da.remove_at_index(0)                       # step 3 - remove 1 element
    print(da.size, da.capacity)
    da.remove_at_index(0)                       # step 4 - remove 1 element
    print(da.size, da.capacity)
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.size, da.capacity)
    da.remove_at_index(0)                       # step 6 - remove 1 element
    print(da.size, da.capacity)
    da.remove_at_index(0)                       # step 7 - remove 1 element
    print(da.size, da.capacity)

    for i in range(14):
        print("Before remove_at_index(): ", da.size, da.capacity, end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.size, da.capacity)


    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)


    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")


    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)


    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)


    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))


    print("\n# map example 2")
    def double(value):
        return value * 2

    def square(value):
        return value ** 2

    def cube(value):
        return value ** 3

    def plus_one(value):
        return value + 1

    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))


    print("\n# filter example 1")
    def filter_a(e):
        return e > 10

    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))


    print("\n# filter example 2")
    def is_long_word(word, length):
        return len(word) > length

    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))


    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 4, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot", "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    print("\nPUSH TEST")
    da = DynamicArray()
    for i in range(9):
        da.push(i)
        print(da)
