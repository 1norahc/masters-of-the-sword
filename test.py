import json
import os


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

        data.append(player_data)

        with open(file_name, "w") as file:
            json.dump(data, file)

c = Character(
    "test@gmail.com", "warrior", "2", "Zbroja"
)

c.save_to_json()