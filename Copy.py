def fill_unique(list, new_list=None):
    # Initializing list
    if new_list is None:
        new_list = []
   
    # Base case
    if len(list) == 0:
        return new_list

    # Checks if the current iteration of the list starts with 0
    if list[0] == 0:
        replacer = 1

        # For every time the replacer is in the list or new list, the value increases by 1
        while replacer in list[1:] or replacer in new_list:
            replacer += 1
        return fill_unique(list[1:], new_list + [replacer])  # Next iteration with replacement added to the new list
   
    # If the list doesn't start with 0, the next iteration will have the non-zero value in the new list
    else:
        return fill_unique(list[1:], new_list + [list[0]])

# Creating list and applying function onto it
list = [0, 1, 0, 1]
print(fill_unique(list))
