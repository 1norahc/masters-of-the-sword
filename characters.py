

import json
import os


# Klasy postaci
class Classes:
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

# Początkowe statystyki max. 20 pkt + 10 do allocate
CLASS = {
    "Warrior": Classes("Warrior", 12, 5, 3, 0, 100),
    "Archer" : Classes("Archer", 5, 10, 5, 0, 100),
    "Mage": Classes("Mage", 3, 5, 12, 0, 100)
}

def allocate_stats(character):
    print("====================")
    points_to_allocate = 10
    print(f"You can allocate additional {points_to_allocate} points to your statistics: ")

    str_points = int(input("Add Strength: "))
    agi_points = int(input("Add Agility: "))
    int_points = int(input("Add Intelligence: "))
    while True:
        total_points = str_points + agi_points + int_points
        if total_points == points_to_allocate:
            character.strength += str_points
            character.agility += agi_points
            character.intelligence += int_points
            break
        else:
            print(f"Total points must be equal to {points_to_allocate}!")

    print("====================")
    print("Your updated stats: ")
    character.stats()

# TODO: Wpada w loopa jak źle wpiszemy dane tj: np za dużą ilość punktów XDDDD

# Początkowe itemy do wybrania
class Items:
    def __init__(self, name, strength, agility, intelligence, armor, hp):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.armor = armor
        self.hp = hp


ITEMS = {
    "Plate Armor": Items("Plate Armor", 5, 0, 0, 30, 100),
    "Leather Armor": Items("Leather Armor", 0, 5, 0, 20, 75),
    "Robe": Items("Robe", 0, 0, 5, 10, 50)
}


def choose_item(character):
    print("====================")
    print(f"You can choose 1 item from the following: {list(ITEMS.keys())}")
    chosen_item = input("Choose an item: ")
    while True:
        if chosen_item in ITEMS:
            selected_item = ITEMS[chosen_item]
            character.strength += selected_item.strength
            character.agility += selected_item.agility
            character.intelligence += selected_item.intelligence
            character.armor += selected_item.armor
            character.hp += selected_item.hp
            print(f"You've chosen {selected_item.name}.")
            print(f"Your stats have been updated!")
            character.stats()
            break
        else:
            print(f"Choose an item from the following: {list(ITEMS.keys())}")

# Tworzenie postaci
def create_character():
    name = input("Enter your name: ")
    print("There are 3 classes avialable: Warrior, Archer and Mage")

# Wybieranie klasy z loopem - musi być poprawna klasa
    while True:
        class_name = input("Choose your class: ")
        if class_name in CLASS:
            print("====================")
            print("You've chosen to be the " + "* " + class_name + " *.")
            print("====================")
            break
# Jeśli podana klasa jest zła
        else:
            print("That class is not available, please choose either Warrior, Archer or Mage")

# # Wyświetlenie statystyk
#     print("Your starting statistics:")
#     character = CLASS[class_name]
#     character.stats()
#
# # Dodawanie statystyk
#     allocate_stats(character)
#
# # Wybieranie itemów
#     choose_item(character)
#
# player = create_character()
#



class Character:
    def __init__(self, email, character_class, stats, items):
        self.email = email
        self.character_class = character_class
        self.stats = stats
        self.items = items

    def add_item(self):
        pass

    def save_to_json(self, file_name="DB/characters.json"):

        player_data = {
            "email": self.email,
            "character_class": self.character_class,
            "stats": self.stats,
            "items": self.items
        }
        if os.path.exists(file_name):
            with open(file_name, "r+") as f:
                data = json.load(f)
        else:
            data = []


x = Character(
    Classes("Warrior", 12, 5, 3, 0, 100),
    Items("Plate Armor", 5, 0, 0, 30, 100)
)




