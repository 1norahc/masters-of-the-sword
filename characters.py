# Klasy postaci
class characterClasses:
    def __init__(self, name, strength, agility, intelligence):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence

    def stats(self):
        print(f"Strength: {self.strength}")
        print(f"Agility: {self.agility}")
        print(f"Intelligence: {self.intelligence}")

# Początkowe statystyki max. 20 pkt + 10 do allocate
CLASS = {
    "Warrior": characterClasses("Warrior", 12, 5, 3),
    "Archer" : characterClasses("Archer", 5, 10, 5),
    "Mage": characterClasses("Mage", 3,5,12)
}

def allocate_stats(character):
    points_to_allocate = 10
    print(f"You got {points_to_allocate} to allocate")

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

# TODO: Wpada w loopa jak źle wpiszemy dane tj: np za dużą ilość punktów XDDDD


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

# Wyświetlenie statystyk
    print("Your starting statistics:")
    character = CLASS[class_name]
    character.stats()

# Dodawanie statystyk
    print("====================")
    print("You can allocate additional 10 points to your statistics: ")
    allocate_stats(character)

# Wyświetlanie nowych statystyk
    print("====================")
    print("Your updated stats: ")
    character.stats()


player = create_character()