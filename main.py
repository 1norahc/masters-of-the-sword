# masters_full_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import os

# Importujemy klasy z istniejących modułów
from player import User, Character, Characters
from characters import CLASS, ITEMS  # ITEMS to słownik przedmiotów
from enemy import ENEMIES  # przeciwnicy

LOG_FILE = "battle_log.txt"


# Pomocnicza klasa do logowania zdarzeń walki
class BattleLogger:
    @staticmethod
    def log(message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")


# Główny kontroler aplikacji – wielostronicowy interfejs Tkinter
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Masters of the Sword")
        self.geometry("800x600")
        self.resizable(False, False)

        # Użytkownik, postać wybrana do gry oraz lista postaci
        self.user = None
        self.selected_char_id = None

        # Ramki – stworzymy je i będziemy przełączać
        self.frames = {}
        for F in (LoginScreen, MainMenu, CreateCharacterScreen, CustomizeCharacterScreen, SelectCharacterScreen, BattleScreen, ItemsScreen):
            page = F(parent=self, controller=self)
            self.frames[F] = page
            page.place(x=0, y=0, relwidth=1, relheight=1)
        self.show_frame(LoginScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Ekran logowania – tworzy/ładuje użytkownika
class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        lbl = tk.Label(self, text="Masters of the Sword", font=("Arial", 24))
        lbl.pack(pady=30)

        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Button(self, text="Login / Create User", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        if not username or not email:
            messagebox.showerror("Błąd", "Wprowadź nazwę użytkownika i email!")
            return
        # Tworzymy użytkownika (klasa User z player.py)
        self.controller.user = User(username, email)
        messagebox.showinfo("Sukces", f"Zalogowano jako: {username}")
        self.controller.show_frame(MainMenu)


# Główne menu – wybór opcji: tworzenie postaci, przegląd, walka, przedmioty
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        lbl = tk.Label(self, text="Menu Główne", font=("Arial", 22))
        lbl.pack(pady=20)

        btn_create = tk.Button(self, text="Utwórz nową postać", width=25,
                                command=lambda: controller.show_frame(CreateCharacterScreen))
        btn_create.pack(pady=10)

        btn_select = tk.Button(self, text="Wybierz postać", width=25,
                               command=lambda: controller.show_frame(SelectCharacterScreen))
        btn_select.pack(pady=10)

        btn_items = tk.Button(self, text="Zobacz dostępne przedmioty", width=25,
                              command=lambda: controller.show_frame(ItemsScreen))
        btn_items.pack(pady=10)

        btn_battle = tk.Button(self, text="Walka z botem", width=25,
                               command=lambda: controller.show_frame(BattleScreen))
        btn_battle.pack(pady=10)


# Ekran tworzenia postaci – użytkownik podaje nazwę i wybiera klasę
class CreateCharacterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        lbl = tk.Label(self, text="Utwórz nową postać", font=("Arial", 20))
        lbl.pack(pady=20)

        tk.Label(self, text="Nazwa postaci:").pack(pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Wybierz klasę:").pack(pady=5)
        self.class_choice = tk.StringVar()
        self.class_box = ttk.Combobox(self, textvariable=self.class_choice, state="readonly")
        self.class_box['values'] = list(CLASS.keys())
        self.class_box.pack()

        tk.Button(self, text="Dalej", command=self.go_customize).pack(pady=20)
        tk.Button(self, text="Powrót do menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=5)

    def go_customize(self):
        name = self.name_entry.get().strip()
        class_sel = self.class_choice.get().strip()
        if not name or class_sel not in CLASS:
            messagebox.showerror("Błąd", "Podaj nazwę postaci i wybierz prawidłową klasę!")
            return
        # Przechowujemy tymczasowo dane w kontrolerze
        self.controller.temp_char_name = name
        self.controller.temp_char_class = class_sel
        self.controller.show_frame(CustomizeCharacterScreen)


# Ekran personalizacji postaci – rozdawanie 10 punktów statystycznych oraz wybór itemu
class CustomizeCharacterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        lbl = tk.Label(self, text="Dostosuj postać", font=("Arial", 20))
        lbl.pack(pady=10)

        tk.Label(self, text="Rozdaj 10 dodatkowych punktów (STR, AGI, INT)").pack(pady=5)
        frame_stats = tk.Frame(self)
        frame_stats.pack(pady=5)

        tk.Label(frame_stats, text="STR:").grid(row=0, column=0, padx=5)
        self.str_spin = tk.Spinbox(frame_stats, from_=0, to=10, width=5)
        self.str_spin.grid(row=0, column=1, padx=5)

        tk.Label(frame_stats, text="AGI:").grid(row=0, column=2, padx=5)
        self.agi_spin = tk.Spinbox(frame_stats, from_=0, to=10, width=5)
        self.agi_spin.grid(row=0, column=3, padx=5)

        tk.Label(frame_stats, text="INT:").grid(row=0, column=4, padx=5)
        self.int_spin = tk.Spinbox(frame_stats, from_=0, to=10, width=5)
        self.int_spin.grid(row=0, column=5, padx=5)

        self.sum_label = tk.Label(self, text="Suma punktów: 0 / 10")
        self.sum_label.pack(pady=5)
        # Monitorujemy zmiany spinboxów
        self.str_spin.config(command=self.update_sum)
        self.agi_spin.config(command=self.update_sum)
        self.int_spin.config(command=self.update_sum)

        tk.Label(self, text="Wybierz item (opcjonalnie):").pack(pady=5)
        self.item_choice = tk.StringVar()
        self.item_box = ttk.Combobox(self, textvariable=self.item_choice, state="readonly")
        # Dodajemy opcję 'Brak'
        values = ["Brak"] + list(ITEMS.keys())
        self.item_box['values'] = values
        self.item_box.current(0)
        self.item_box.pack(pady=5)

        tk.Button(self, text="Utwórz postać", command=self.create_character).pack(pady=15)
        tk.Button(self, text="Powrót", command=lambda: controller.show_frame(CreateCharacterScreen)).pack()

    def update_sum(self):
        try:
            s = int(self.str_spin.get())
            a = int(self.agi_spin.get())
            i = int(self.int_spin.get())
        except:
            s = a = i = 0
        total = s + a + i
        self.sum_label.config(text=f"Suma punktów: {total} / 10")

    def create_character(self):
        try:
            extra_str = int(self.str_spin.get())
            extra_agi = int(self.agi_spin.get())
            extra_int = int(self.int_spin.get())
        except:
            messagebox.showerror("Błąd", "Błędne wartości punktowe!")
            return

        if extra_str + extra_agi + extra_int != 10:
            messagebox.showerror("Błąd", "Suma punktów musi wynosić dokładnie 10!")
            return

        name = self.controller.temp_char_name
        class_sel = self.controller.temp_char_class
        base = CLASS[class_sel]

        # Podstawowe statystyki z wybranej klasy
        final_str = base.strength + extra_str
        final_agi = base.agility + extra_agi
        final_int = base.intelligence + extra_int
        final_armor = base.armor
        final_hp = base.hp

        # Dodanie statystyk z przedmiotu, jeśli wybrano
        item_key = self.item_choice.get()
        if item_key != "Brak":
            item = ITEMS[item_key]
            final_str += item.strength
            final_agi += item.agility
            final_int += item.intelligence
            final_armor += item.armor
            final_hp += item.hp

        # Tworzymy postać – wykorzystujemy klasę Character z player.py
        new_char = Character(name, class_sel)
        new_char.strength = final_str
        new_char.agility = final_agi
        new_char.intelligence = final_int
        new_char.armor = final_armor
        new_char.hp = final_hp

        # Zapisujemy postać do bazy postaci
        chars_db = Characters()
        chars_db.db.update_data(new_char.id, new_char.__dict__)

        # Dodajemy ID postaci do konta gracza – tutaj odwołujemy się do pola 'player.data'
        self.controller.user.player.data["characters"].append(new_char.id)
        self.controller.user.player.players_db.update_data(self.controller.user.player.username,
                                                           self.controller.user.player.data)

        messagebox.showinfo("Sukces",
                            f"Postać '{name}' utworzona!\nStatystyki:\nSTR: {final_str} | AGI: {final_agi} | INT: {final_int}\nARMOR: {final_armor} | HP: {final_hp}")
        self.controller.show_frame(MainMenu)


# Ekran wyboru postaci – lista postaci przypisanych do użytkownika
class SelectCharacterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        lbl = tk.Label(self, text="Wybierz postać", font=("Arial", 20))
        lbl.pack(pady=20)

        self.listbox = tk.Listbox(self, width=50, height=10)
        self.listbox.pack(pady=10)

        tk.Button(self, text="Odśwież listę", command=self.load_characters).pack(pady=5)
        tk.Button(self, text="Wybierz", command=self.select_character).pack(pady=5)
        tk.Button(self, text="Powrót do menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=5)

    def load_characters(self):
        self.listbox.delete(0, tk.END)
        user_info = self.controller.user.get_user_info()
        self.char_ids = []
        if not user_info["characters"]:
            self.listbox.insert(tk.END, "Brak postaci! Utwórz nową.")
        else:
            for char in user_info["characters"]:
                display = f"{char['name']} ({char['class']}) - Poziom: {char['level']}"
                self.listbox.insert(tk.END, display)
                self.char_ids.append(char["id"])

    def select_character(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showerror("Błąd", "Wybierz postać z listy!")
            return
        self.controller.selected_char_id = self.char_ids[selection[0]]
        messagebox.showinfo("Sukces", "Postać wybrana!")
        self.controller.show_frame(MainMenu)


# Ekran wyświetlający dostępne przedmioty
class ItemsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        lbl = tk.Label(self, text="Dostępne przedmioty", font=("Arial", 20))
        lbl.pack(pady=20)

        text = tk.Text(self, width=60, height=15)
        text.pack(pady=10)
        text.insert(tk.END, "Przykładowe przedmioty:\n")
        for key, item in ITEMS.items():
            text.insert(tk.END, f"{key} -> STR: {item.strength}, AGI: {item.agility}, INT: {item.intelligence}, ARMOR: {item.armor}, HP: {item.hp}\n")
        text.config(state="disabled")

        tk.Button(self, text="Powrót do menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=10)


# Ekran walki z botem – symulacja pojedynek wybranej postaci z losowym przeciwnikiem
class BattleScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        lbl = tk.Label(self, text="Walka z botem", font=("Arial", 20))
        lbl.pack(pady=10)

        self.text = tk.Text(self, wrap="word", width=80, height=20, font=("Courier", 10))
        self.text.pack(pady=10)

        tk.Button(self, text="Start Walki", command=self.start_battle).pack(pady=5)
        tk.Button(self, text="Powrót do menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=5)

    def start_battle(self):
        self.text.delete("1.0", tk.END)
        if not self.controller.selected_char_id:
            messagebox.showerror("Błąd", "Nie wybrano postaci! Wybierz lub utwórz postać.")
            return

        # Pobieramy postać z bazy
        char_obj = Characters().get_character(self.controller.selected_char_id)
        if not hasattr(char_obj, 'hp'):
            messagebox.showerror("Błąd", "Wybrana postać nie posiada ustawionych statystyk! Utwórz ją ponownie.")
            return

        # Wybieramy losowego przeciwnika z istniejących (plik enemy.py)
        enemy = random.choice(list(ENEMIES.values()))

        self.text.insert(tk.END, f"START WALKI:\n{char_obj.name} ({char_obj.character_class}) vs {enemy.name}\n\n")
        BattleLogger.log(f"=== Walka rozpoczęta: {char_obj.name} vs {enemy.name} ===")

        player_hp = char_obj.hp
        enemy_hp = enemy.hp
        round_num = 1

        while player_hp > 0 and enemy_hp > 0:
            self.text.insert(tk.END, f"--- Runda {round_num} ---\n")
            p_dmg = char_obj.strength + random.randint(0, char_obj.agility)
            e_dmg = enemy.strength + random.randint(0, enemy.agility)
            enemy_hp -= p_dmg
            log_line = f"{char_obj.name} zadaje {p_dmg} obrażeń. HP {enemy.name}: {max(0, enemy_hp)}"
            self.text.insert(tk.END, log_line + "\n")
            BattleLogger.log(log_line)

            if enemy_hp <= 0:
                break

            player_hp -= e_dmg
            log_line = f"{enemy.name} zadaje {e_dmg} obrażeń. HP {char_obj.name}: {max(0, player_hp)}"
            self.text.insert(tk.END, log_line + "\n\n")
            BattleLogger.log(log_line)

            round_num += 1

        if player_hp > 0:
            result = f"🏆 {char_obj.name} wygrywa walkę!"
        else:
            result = f"💀 {enemy.name} zwycięża!"

        self.text.insert(tk.END, "\n" + result)
        BattleLogger.log(result + "\n")


if __name__ == "__main__":
    # Upewnij się, że plik logu istnieje
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("=== LOGI WALKI ===\n")
    app = App()
    app.mainloop()
