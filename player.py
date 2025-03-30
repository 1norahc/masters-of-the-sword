import uuid
from database import Database


"""
TODO
====

ITEMKI:
* Mają wartość
* Wczytują się z klasy Items
* Pobierają dane o itemach z "bazy danych" items.json

KLASY POSTACI:
* zwracać zamiast "character_class": "Mage", np. 
    "character": {
        class : [<class name>],
        stats : [<statystyki>]
    }
!!!!! Statystyki muszą być podawane do bazy na podstawie poziomu
czyli jak Gracz ma lvl 1 i wybierze kalse Warrior to jego statystyki mają podstawowe wartości dla klasy Warrior
* Jeżeli gracz zwiększy poziom to statystki muszą też wzrosnąć (czyli aktulaizowanie statystyk gracza)
* Dodać możliwość EXP czyli gracz musi mieć EXP żeby wbić kolejny poziom (dodać system expienia)



# Dodać przeciwników 
# Dodać automatyczny system walki

"""



class Player:
    """
    Klasa reprezentująca gracza w systemie.

    Atrybuty:
        username (str): Nazwa użytkownika.
        email (str): Email użytkownika.
        players_db (Database): Obiekt bazy danych graczy.
        characters_db (Characters): Obiekt bazy danych postaci.
        data (dict): Dane gracza z bazy danych.

    Metody:
        get_stats(): Zwraca informacje o graczu i jego postaciach.
        get_characters(): Zwraca listę postaci gracza.
        add_character(name, character_class): Dodaje postać do konta gracza, sprawdzając unikalność nazwy.
    """

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.players_db = Database("DB/players.json")
        self.characters_db = Characters()
        self.data = self.players_db.get_data(username)

        # ------------------------------------------
        # Jeśli gracz nie istnieje, utwórz nowego
        if self.data is None:
            self.data = {"email": email, "characters": []}
            self.players_db.update_data(username, self.data)
        # ------------------------------------------

    def get_stats(self):
        """
        Zwraca statystyki gracza, w tym informacje o postaciach.
        """
        return {
            "username": self.username,
            "email": self.email,
            "characters": [char.get_stats() for char in self.get_characters()]
        }

    def get_characters(self):
        """
        Zwraca listę postaci gracza.
        """
        return [self.characters_db.get_character(char_id) for char_id in self.data.get("characters", []) if
                self.characters_db.get_character(char_id)]

    # ----------------------------------------------------------------

    def add_character(self, name, character_class):
        """
        Dodaje nową postać do konta gracza, sprawdzając, czy nazwa jest unikalna.

        Args:
            name (str): Nazwa postaci.
            character_class (str): Klasa postaci.

        Returns:
            str: ID dodanej postaci.
        """
        if self.is_name_taken(name):
            raise ValueError(f"Character name '{name}' is already taken.")
        char_id = self.characters_db.add_character(name, character_class)
        self.data["characters"].append(char_id)
        self.players_db.update_data(self.username, self.data)
        return char_id

    # ----------------------------------------------------------

    def is_name_taken(self, name):
        """
        Sprawdza, czy nazwa postaci jest już używana przez tego gracza.

        Args:
            name (str): Nazwa postaci.

        Returns:
            bool: True jeśli nazwa jest już zajęta, False w przeciwnym razie.
        """
        for char in self.get_characters():
            if char.name == name:
                return True
        return False


