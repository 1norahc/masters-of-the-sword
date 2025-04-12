from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import random

app = Flask(__name__)
app.secret_key = "tajny_klucz"  # Niezbędny do korzystania z sesji


# ------------------------------------------------
# Modele – przykładowe klasy dla postaci, przeciwników i przedmiotów
# ------------------------------------------------

class Character:
    def __init__(self, name, strength, agility, intelligence, armor, hp, inventory=None):
        self.name = name
        self.base_stats = {
            "strength": strength,
            "agility": agility,
            "intelligence": intelligence,
            "armor": armor,
            "hp": hp
        }
        self.current_stats = self.base_stats.copy()
        self.current_stats["hp"] = hp
        self.inventory = inventory if inventory is not None else []  # lista nazw przedmiotów
        # Sloty: weapon, armor, helmet, boots
        self.equipment = {"weapon": None, "armor": None, "helmet": None, "boots": None}

    def recalc_stats(self):
        """Przelicza bieżące statystyki na podstawie statystyk bazowych oraz bonusów ze sprzętu."""
        self.current_stats = self.base_stats.copy()
        for slot, item_name in self.equipment.items():
            if item_name is not None and item_name in ITEMS:
                item = ITEMS[item_name]
                for stat in ["strength", "agility", "intelligence", "armor", "hp"]:
                    self.current_stats[stat] += item.get(stat, 0)
        # Możemy ograniczyć np. HP, aby nie przekraczało określonej wartości – dla uproszczenia pomijamy to tutaj

    def equip_item(self, item_name):
        """Wyposaża przedmiot w odpowiedni slot na podstawie jego własności."""
        if item_name not in ITEMS:
            return False
        item = ITEMS[item_name]
        slot = item["slot"]
        self.equipment[slot] = item_name
        self.recalc_stats()
        return True

    def as_dict(self):
        return {
            "name": self.name,
            "base_stats": self.base_stats,
            "current_stats": self.current_stats,
            "inventory": self.inventory,
            "equipment": self.equipment
        }

    @classmethod
    def from_dict(cls, data):
        char = cls(
            data["name"],
            data["base_stats"]["strength"],
            data["base_stats"]["agility"],
            data["base_stats"]["intelligence"],
            data["base_stats"]["armor"],
            data["base_stats"]["hp"],
            data.get("inventory", [])
        )
        char.equipment = data.get("equipment", {"weapon": None, "armor": None, "helmet": None, "boots": None})
        char.recalc_stats()
        return char


class Enemy:
    def __init__(self, name, strength, agility, armor, hp):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.armor = armor
        self.hp = hp


# Przykładowe przedmioty – bonusy oraz przypisanie slotu
ITEMS = {
    "Miecz": {"slot": "weapon", "strength": 3, "agility": 1, "intelligence": 0, "armor": 0, "hp": 0},
    "Topór": {"slot": "weapon", "strength": 4, "agility": -1, "intelligence": 0, "armor": 0, "hp": 0},
    "Zbroja": {"slot": "armor", "strength": 0, "agility": 0, "intelligence": 0, "armor": 5, "hp": 20},
    "Hełm": {"slot": "helmet", "strength": 0, "agility": 0, "intelligence": 0, "armor": 2, "hp": 10},
    "Buty": {"slot": "boots", "strength": 0, "agility": 2, "intelligence": 0, "armor": 0, "hp": 5}
}

# Przykładowi przeciwnicy – do walki na arenie
ARENA_ENEMIES = [
    Enemy("Goblin", strength=4, agility=3, armor=1, hp=40),
    Enemy("Ork", strength=6, agility=2, armor=3, hp=50),
    Enemy("Troll", strength=8, agility=1, armor=4, hp=60)
]


# ------------------------------------------------
# Routing – strony aplikacji
# ------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session["username"] = username
            flash(f"Witaj, {username}!")
            return redirect(url_for("main_menu"))
        else:
            flash("Podaj nazwę użytkownika.")
    return render_template("login.html", title="Logowanie")


@app.route("/main")
def main_menu():
    return render_template("main_menu.html", title="Menu Główne")


@app.route("/create_character", methods=["GET", "POST"])
def create_character():
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            flash("Podaj nazwę postaci!")
            return redirect(url_for("create_character"))
        try:
            strength = int(request.form.get("strength"))
            agility = int(request.form.get("agility"))
            intelligence = int(request.form.get("intelligence"))
            armor = int(request.form.get("armor"))
            hp = int(request.form.get("hp"))
        except ValueError:
            flash("Błędne dane statystyczne!")
            return redirect(url_for("create_character"))
        character = Character(name, strength, agility, intelligence, armor, hp)
        session["character"] = character.as_dict()
        flash(f"Postać {name} została utworzona!")
        return redirect(url_for("main_menu"))
    return render_template("create_character.html", title="Utwórz Postać")


