import random

print("Welcome to Higher & Lower, a game where you have 5 attempts to guess the correct number.")
print("When you forgot your previous attempts you can guess -1 which does not count as")
print("a guess but will print your previous guesses!")

max_number = int(input("Choose the guessing range starting from 1 to : "))
print()
secret_number = random.randint(1, max_number)

counter = 0
guesses = []
attempts = 5
points_table = [10, 8, 5, 2, 1]
is_won = False

while counter < attempts:
    guess = int(input(f"Guess a number between 1 and {max_number}: "))
    print()

    if guess == -1:
        print(f"your previous guesses are: {"".join(str(x) for x in guesses)}")
        continue

    guesses.append(guess)

    if guess == secret_number:
        print("You have tried to following numbers: ")
        print(f"{" ".join(str(x) for x in guesses)} to guess the secret number {secret_number}!")
        print(f"You won and are awarded {points_table[counter]} points!")
        is_won = True
        break
    elif guess < secret_number:
        print(f"{guess} is incorrect, the number is higher.")
    else:
        print(f"{guess} is incorrect, the number is lower.")

    counter += 1

if not is_won:
    print("You have tried to following numbers: ")
    print(f"{" ".join(str(x) for x in guesses)} to guess the secret number {secret_number}!")
    print("You lost :(")
