# masters_gui_simulation.py

import tkinter as tk
from tkinter import ttk, messagebox
from player import User, Characters
from characters import CLASS, ITEMS
from enemy import ENEMIES
import random
import datetime
import os

LOG_FILE = "battle_log.txt"

# AI helper
class AICharacter:
    def __init__(self, name, class_name):
        self.name = name
        base = CLASS[class_name]
        self.class_name = class_name
        self.strength = base.strength + random.randint(2, 5)
        self.agility = base.agility + random.randint(2, 5)
        self.intelligence = base.intelligence + random.randint(2, 5)
        self.armor = base.armor + random.randint(0, 20)
        self.hp = base.hp + random.randint(20, 50)

    def stats(self):
        return f"{self.name} [{self.class_name}] - STR:{self.strength} AGI:{self.agility} INT:{self.intelligence} ARM:{self.armor} HP:{self.hp}"

class BattleLogger:
    @staticmethod
    def log(message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

class BattleSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Battle Simulator - Masters of the Sword")
        self.geometry("800x600")

        self.text = tk.Text(self, wrap="word", font=("Courier", 10))
        self.text.pack(expand=True, fill="both")

        tk.Button(self, text="Start AI vs AI Battle", command=self.start_ai_battle).pack(pady=10)

    def start_ai_battle(self):
        self.text.delete("1.0", tk.END)

        ai1 = AICharacter("AI_Warrior", "Warrior")
        ai2 = AICharacter("AI_Mage", "Mage")

        self.text.insert(tk.END, f"🤖 {ai1.stats()}\n")
        self.text.insert(tk.END, f"🤖 {ai2.stats()}\n\n")

        BattleLogger.log(f"=== AI Battle Started: {ai1.name} vs {ai2.name} ===")
        round_num = 1

        hp1 = ai1.hp
        hp2 = ai2.hp

        while hp1 > 0 and hp2 > 0:
            self.text.insert(tk.END, f"-- Round {round_num} --\n")
            dmg1 = ai1.strength + random.randint(0, ai1.agility)
            dmg2 = ai2.strength + random.randint(0, ai2.agility)

            hp2 -= dmg1
            log1 = f"{ai1.name} deals {dmg1} damage. {ai2.name} HP left: {max(0, hp2)}"
            self.text.insert(tk.END, log1 + "\n")
            BattleLogger.log(log1)
            if hp2 <= 0:
                break

            hp1 -= dmg2
            log2 = f"{ai2.name} deals {dmg2} damage. {ai1.name} HP left: {max(0, hp1)}"
            self.text.insert(tk.END, log2 + "\n\n")
            BattleLogger.log(log2)

            round_num += 1

        if hp1 > 0:
            result = f"🏆 {ai1.name} wins the battle!"
        else:
            result = f"🏆 {ai2.name} wins the battle!"

        self.text.insert(tk.END, "\n" + result)
        BattleLogger.log(result + "\n")

if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("=== Battle Logs ===\n")

    app = BattleSimulator()
    app.mainloop()
