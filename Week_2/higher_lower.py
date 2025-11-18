"""
File: higher_lower.py
Author: Sharvan Gangadin
Decription: Higher & Lower game: guess the secret number in 5 attempts
License: LU license
"""

import random  # Import random to generate secret number

# Game introduction
print("Welcome to Higher & Lower, a game where you have 5 attempts to guess the correct number.")
print("When you forgot your previous attempts you can guess -1 which does not count as")
print("a guess but will print your previous guesses!")

# Game setup
max_number = int(input("Choose the guessing range starting from 1 to : "))
print()
secret_number = random.randint(1, max_number)  # Generates secret number in range 1 to max_number

# Intializing variables for game
counter = 0  # Number of guesses made
guesses = []  # List of previous guesses
attempts = 5  # Number of allowed attempts
points_table = [10, 8, 5, 2, 1]  # Points per attempt for each index
is_won = False  # Tracker for win condition

# Main game loop
while counter < attempts:
    guess = int(input(f"Guess a number between 1 and {max_number}: "))
    print()

    # History check
    if guess == -1:
        print(f"your previous guesses are: {"".join(str(x) for x in guesses)}")
        continue  # Skip the rest of the loop

    guesses.append(guess)  # Store the new guess in the list

    # Win check
    if guess == secret_number:
        print("You have tried to following numbers: ")
        print(f"{" ".join(str(x) for x in guesses)} to guess the secret number {secret_number}!")
        print(f"You won and are awarded {points_table[counter]} points!")
        is_won = True
        break  # Stops loop when number is guessed
    elif guess < secret_number:  # Hint if number is higer
        print(f"{guess} is incorrect, the number is higher.")
    else:  # Hint if number is lower
        print(f"{guess} is incorrect, the number is lower.")

    counter += 1  # Move to next attepmt

# Lost screen
if not is_won:
    print("You have tried to following numbers: ")
    print(f"{" ".join(str(x) for x in guesses)} to guess the secret number {secret_number}!")
    print("You lost :(")
