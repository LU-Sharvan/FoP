"""
File: pokemon.py
Author: Sharvan Gangadin
Description: Mini Pokémon Game where you can play simulated matches based on your pokemons level
License: LU License
"""

# Classes

class Pokemon:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.moves = set()  # Empty set to be filled later

    def __repr__(self):
        return f"{self.name} (Level: {self.level} | Moves: {self.moves})"

class Trainer:
    def __init__(self, name, pokemons):
        self.name = name
        self.pokemons = pokemons  # List

    def __repr__(self):
        return f"{self.name} pokemons: {self.pokemons}"

# Functions

def add_pokemon(pokemon_mapping, name, pokemon_ID, level):
    if pokemon_ID in pokemon_mapping:
        print("Error: Pokemon ID 1 already exists!")
        return pokemon_mapping  # Prevents duplicate Pokémon ID
    pokemon_mapping[pokemon_ID] = Pokemon(name, level)  # Places Pokemon(name, level) at unique index Pokemon_ID
    return pokemon_mapping  # Returns updated pokemon_mapping

def add_move(pokemon_mapping, unique_moves, pokemon_ID, move):
    if pokemon_ID not in pokemon_mapping:
        print("Error: Pokemon ID 2 not found!")
        return unique_moves  # Prevents adding move to a non-existent Pokémon
    unique_moves.add(move)
    pokemon_mapping[pokemon_ID].moves.add(move)  # Pokemon.moves gets accessed
    return unique_moves  # Return updated list of unique global moves

def add_trainer(trainer_mapping, trainer_name, trainer_ID, pokemon_mapping, pokemons_ID):
    if trainer_ID in trainer_mapping:
        print("Error: Trainer ID 3 already exists!")
        return trainer_mapping  # Prevents duplicate trainer ID

    # Prints Error if pokemon ID doesn't exist, otherwise it adds it to the list of owned Pokemon
    pokemons = []
    for ID in pokemons_ID:
        if ID not in pokemon_mapping:
            print("Error ID 5 not found!")
            return pokemons
        pokemons.append(pokemon_mapping[ID])

    trainer_mapping[trainer_ID] = Trainer(trainer_name, pokemons)  # Store var of type Trainer in trainer_mapping
    return trainer_mapping

def strongest_pokemon(pokemon_mapping):
    highest_level = -1  # Sets a starting value such that every possible pokemon level is above it
    strongest_pokemon = None  # Later gets replaced by the ID of the strognest

    if not pokemon_mapping:
        return None

    # Loops through each ID and assings the Pokemon with the highest level to highest_level and strongest_pokemon
    for ID in pokemon_mapping:
        if pokemon_mapping[ID].level > highest_level:
            highest_level = pokemon_mapping[ID].level
            strongest_pokemon = ID
    return pokemon_mapping[strongest_pokemon]

def battle(trainer_1, trainer_2):
    t1_points = 0
    t2_points = 0

    # Points system
    for t1_pokemon, t2_pokemon in zip(trainer_1.pokemons, trainer_2.pokemons):  # Matches based on tuples made by zip
        if t1_pokemon.level > t2_pokemon.level:
            t1_points += 1
        elif t1_pokemon.level < t2_pokemon.level:
            t2_points += 1
        else:
            t2_points += 1

    # Determining the winner based on obtained points
    if t1_points > t2_points:
        return print(f"{trainer_1.name} won the battle!")
    elif t1_points < t2_points:
        return print(f"{trainer_2.name} won the battle!")
    else:
        return print(f"{trainer_1.name} won the battle!")

# Main script
if __name__ == "__main__":
    print("Framework Pokemon Game:")

    # Data structures
    pokemon_mapping = {}  # Pokemon ID : Pokemon("Name", level)
    trainer_mapping = {}  # Trainer ID : Trainer("Name", pokemons)
    unique_moves = set()

    # Adding Pokemon
    add_pokemon(pokemon_mapping, "Baxcalibur", 998, 100)
    add_pokemon(pokemon_mapping, "Totodile", 158, 15)
    add_pokemon(pokemon_mapping, "Scream Tail", 985, 94)

    # Adding moves to Pokemon
    add_move(pokemon_mapping, unique_moves, 998, "Dragon Rush")
    add_move(pokemon_mapping, unique_moves, 158, "Water Gun")
    add_move(pokemon_mapping, unique_moves, 985, "Disarming Voice")
    add_move(pokemon_mapping, unique_moves, 998, "Glaive Rush")

    # Adding trainers
    add_trainer(trainer_mapping, "Ash", 5, pokemon_mapping, [158])
    add_trainer(trainer_mapping, "Gladeon", 101, pokemon_mapping, [998])

    # Printing list of all unique moves and strongest Pokemon
    print(unique_moves)
    print(strongest_pokemon(pokemon_mapping))

    # Simulating battle between Ash and Gladeon
    print(battle(trainer_mapping[5], trainer_mapping[101]))
