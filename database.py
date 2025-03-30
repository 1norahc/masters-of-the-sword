import json
import os

class Database:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump({}, file)

    def load_data(self):
        with open(self.filename, 'r') as file:
            return json.load(file)

    def save_data(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def update_data(self, key, value):
        data = self.load_data()
        data[key] = value  # Nadpisuje istniejący wpis lub dodaje nowy
        self.save_data(data)

    def get_data(self, key):
        return self.load_data().get(key, None)
