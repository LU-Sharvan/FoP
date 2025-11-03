import random

print("Welcome to Higher & Lower, a game where you have 5 attempts to guess the correct number.")
print("When you forgot your previous attempts you can guess -1 which does not count as")
print("a guess but will print your previous guesses!")

max_number = int(input("Choose the guessing range starting from 1 to : "))
played_rounds = 0
scores_per_round = []
points_table = [10, 8, 5, 2, 1]

while True:
    secret_number = random.randint(1, max_number)
    counter = 0
    guesses = []
    attempts = 5
    is_won = False

    while counter < attempts:
        guess = int(input(f"Guess a number between 1 and {max_number}: "))
        print()

        if guess == -1:
            print(f"your previous guess(es) are: {"".join(str(x) for x in guesses)}")
            continue

        guesses.append(guess)

        if guess == secret_number:
            print("You have tried to following numbers: ")
            print(f"{" ".join(str(x) for x in guesses)} to guess the secret number {secret_number}!")
            print(f"You won and are awarded {points_table[counter]} points!")
            scores_per_round.append(points_table[counter])
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
        scores_per_round.append(0)

    played_rounds += 1

    new_round = input("Do you want to play again? (y/n) ")
    if new_round.strip().lower() not in ("y", "yes"):
        break

obtained_score = sum(scores_per_round)
max_score = played_rounds * 10

print(f"You played {played_rounds} rounds, where you recieved {obtained_score}/{max_score} points")
print(f"You scored per round: {scores_per_round}")
