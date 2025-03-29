import random

class Enemy:
    def __init__(self, name, strength, agility, intelligence, armor, hp):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.armor = armor
        self.hp = hp

    def stats(self):
        print(f"Strength: {self.strength}")
        print(f"Agility: {self.agility}")
        print(f"Intelligence: {self.intelligence}")
        print(f"Armor: {self.armor}")
        print(f"HP: {self.hp}")

ENEMIES = {
    "Goblin": Enemy("Goblin", 3, 5,0,5,50),
    "Orc": Enemy("Orc", 12,5,6,25, 150),
    "Bandit": Enemy("Bandit", 6, 12, 6, 10,100)
}
