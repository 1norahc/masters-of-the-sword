import random

class Player:
    """
    TODO: Stworzyć klasy:
    - Items -> klasa która będzie tworzyć obiekt Item, który będzie zapisywany później w bazie ze swoim ID
    - Stats -> w której będą statystki gracza
    i przekazać je do tej klasy w formie np Player(Items, Stats)
    """

    # Zmienne stałe zrobione dla przykładu
    BASE_STATS = {
        "Warrior": {"Strength": 5, "Intelligence": 1, "Dexterity": 3, "Armor": 4},
        "Mage": {"Strength": 1, "Intelligence": 5, "Dexterity": 3, "Armor": 2},
        "Archer": {"Strength": 3, "Intelligence": 2, "Dexterity": 5, "Armor": 2}
    }

    ABILITIES = {
        "Warrior": ["Normal Attack", "Hard Attack"],
        "Mage": ["Fireball", "Staff Attack"],
        "Archer": ["Normal Shot", "Hard Shot"]
    }

    def __init__(self,
                 name: str,
                 character_class: str,
                 stat_points: dict,
                 items: list
                 ):
        """
        :param name: Nazwa postaci
        :param character_class: Klasa postaci
        :param stat_points: Statystki gracza
        :param items: Itemy gracza (na razie tworzę jako listę żeby operować na mniejszych danych, później doda się tu jakąś prostą bazę)
        """
        if character_class not in self.BASE_STATS:
            raise ValueError("Invalid class. Choose from: Warrior, Mage, Archer")

        self.name = name
        self.character_class = character_class
        self.stats = self.BASE_STATS[character_class].copy()
        self.items = items

    def __str__(self):
        return """ Klasa reprezentująca gracza. """

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Class: {self.character_class}")
        print(f"Stats: {self.stats}")
        print(f"Items: {self.items}")

    def attack(self):
        abilities = self.ABILITIES[self.character_class]
        return random.choice(abilities)


# Wywołanie
def test1():
    # Tworzenie postaci
    player1 = Player(
        name="DragonSlayer69",
        character_class="Warrior",
        stat_points={"Strength": 4, "Intelligence": 0, "Dexterity": 3, "Armor": 3},
        items=[{"name": "Iron Helmet", "stats": {"Armor": 2}}, {"name": "Sword", "stats": {"Strength": 3}}]
    )

    # Wyświetlenie informacji o postaci
    player1.display_info()

    # Wykonanie ataku
    attack_used = player1.attack()
    print(f"\n{player1.name} używa ataku: {attack_used}")

test1()