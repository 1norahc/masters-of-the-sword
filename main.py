import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import os
import sys
import numpy as np  # Do prostych obliczeń sieci neuronowej

# Importujemy klasy z istniejących modułów
from player import User, Character, Characters
from characters import CLASS, ITEMS  # ITEMS to słownik przedmiotów
from enemy import ENEMIES  # przeciwnicy

LOG_FILE = "battle_log.txt"

# =============================================================================
# Klasy do symulacji sieci neuronowych dla botów
# =============================================================================

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Losowe wagi i biasy
        self.weights1 = np.random.randn(input_size, hidden_size)
        self.bias1 = np.zeros(hidden_size)
        self.weights2 = np.random.randn(hidden_size, output_size)
        self.bias2 = np.zeros(output_size)

    def forward(self, x):
        # Aktywacja tanh
        h = np.tanh(np.dot(x, self.weights1) + self.bias1)
        o = np.tanh(np.dot(h, self.weights2) + self.bias2)
        return o

class NeuralBot:
    def __init__(self, name, difficulty):
        self.name = name
        if difficulty == 'easy':
            input_size = 5; hidden_size = 3; output_size = 1
            self.hp = 50
            self.strength = 5
            self.agility = 3
        elif difficulty == 'medium':
            input_size = 5; hidden_size = 5; output_size = 1
            self.hp = 70
            self.strength = 7
            self.agility = 5
        else:  # hard
            input_size = 5; hidden_size = 7; output_size = 1
            self.hp = 90
            self.strength = 9
            self.agility = 7
        self.nn = NeuralNetwork(input_size, hidden_size, output_size)

    def decide_attack(self, opponent_stats):
        """
        opponent_stats – wektor: [hp_gracza, strength, agility, intelligence, armor]
        Wyjście z sieci neuronowej normalizujemy do [0,1] i traktujemy jako mnożnik bonusowy.
        """
        output = self.nn.forward(np.array(opponent_stats))
        factor = (output[0] + 1) / 2  # normalizacja do [0,1]
        damage = int(self.strength + factor * self.agility)
        return damage

# =============================================================================
# Klasa do logowania zdarzeń walki
# =============================================================================