@app.route("/battle")
def battle():
    if "character" not in session:
        flash("Najpierw utwórz postać!")
        return redirect(url_for("main_menu"))
    char = Character.from_dict(session.get("character"))
    enemy_proto = random.choice(ARENA_ENEMIES)
    enemy = Enemy(enemy_proto.name, enemy_proto.strength, enemy_proto.agility, enemy_proto.armor, enemy_proto.hp)

    log = []
    round_num = 1
    log.append(f"START WALKI: {char.name} vs {enemy.name}")
    while char.current_stats["hp"] > 0 and enemy.hp > 0:
        log.append(f"--- Runda {round_num} ---")
        if random.choice([True, False]):
            dmg = char.current_stats["strength"] + random.randint(0, char.current_stats["agility"])
            enemy.hp -= dmg
            log.append(f"{char.name} zadaje {dmg} obrażeń {enemy.name}. (HP przeciwnika: {max(enemy.hp, 0)})")
            if enemy.hp <= 0:
                break
            dmg_enemy = enemy.strength + random.randint(0, enemy.agility)
            char.current_stats["hp"] -= dmg_enemy
            log.append(
                f"{enemy.name} zadaje {dmg_enemy} obrażeń {char.name}. (HP gracza: {max(char.current_stats['hp'], 0)})")
        else:
            dmg_enemy = enemy.strength + random.randint(0, enemy.agility)
            char.current_stats["hp"] -= dmg_enemy
            log.append(
                f"{enemy.name} zadaje {dmg_enemy} obrażeń {char.name}. (HP gracza: {max(char.current_stats['hp'], 0)})")
            if char.current_stats["hp"] <= 0:
                break
            dmg = char.current_stats["strength"] + random.randint(0, char.current_stats["agility"])
            enemy.hp -= dmg
            log.append(f"{char.name} zadaje {dmg} obrażeń {enemy.name}. (HP przeciwnika: {max(enemy.hp, 0)})")
        round_num += 1

    if char.current_stats["hp"] > 0:
        result = f"🏆 {char.name} wygrywa walkę!"
        drop_item = None
        if random.random() < 0.3:
            drop_item = random.choice(list(ITEMS.keys()))
            log.append(f"Przeciwnik upuścił przedmiot: {drop_item}!")
            item = ITEMS[drop_item]
            # Aktualizacja statystyk postaci bazowych (na przyszłe walki)
            char.base_stats["strength"] += item["strength"]
            char.base_stats["agility"] += item["agility"]
            char.base_stats["intelligence"] += item["intelligence"]
            char.base_stats["armor"] += item["armor"]
            char.base_stats["hp"] += item["hp"]
            char.inventory.append(drop_item)
        log.append(result)
        session["character"] = char.as_dict()
        return render_template("result.html", log=log, drop_item=drop_item, title="Wynik Walki")
    else:
        result = f"💀 {enemy.name} zwycięża!"
        log.append(result)
        session["character"] = char.as_dict()
        return render_template("result.html", log=log, drop_item=None, title="Wynik Walki")


@app.route("/inventory")
def inventory():
    if "character" not in session:
        flash("Najpierw utwórz postać!")
        return redirect(url_for("main_menu"))
    char = Character.from_dict(session.get("character"))
    return render_template("inventory.html", character=char, title="Ekwipunek")


# ------------------------------------------------
# Nowy ekran – zarządzanie wyposażeniem (drag & drop)
# ------------------------------------------------

@app.route("/equipment")
def equipment():
    if "character" not in session:
        flash("Najpierw utwórz postać!")
        return redirect(url_for("main_menu"))
    char = Character.from_dict(session.get("character"))
    # Przekazujemy listę przedmiotów z inwentarza oraz obecne wyposażenie
    return render_template("equipment.html", character=char, items=char.inventory, title="Zarządzanie Ekwipunkiem")


@app.route("/update_equipment", methods=["POST"])
def update_equipment():
    if "character" not in session:
        return jsonify({"success": False, "message": "Nie znaleziono postaci w sesji."})
    data = request.get_json()
    slot = data.get("slot")
    item = data.get("item")
    char = Character.from_dict(session.get("character"))
    # Spróbuj wyposażyć podany przedmiot
    if item in char.inventory and char.equip_item(item):
        # Po wyekwipowaniu możesz opcjonalnie usunąć przedmiot z inwentarza,
        # jeśli chcesz, aby dany przedmiot był jednokrotnie używany.
        # Tutaj pozostawiamy go w inwentarzu.
        session["character"] = char.as_dict()
        return jsonify({"success": True, "message": f"Wyposażono {item} w slot {slot}."})
    else:
        return jsonify({"success": False, "message": "Nie udało się wyekwipować przedmiotu."})


# ------------------------------------------------
# Uruchomienie aplikacji
# ------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

