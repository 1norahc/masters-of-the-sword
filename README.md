# Masters of the sword

The game "Masters of the sword" allows players to create their own character, choose class and allocate stats, then fight against randomly  generated opponents. The gameplay is based on atuomatic battles, where the chances of using certain attacks are determined by percentages.

UPDATE requirements.txt, w terminalu wpisujesz pip3 freeze > requirements.txt

# Game overview:
## 1. Players can choose 3 classes:
- Warrior
- Mage
- Archer

## 2. Players can modify 4 stats:
- Strength
- Intelligence
- Dexterity
- Armor

## 3. Characters can use Abilities depending on Classes:
- Warrior (normal attack, hard attack)
- Mage (Fireball, Staff attack)
- Archer (Normal shot, Hard shot)

## 4. Items - can be used to modify all stats. Each players can choose starting equipement when creating a profile.

## 5. Fights - players can fight randomly generated opponents.

## 6. Player's profile need to containt informations such as:
* Name
* Class
* Initial Stats - players will have 10 starting points to choose from besides initial ones that are the same for each character
* Items - players can choose initial items that supplement their Stats

## 7. Fights - automatic fights based on % of chance to use non-standard attack

# BACKEND
1. Logika gry:
* tworzenie użytkownika
* tworzenie postaci
* walidacja wyboru - itemów i statysyk
* symulacja automatycznej walki bazującej na statystykach gracza, oponenta oraz szansach na atki specjalne

2. Utworzenie baz danych dla przechowywania informacji o graczu, itemach, statystykach, przeciwnikach, wynikach walk.





