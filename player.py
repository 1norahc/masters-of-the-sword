

"""
Player <- Characters <- Items

"""


import json
import os


class Character:
    def __init__(self, email, character_class, stats, items):
        """
        :param email:
        :param character_class:
        :param stats:
        :param items: Wczytanie aktualnego stanu itemów z "bazy danych"

        """
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

        # Upewnij się, że katalog istnieje
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        data = []
        if os.path.exists(file_name):
            try:
                with open(file_name, "r") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass  # Plik pusty lub uszkodzony, zostawiamy pustą listę

        data.append(player_data)

        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)


# Poprawione dane wejściowe
c = Character(
    "test@gmail.com", "warrior", {"strength": 2}, ["Zbroja"]
)

c.save_to_json()