class BattleLogger:
    @staticmethod
    def log(message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

# =============================================================================
# Główny kontroler aplikacji – rozbudowany interfejs Tkinter
# =============================================================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Masters of the Sword")
        self.geometry("800x600")
        self.resizable(False, False)

        self.create_menu()

        # Pasek statusu
        self.status_var = tk.StringVar()
        self.status_var.set("Gotowy")
        status_bar = tk.Label(self, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Użytkownik, postać wybrana do gry
        self.user = None
        self.selected_char_id = None

        # Ramki – dodajemy dodatkowo ekran ekwipunku
        self.frames = {}
        for F in (LoginScreen, MainMenu, CreateCharacterScreen, CustomizeCharacterScreen,
                  SelectCharacterScreen, BattleScreen, BotBattleScreen, InventoryScreen, ItemsScreen):
            page = F(parent=self, controller=self)
            self.frames[F] = page
            page.place(x=0, y=0, relwidth=1, relheight=1)
        self.show_frame(LoginScreen)

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nowa Gra", command=self.restart)
        file_menu.add_separator()
        file_menu.add_command(label="Wyjście", command=self.quit)
        menubar.add_cascade(label="Plik", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="O grze", command=self.show_about)
        menubar.add_cascade(label="Pomoc", menu=help_menu)
        self.config(menu=menubar)

    def restart(self):
        self.status_var.set("Restartowanie gry...")
        self.destroy()
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def show_about(self):
        messagebox.showinfo("O grze", "Masters of the Sword\nProsty interfejs wzorowany na Shakes & Fidget.\n\n"
                             "Podczas walki może dropnąć przedmiot, który zwiększy Twoje statystyki.")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.status_var.set(f"Aktywny ekran: {cont.__name__}")

# =============================================================================
# Ekran logowania – tworzy/ładuje użytkownika
# =============================================================================

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Masters of the Sword", font=("Arial", 24)).pack(pady=30)
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
        self.controller.user = User(username, email)
        messagebox.showinfo("Sukces", f"Zalogowano jako: {username}")
        self.controller.show_frame(MainMenu)

# =============================================================================
# Główne menu – dodano przycisk do ekwipunku
# =============================================================================

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Menu Główne", font=("Arial", 22)).pack(pady=20)
        tk.Button(self, text="Utwórz nową postać", width=25,
                  command=lambda: controller.show_frame(CreateCharacterScreen)).pack(pady=10)
        tk.Button(self, text="Wybierz postać", width=25,
                  command=lambda: controller.show_frame(SelectCharacterScreen)).pack(pady=10)
        tk.Button(self, text="Zobacz przedmioty (Globalne)", width=25,
                  command=lambda: controller.show_frame(ItemsScreen)).pack(pady=10)
        tk.Button(self, text="Ekwipunek", width=25,
                  command=lambda: controller.show_frame(InventoryScreen)).pack(pady=10)
        tk.Button(self, text="Walka z botem (klasyczna)", width=25,
                  command=lambda: controller.show_frame(BattleScreen)).pack(pady=10)
        tk.Button(self, text="Walka z botem NN", width=25,
                  command=lambda: controller.show_frame(BotBattleScreen)).pack(pady=10)

# =============================================================================
# Ekran tworzenia postaci – użytkownik podaje nazwę i wybiera klasę
# =============================================================================

class CreateCharacterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Utwórz nową postać", font=("Arial", 20)).pack(pady=20)
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
        self.controller.temp_char_name = name
        self.controller.temp_char_class = class_sel
        self.controller.show_frame(CustomizeCharacterScreen)

# =============================================================================
# Ekran personalizacji postaci – rozdawanie 10 punktów i wybór itemu
# =============================================================================

class CustomizeCharacterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Dostosuj postać", font=("Arial", 20)).pack(pady=10)
        tk.Label(self, text="Rozdaj 10 dodatkowych punktów (STR, AGI, INT)").pack(pady=5)
        frame_stats = tk.Frame(self)
        frame_stats.pack(pady=5)
        tk.Label(frame_stats, text="STR:").grid(row=0, column=0, padx=5)
        self.str_spin = tk.Spinbox(frame_stats, from_=0, to=10, width=5, command=self.update_sum)
        self.str_spin.grid(row=0, column=1, padx=5)
        tk.Label(frame_stats, text="AGI:").grid(row=0, column=2, padx=5)
        self.agi_spin = tk.Spinbox(frame_stats, from_=0, to=10, width=5, command=self.update_sum)
        self.agi_spin.grid(row=0, column=3, padx=5)
        tk.Label(frame_stats, text="INT:").grid(row=0, column=4, padx=5)
        self.int_spin = tk.Spinbox(frame_stats, from_=0, to=10, width=5, command=self.update_sum)
        self.int_spin.grid(row=0, column=5, padx=5)
        self.sum_label = tk.Label(self, text="Suma punktów: 0 / 10")
        self.sum_label.pack(pady=5)
        tk.Label(self, text="Wybierz item (opcjonalnie):").pack(pady=5)
        self.item_choice = tk.StringVar()
        self.item_box = ttk.Combobox(self, textvariable=self.item_choice, state="readonly")
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
        final_str = base.strength + extra_str
        final_agi = base.agility + extra_agi
        final_int = base.intelligence + extra_int
        final_armor = base.armor
        final_hp = base.hp
        item_key = self.item_choice.get()
        if item_key != "Brak":
            item = ITEMS[item_key]
            final_str += item.strength
            final_agi += item.agility
            final_int += item.intelligence
            final_armor += item.armor
            final_hp += item.hp
        new_char = Character(name, class_sel)
        new_char.strength = final_str
        new_char.agility = final_agi
        new_char.intelligence = final_int
        new_char.armor = final_armor
        new_char.hp = final_hp
        # Dodajemy nowy atrybut: ekwipunek
        new_char.inventory = []
        chars_db = Characters()
        chars_db.db.update_data(new_char.id, new_char.__dict__)
        self.controller.user.player.data["characters"].append(new_char.id)
        self.controller.user.player.players_db.update_data(self.controller.user.player.username,
                                                           self.controller.user.player.data)
        messagebox.showinfo("Sukces",
            f"Postać '{name}' utworzona!\nStatystyki:\nSTR: {final_str} | AGI: {final_agi} | INT: {final_int}\nARMOR: {final_armor} | HP: {final_hp}")
        self.controller.show_frame(MainMenu)

# =============================================================================
# Ekran wyboru postaci – lista postaci przypisanych do użytkownika
# =============================================================================

class SelectCharacterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Wybierz postać", font=("Arial", 20)).pack(pady=20)
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

# =============================================================================
# Ekran wyświetlający globalne dostępne przedmioty
# =============================================================================

class ItemsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Globalne Przedmioty", font=("Arial", 20)).pack(pady=20)
        text = tk.Text(self, width=60, height=15)
        text.pack(pady=10)
        text.insert(tk.END, "Dostępne przedmioty:\n")
        for key, item in ITEMS.items():
            text.insert(tk.END, f"{key} -> STR: {item.strength}, AGI: {item.agility}, "
                                 f"INT: {item.intelligence}, ARMOR: {item.armor}, HP: {item.hp}\n")
        text.config(state="disabled")
        tk.Button(self, text="Powrót do menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=10)

# =============================================================================
# Ekran ekwipunku gracza – wyświetla przedmioty zebrane w walce
# =============================================================================

class InventoryScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Twój Ekwipunek", font=("Arial", 20)).pack(pady=20)
        self.listbox = tk.Listbox(self, width=60, height=10)
        self.listbox.pack(pady=10)
        tk.Button(self, text="Odśwież", command=self.load_inventory).pack(pady=5)
        tk.Button(self, text="Powrót do menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=5)

    def load_inventory(self):
        self.listbox.delete(0, tk.END)
        # Pobieramy aktualną postać
        char_obj = Characters().get_character(self.controller.selected_char_id)
        if not hasattr(char_obj, 'inventory') or not char_obj.inventory:
            self.listbox.insert(tk.END, "Brak przedmiotów w ekwipunku.")
        else:
            for item in char_obj.inventory:
                self.listbox.insert(tk.END, f"{item} -> Bonusy: STR+{ITEMS[item].strength}, AGI+{ITEMS[item].agility}, "
                                            f"INT+{ITEMS[item].intelligence}, ARMOR+{ITEMS[item].armor}, HP+{ITEMS[item].hp}")

# =============================================================================
# Funkcja wspólna: symulacja walki z losowym ustaleniem kolejności ataków
# =============================================================================

def simulate_battle(attacker_name, defender_name, atk_func, def_func, text_widget, logger):
    """
    atk_func oraz def_func to funkcje obliczające obrażenia dla atakującego i przeciwnika.
    Funkcja symuluje rundy, w których kolejność ataków ustalana jest losowo.
    Zwraca wynik ("player" lub "enemy").
    """
    round_num = 1
    while True:
        text_widget.insert(tk.END, f"--- Runda {round_num} ---\n")
        # Losujemy, kto atakuje jako pierwszy
        if random.choice([True, False]):
            # Najpierw atakuje gracz
            dmg = atk_func()
            text_widget.insert(tk.END, f"{attacker_name} zadaje {dmg} obrażeń.\n")
            logger.log(f"{attacker_name} zadaje {dmg} obrażeń.")
            if def_func(dmg):
                break
            dmg = def_func(0, attack=True)
            text_widget.insert(tk.END, f"{defender_name} zadaje {dmg} obrażeń.\n")
            logger.log(f"{defender_name} zadaje {dmg} obrażeń.")
            if atk_func(dmg, attack=True):
                break
        else:
            dmg = def_func(0, attack=True)
            text_widget.insert(tk.END, f"{defender_name} zadaje {dmg} obrażeń.\n")
            logger.log(f"{defender_name} zadaje {dmg} obrażeń.")
            if atk_func(dmg):
                break
            dmg = atk_func()
            text_widget.insert(tk.END, f"{attacker_name} zadaje {dmg} obrażeń.\n")
            logger.log(f"{attacker_name} zadaje {dmg} obrażeń.")
            if def_func(dmg):
                break
        round_num += 1

# =============================================================================
# Ekran walki z botem – klasyczna walka z losowym przeciwnikiem
# =============================================================================

class BattleScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Walka z botem (klasyczna)", font=("Arial", 20)).pack(pady=10)
        self.text = tk.Text(self, wrap="word", width=80, height=20, font=("Courier", 10))
        self.text.pack(pady=10)
        tk.Button(self, text="Start Walki", command=self.start_battle).pack(pady=5)
        tk.Button(self, text="Powrót do menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=5)

    def start_battle(self):
        self.text.delete("1.0", tk.END)
        if not self.controller.selected_char_id:
            messagebox.showerror("Błąd", "Nie wybrano postaci! Wybierz lub utwórz postać.")
            return
        char_obj = Characters().get_character(self.controller.selected_char_id)
        if not hasattr(char_obj, 'hp'):
            messagebox.showerror("Błąd", "Postać nie posiada ustawionych statystyk! Utwórz ją ponownie.")
            return
        enemy = random.choice(list(ENEMIES.values()))
        self.text.insert(tk.END, f"START WALKI:\n{char_obj.name} ({char_obj.character_class}) vs {enemy.name}\n\n")
        BattleLogger.log(f"Walka: {char_obj.name} vs {enemy.name}")
        player_hp = char_obj.hp
        enemy_hp = enemy.hp
        round_num = 1
        # Zmodyfikowana walka: losujemy kolejność ataków
        while player_hp > 0 and enemy_hp > 0:
            if random.choice([True, False]):
                # Gracz atakuje pierwszy
                p_dmg = char_obj.strength + random.randint(0, char_obj.agility)
                enemy_hp -= p_dmg
                self.text.insert(tk.END, f"{char_obj.name} zadaje {p_dmg} obrażeń. HP {enemy.name}: {max(0, enemy_hp)}\n")
                BattleLogger.log(f"{char_obj.name} zadaje {p_dmg} obrażeń. HP {enemy.name}: {max(0, enemy_hp)}")
                if enemy_hp <= 0:
                    break
                e_dmg = enemy.strength + random.randint(0, enemy.agility)
                player_hp -= e_dmg
                self.text.insert(tk.END, f"{enemy.name} zadaje {e_dmg} obrażeń. HP {char_obj.name}: {max(0, player_hp)}\n\n")
                BattleLogger.log(f"{enemy.name} zadaje {e_dmg} obrażeń. HP {char_obj.name}: {max(0, player_hp)}")
            else:
                e_dmg = enemy.strength + random.randint(0, enemy.agility)
                player_hp -= e_dmg
                self.text.insert(tk.END, f"{enemy.name} zadaje {e_dmg} obrażeń. HP {char_obj.name}: {max(0, player_hp)}\n")
                BattleLogger.log(f"{enemy.name} zadaje {e_dmg} obrażeń. HP {char_obj.name}: {max(0, player_hp)}")
                if player_hp <= 0:
                    break
                p_dmg = char_obj.strength + random.randint(0, char_obj.agility)
                enemy_hp -= p_dmg
                self.text.insert(tk.END, f"{char_obj.name} zadaje {p_dmg} obrażeń. HP {enemy.name}: {max(0, enemy_hp)}\n\n")
                BattleLogger.log(f"{char_obj.name} zadaje {p_dmg} obrażeń. HP {enemy.name}: {max(0, enemy_hp)}")
        if player_hp > 0:
            result = f"🏆 {char_obj.name} wygrywa walkę!"
            self.text.insert(tk.END, "\n" + result)
            BattleLogger.log(result)
            self.handle_item_drop(char_obj)
        else:
            result = f"💀 {enemy.name} zwycięża!"
            self.text.insert(tk.END, "\n" + result)
            BattleLogger.log(result)

    def handle_item_drop(self, char_obj):
        # 30% szans na drop przedmiotu
        if random.random() < 0.3:
            dropped = random.choice(list(ITEMS.keys()))
            if messagebox.askyesno("Drop!", f"Przeciwnik upuścił {dropped}. Chcesz go podnieść?"):
                item = ITEMS[dropped]
                # Dodajemy do ekwipunku i aktualizujemy statystyki
                if not hasattr(char_obj, 'inventory'):
                    char_obj.inventory = []
                char_obj.inventory.append(dropped)
                char_obj.strength += item.strength
                char_obj.agility += item.agility
                char_obj.intelligence += item.intelligence
                char_obj.armor += item.armor
                char_obj.hp += item.hp
                messagebox.showinfo("Ekwipunek", f"Podniosłeś {dropped}. Twoje statystyki zostały zaktualizowane!")

# =============================================================================
# Ekran walki z botem NN – walka z botem sterowanym przez "sieć neuronową"
# =============================================================================

class BotBattleScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Walka z botem (NN)", font=("Arial", 20)).pack(pady=10)
        tk.Label(self, text="Wybierz poziom bota:").pack(pady=5)
        self.bot_choice = tk.StringVar()
        self.bot_box = ttk.Combobox(self, textvariable=self.bot_choice, state="readonly")
        self.bot_box['values'] = ["Easy", "Medium", "Hard"]
        self.bot_box.current(0)
        self.bot_box.pack(pady=5)
        self.text = tk.Text(self, wrap="word", width=80, height=20, font=("Courier", 10))
        self.text.pack(pady=10)
        tk.Button(self, text="Start Walki", command=self.start_battle).pack(pady=5)
        tk.Button(self, text="Powrót do menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=5)

    def start_battle(self):
        self.text.delete("1.0", tk.END)
        if not self.controller.selected_char_id:
            messagebox.showerror("Błąd", "Nie wybrano postaci! Wybierz lub utwórz postać.")
            return
        char_obj = Characters().get_character(self.controller.selected_char_id)
        if not hasattr(char_obj, 'hp'):
            messagebox.showerror("Błąd", "Postać nie posiada ustawionych statystyk! Utwórz ją ponownie.")
            return
        level = self.bot_choice.get().lower()
        bot = NeuralBot(name=f"Bot {level.capitalize()}", difficulty=level)
        self.text.insert(tk.END, f"START WALKI:\n{char_obj.name} ({char_obj.character_class}) vs {bot.name}\n\n")
        BattleLogger.log(f"Walka: {char_obj.name} vs {bot.name}")
        player_hp = char_obj.hp
        bot_hp = bot.hp
        round_num = 1
        # Zmodyfikowana walka – losowanie kolejności ataków
        while player_hp > 0 and bot_hp > 0:
            if random.choice([True, False]):
                p_dmg = char_obj.strength + random.randint(0, char_obj.agility)
                bot_hp -= p_dmg
                self.text.insert(tk.END, f"{char_obj.name} zadaje {p_dmg} obrażeń. HP {bot.name}: {max(0, bot_hp)}\n")
                BattleLogger.log(f"{char_obj.name} zadaje {p_dmg} obrażeń. HP {bot.name}: {max(0, bot_hp)}")
                if bot_hp <= 0:
                    break
                # Wejście do sieci NN wykorzystujące statystyki gracza
                player_stats = [player_hp, char_obj.strength, char_obj.agility, char_obj.intelligence, char_obj.armor]
                b_dmg = bot.decide_attack(player_stats)
                player_hp -= b_dmg
                self.text.insert(tk.END, f"{bot.name} zadaje {b_dmg} obrażeń. HP {char_obj.name}: {max(0, player_hp)}\n\n")
                BattleLogger.log(f"{bot.name} zadaje {b_dmg} obrażeń. HP {char_obj.name}: {max(0, player_hp)}")
            else:
                # Bot atakuje pierwszy
                player_stats = [player_hp, char_obj.strength, char_obj.agility, char_obj.intelligence, char_obj.armor]
                b_dmg = bot.decide_attack(player_stats)
                player_hp -= b_dmg
                self.text.insert(tk.END, f"{bot.name} zadaje {b_dmg} obrażeń. HP {char_obj.name}: {max(0, player_hp)}\n")
                BattleLogger.log(f"{bot.name} zadaje {b_dmg} obrażeń. HP {char_obj.name}: {max(0, player_hp)}")
                if player_hp <= 0:
                    break
                p_dmg = char_obj.strength + random.randint(0, char_obj.agility)
                bot_hp -= p_dmg
                self.text.insert(tk.END, f"{char_obj.name} zadaje {p_dmg} obrażeń. HP {bot.name}: {max(0, bot_hp)}\n\n")
                BattleLogger.log(f"{char_obj.name} zadaje {p_dmg} obrażeń. HP {bot.name}: {max(0, bot_hp)}")
            round_num += 1
        if player_hp > 0:
            result = f"🏆 {char_obj.name} wygrywa walkę!"
            self.text.insert(tk.END, "\n" + result)
            BattleLogger.log(result)
            self.handle_item_drop(char_obj)
        else:
            result = f"💀 {bot.name} zwycięża!"
            self.text.insert(tk.END, "\n" + result)
            BattleLogger.log(result)

    def handle_item_drop(self, char_obj):
        if random.random() < 0.3:
            dropped = random.choice(list(ITEMS.keys()))
            if messagebox.askyesno("Drop!", f"Bot upuścił {dropped}. Chcesz go podnieść?"):
                item = ITEMS[dropped]
                if not hasattr(char_obj, 'inventory'):
                    char_obj.inventory = []
                char_obj.inventory.append(dropped)
                char_obj.strength += item.strength
                char_obj.agility += item.agility
                char_obj.intelligence += item.intelligence
                char_obj.armor += item.armor
                char_obj.hp += item.hp
                messagebox.showinfo("Ekwipunek", f"Podniosłeś {dropped}. Statystyki zostały zaktualizowane!")

# =============================================================================
# Inicjalizacja aplikacji
# =============================================================================

if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("=== LOGI WALKI ===\n")
    app = App()
    app.mainloop()
