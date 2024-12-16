import random
import time
import math

def create_random_list(length, min_value, max_value):
    if length < 0:
        raise ValueError("Length must be a non-negative integer.")
    
    random_list = [random.randint(min_value, max_value) for _ in range(length)]
    return random_list



def bubble_sort(v1):
    not_done = True
    while not_done:
        not_done = False
        for i in range(len(v1) - 1):
            if v1[i] > v1[i+1]:
                v1[i], v1[i+1] = v1[i+1], v1[i]
                not_done = True
    return v1


def get_smallest_element(list):
    small = math.inf
    for elem in list:
        if elem < small:
            small = elem
    return small

def selection_sort(to_sort):
    sorted = []
    for _ in range(len(to_sort)):
        small = get_smallest_element(to_sort)
        to_sort.remove(small)
        sorted.append(small)
    return sorted

""" start_selection = time.time()

v = create_random_list(100000, -1000, 100)
selection_sort(v)
end_selection = time.time()


start_bubble = time.time()
v = create_random_list(100000, -1000, 100)
bubble_sort(v)
end_bubble = time.time()

bubble_time = end_bubble - start_bubble
selection_time = end_selection - start_selection
print(f"The selection sorting took {selection_time} seconds")
print(f"The bubble sorting took {bubble_time} seconds")

if bubble_time > selection_time:
    print("Bubble sorting took the longest")
else:
    print("Selection sorting took the longest") """

print(math.inf)