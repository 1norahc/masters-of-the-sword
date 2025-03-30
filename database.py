import json
import os


class Database:
    """
    Klasa Database reprezentuje prostą bazę danych opartą na pliku JSON.
    Umożliwia przechowywanie, wczytywanie, aktualizowanie i pobieranie danych
    w formacie klucz-wartość zapisanym w pliku JSON.
    """

    def __init__(self, filename):
        """
        Inicjalizuje obiekt bazy danych z podaną nazwą pliku.

        Args:
            filename (str): Nazwa pliku JSON, w którym przechowywane są dane.

        Jeśli plik nie istnieje, tworzy nowy plik z pustym słownikiem jako zawartością.
        """
        self.filename = filename  # Przechowuje nazwę pliku jako atrybut instancji
        if not os.path.exists(self.filename):
            # Tworzy nowy plik JSON z pustym słownikiem, jeśli nie istnieje
            with open(self.filename, 'w') as file:
                json.dump({}, file)

    def load_data(self):
        """
        Wczytuje dane z pliku JSON.

        Returns:
            dict: Słownik zawierający dane wczytane z pliku JSON.
        """
        with open(self.filename, 'r') as file:
            # Deserializuje zawartość pliku JSON do słownika Pythona
            return json.load(file)

    def save_data(self, data):
        """
        Zapisuje dane do pliku JSON, nadpisując jego dotychczasową zawartość.

        Args:
            data (dict): Słownik danych do zapisania w pliku JSON.
        """
        with open(self.filename, 'w') as file:
            # Serializuje dane do formatu JSON z wcięciami dla czytelności
            json.dump(data, file, indent=4)

    def update_data(self, key, value):
        """
        Aktualizuje dane w bazie, nadpisując istniejący klucz lub dodając nowy.

        Args:
            key (str): Klucz, pod którym zapisana zostanie wartość.
            value: Wartość do zapisania pod podanym kluczem.
        """
        data = self.load_data()  # Wczytuje aktualne dane z pliku
        data[key] = value  # Nadpisuje istniejący klucz lub dodaje nowy
        self.save_data(data)  # Zapisuje zaktualizowane dane z powrotem do pliku

    def get_data(self, key):
        """
        Pobiera wartość powiązaną z podanym kluczem.

        Args:
            key (str): Klucz, którego wartość ma zostać zwrócona.

        Returns:
            Wartość powiązana z kluczem lub None, jeśli klucz nie istnieje.
        """
        # Wczytuje dane i zwraca wartość dla klucza lub None, jeśli nie znaleziono
        return self.load_data().get(key, None)


# Przykład użycia (opcjonalny, dla demonstracji)
if __name__ == "__main__":
    # Tworzy instancję bazy danych z plikiem 'example.json'
    db = Database("example.json")

    # Dodaje dane do bazy
    db.update_data("user1", {"name": "Jan", "age": 30})
    db.update_data("user2", {"name": "Anna", "age": 25})

    # Pobiera i wyświetla dane
    print(db.get_data("user1"))  # {'name': 'Jan', 'age': 30}
    print(db.get_data("user3"))  # None