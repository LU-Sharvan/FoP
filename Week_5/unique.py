"""
File: unique.py
Author: Sharvan Gangadin
Description: Creating copy of a list where every zero gets replaced by an increasing non-zero value
"""

def fill_unique(list, new_list=None):
   
    # Base Case: the new list is empty; supposed to be the first iteration
    if new_list is None:
        new_list = [] 

    # Base Case: the new list is just as large as the original
    if len(new_list) == len(list):
        return new_list

    # Determines position where to start replacing zero's
    index = len(new_list)
    current = list[index]

    # Recursive function: add the first looked at element of the list to the new list
    if current == 0:
        replacement = 1
        while replacement in list[index + 1:] or replacement in new_list:
            replacement += 1  # If the non-zero value increases by 1 if it's already in the remainder or in the new list
        return fill_unique(list, new_list + [replacement])  # Remainder is evaluated, replacement added to new list

    # If the position is a non-zero value
    return fill_unique(list, new_list + [current])

print(fill_unique([1, 1, 1, 0, 1, 0, 1, 0]))
