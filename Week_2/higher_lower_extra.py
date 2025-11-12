"""
File: higher_lower_extra.py
Author: Sharvan Gangadin
Description: Higher & Lower game: multiple rounds of guesssing the secret number in 5 attempts
License: LU license
"""

import random  # Import random to generate secret number

# Game introduction
print("Welcome to Higher & Lower, a game where you have 5 attempts to guess the correct number.")
print("When you forgot your previous attempts you can guess -1 which does not count as")
print("a guess but will print your previous guesses!")

# Game setup
max_number = int(input("Choose the guessing range starting from 1 to : "))
played_rounds = 0  # Number of played rounds
scores_per_round = []  # Scores of each round
points_table = [10, 8, 5, 2, 1]  # Points per attempt for each index

# Main game loop (multiple rounds)
while True:
    secret_number = random.randint(1, max_number)  # Secret number generation for all rounds
    counter = 0  # Attempt counter for each round
    guesses = []  # Guesses for each round
    attempts = 5  # Attempts per round
    is_won = False  # Tracks if the player won in the current round

    # Question loop
    while counter < attempts:
        guess = int(input(f"Guess a number between 1 and {max_number}: "))
        print()

        # History check
        if guess == -1:
            print(f"your previous guess(es) are: {"".join(str(x) for x in guesses)}")
            continue

        guesses.append(guess)  # Add guess to list of attempts

        # Win check
        if guess == secret_number:
            print("You have tried to following numbers: ")
            print(f"{" ".join(str(x) for x in guesses)} to guess the secret number {secret_number}!")
            print(f"You won and are awarded {points_table[counter]} points!")
            scores_per_round.append(points_table[counter])
            is_won = True
            break
        elif guess < secret_number:
            print(f"{guess} is incorrect, the number is higher.")  # Hint 1
        else:
            print(f"{guess} is incorrect, the number is lower.")  # Hint 2

        counter += 1  # Move to the next attempt

    # Lost screen
    if not is_won:
        print("You have tried to following numbers: ")
        print(f"{" ".join(str(x) for x in guesses)} to guess the secret number {secret_number}!")
        print("You lost :(")
        scores_per_round.append(0)

    played_rounds += 1  # Tracks amount of played rounds

    # Asks user for another round
    new_round = input("Do you want to play again? (y/n) ")
    if new_round.strip().lower() not in ("y", "yes"):  # If input is not yes, the game loop breaks
        break

# Final results output
obtained_score = sum(scores_per_round)  # Total score obtained
max_score = played_rounds * 10  # Max possible score
print(f"You played {played_rounds} rounds, where you recieved {obtained_score}/{max_score} points")
print(f"You scored per round: {scores_per_round}")
