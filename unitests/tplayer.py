
import unittest

from ..player import User

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
        Test sprawdzający poprawność zwróconych
        informacji o graczu.
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
