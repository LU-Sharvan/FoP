import random

given_number = random.randint(256, 1024)

print("The given number is", given_number)

number = int(input("Input your number: \n"))
same = number == given_number
size = number < given_number
zero_plus = (number > 0) and (given_number > 0)
memory_object = id(number) == id(given_number)


print("The input is the same as the given number is ", same)
print("The input is smaller compared to the given number is ", size)
print("The input and the given number are both not zero ", zero_plus)
print("The input is the same memory object as the given number is ", memory_object)
