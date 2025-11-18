"""
File: shooter.py
Author: Sharvan Gangadin
Description: Mini Shooter Game: Player takes on pre-set enemies in a life or death duel
License: LU License
"""

# Classes

class Enemy:
    enemies = []

    def __init__(self, hitpoints, damage):
        self.hitpoints = hitpoints
        self.damage = damage
        Enemy.enemies.append(self)

    def __repr__(self):
        return f"Enemy(hitpoints = {self.hitpoints}, damage = {self.damage})"

    def take_hit(self, damage):
        self.hitpoints -= damage
        if self.hitpoints <= fatal and self in Enemy.enemies:  # Checks whether enemy is in the list and if HP =< 0
            Enemy.enemies.remove(self)

    def shoot(self, player):
        return player.take_hit(self.damage)  # Player gets hit when enemy shoots

class Player:
    def __init__(self, hitpoints, damage, nth_shot=None):
        self.hitpoints = hitpoints
        self.damage = damage

        # Intializes only when nth_shot is passed
        if nth_shot is not None:
            self.nth_shot = nth_shot
            self.shots_fired = 0

    def __repr__(self):
        return f"Player(hitpoints = {self.hitpoints}, damage = {self.damage})"

    def take_hit(self, damage):
        self.hitpoints -= damage
        return self.hitpoints <= fatal  # Boolean returns True or False

    def shoot_5_times(self):
        for _ in range(5):
            if not Enemy.enemies:  # If the list of enemies is empty, the loop stops
                break
            damage_to_deal = self.damage  # Normal damage in every loop
            
            # If nth_value is passed in Player, the amount of fired shots goes up for every loop
            if "nth_shot" in vars(self):
                self.shots_fired += 1

                # When the amount of fired shots is divisible by the nth shot (eg 3th, 6th, 9th), the damage is doubled
                if self.shots_fired % self.nth_shot == 0:
                    damage_to_deal = self.damage * 2
            
            # Target is set for the oldest enemy who gets hit with either normal or double damage
            target = Enemy.enemies[0]
            target.take_hit(damage_to_deal)

        return not Enemy.enemies

# Functions

def duel(player):
    while player.hitpoints >= fatal:  # Loop runs as long as player has HP >= 0
        player.shoot_5_times()  # The player shoots first

        # Checks Falsy condition if there are any enemies left
        if not Enemy.enemies:
            return print("The player won!")

        # Loops through enemies to let them shoot
        for enemy in list(Enemy.enemies):
            neutralized = enemy.shoot(player)  # Boolean operator

            # If player has HP <0, the enemies have won
            if neutralized:
                return print("The enemies won!")

# Main code
fatal = 0

if __name__ == "__main__":

    # Creating enemies and players
    player = Player(100, 60, 1)
    enemy1 = Enemy(30, 30)
    enemy2 = Enemy(40000, 1)

    duel(player)  # Initiate duel

    # Print final stats of player and enemies
    print(player)
    print(Enemy.enemies)