class Character:
    """
    Klasa reprezentująca postać w grze.

    Atrybuty:
        id (str): Unikalny identyfikator postaci.
        name (str): Nazwa postaci.
        character_class (str): Klasa postaci.
        level (int): Poziom postaci.
        inventory (list): Lista przedmiotów w ekwipunku.
        gold (int): Ilość złota postaci.
        silver (int): Ilość srebra postaci.
        equipped (dict): Ekwipowane przedmioty w postaci (np. broń, hełm, rękawice).

    Metody:
        get_stats(): Zwraca informacje o postaci.
        equip_item(item_name): Wyposaża postać w przedmiot.
        sell_item(item_name, price): Sprzedaje przedmiot i dodaje uzyskaną walutę.
        add_currency(silver_amount): Dodaje srebro i konwertuje je na złoto.
        get_item_slot(item_name): Zwraca slot przedmiotu na podstawie jego nazwy.
    """
    BASE_INVENTORY_SIZE = 10  # Bazowy rozmiar ekwipunku
    EQUIPMENT_SLOTS = {"weapon": None, "helmet": None, "gloves": None, "belt": None, "special": None}

    def __init__(self, name, character_class, level=1, inventory=None, gold=0, silver=0, equipped=None, id=None):
        self.id = id if id else str(uuid.uuid4())  # Jeśli ID istnieje, użyj go, jeśli nie, wygeneruj nowe.
        self.name = name
        self.character_class = character_class
        self.level = level
        self.gold = gold
        self.silver = silver
        self.inventory = inventory if inventory else []
        self.equipped = equipped if equipped else self.EQUIPMENT_SLOTS.copy()

    def get_stats(self):
        """
        Zwraca statystyki postaci.
        """
        return {
            "id": self.id,
            "name": self.name,
            "class": self.character_class,
            "level": self.level,
            "gold": self.gold,
            "silver": self.silver,
            "inventory": self.inventory,
            "equipped": self.equipped,
            "inventory_size": self.get_max_inventory_size()
        }

    def get_max_inventory_size(self):
        """
        Zwraca maksymalny rozmiar ekwipunku, który rośnie co 5 poziomów.
        """
        return self.BASE_INVENTORY_SIZE + (self.level // 5)

    def equip_item(self, item_name):
        """
        Wyposaża postać w przedmiot, jeśli znajduje się w jej ekwipunku.
        """
        if item_name in self.inventory:
            item_slot = self.get_item_slot(item_name)
            if item_slot and item_slot in self.equipped:
                self.equipped[item_slot] = item_name
                self.inventory.remove(item_name)
                return f"Equipped {item_name} in {item_slot}."
        return "Cannot equip item."

    def sell_item(self, item_name, price):
        """
        Sprzedaje przedmiot i dodaje uzyskaną walutę.
        """
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            self.add_currency(price)
            return f"Sold {item_name} for {price} silver."
        return "Item not found."

    def add_currency(self, silver_amount):
        """
        Dodaje srebro do postaci, konwertując nadmiar na złoto.
        """
        total_silver = self.silver + silver_amount
        self.gold += total_silver // 100  # Każde 100 srebra to 1 złoto
        self.silver = total_silver % 100

    def get_item_slot(self, item_name):
        """
        Zwraca slot, w którym postać może wyposażyć dany przedmiot.
        """
        item_slots = {
            "Sword": "weapon",
            "Helmet": "helmet",
            "Gloves": "gloves",
            "Belt": "belt",
            "Amulet": "special",
            "Health Potion": "consumable"
        }
        return item_slots.get(item_name, None)


class Characters:
    """
    Klasa reprezentująca bazę danych postaci w grze.

    Atrybuty:
        db (Database): Baza danych postaci.

    Metody:
        add_character(name, character_class): Dodaje nową postać do bazy danych.
        get_character(char_id): Pobiera postać z bazy danych.
    """

    def __init__(self):
        self.db = Database("DB/characters.json")

    def add_character(self, name, character_class, level=1, inventory=None, gold=0, silver=0, equipped=None):
        """
        Dodaje postać do bazy danych.
        """
        character = Character(name, character_class, level, inventory, gold, silver, equipped)
        self.db.update_data(character.id, character.__dict__)
        return character.id  # Zwraca ID dodanej postaci

    def get_character(self, char_id):
        """
        Pobiera postać z bazy danych po ID.
        """
        data = self.db.get_data(char_id)
        if data:
            return Character(**data)
        return None


class User:
    """
    Klasa reprezentująca użytkownika w systemie.

    Atrybuty:
        player (Player): Obiekt reprezentujący gracza.

    Metody:
        get_user_info(): Zwraca informacje o graczu i jego postaciach.
        create_character(name, character_class): Tworzy nową postać dla użytkownika.
    """

    def __init__(self, username, email):
        self.player = Player(username, email)

    def get_user_info(self):
        """
        Zwraca informacje o graczu.
        """
        return self.player.get_stats()

    def create_character(self, name, character_class):
        """
        Tworzy nową postać dla gracza.
        """
        return self.player.add_character(name, character_class)


# # Przykładowe użycie
# if __name__ == "__main__":
#     user = User("Arthas", "arthas@example.com")
#     print(user.get_user_info())
#
#     # Tworzenie nowej postaci
#     char_id = user.create_character("Gandalf", "Mage")
#     print(f"Created character with ID: {char_id}")
#     print(user.get_user_info())

import unittest

class TestPlayer(unittest.TestCase):

    def setUp(self):
        """
        Inicjalizacja przed każdym testem. Tworzymy testowego gracza.
        """
        self.user = User("TestUser", "testuser@example.com")

    def test_create_character_unique_name(self):
        """
        Test sprawdzający, czy nie można utworzyć postaci o tej samej nazwie.
        """
        self.user.create_character("Gandalf", "Mage")
        with self.assertRaises(ValueError):
            self.user.create_character("Gandalf", "Warrior")  # Nazwa już istnieje

    def test_get_user_info(self):
        """
        Test sprawdzający poprawność zwróconych informacji o graczu.
        """
        self.assertEqual(self.user.get_user_info()["username"], "TestUser")
        self.assertEqual(self.user.get_user_info()["email"], "testuser@example.com")

    def test_add_character(self):
        """
        Test dodawania postaci do gracza.
        """
        char_id = self.user.create_character("Aragorn", "Warrior")
        self.assertIsNotNone(char_id)
        self.assertEqual(len(self.user.get_user_info()["characters"]), 1)


if __name__ == "__main__":
    unittest.main()

