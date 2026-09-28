import random
import json
import os

from missions import missions, final_missions
from achievements import achievements

level = 0
xp = 0
next_level = 100
gc = 0

skills = {
    "exploration": 0,
    "creativity": 0,
    "resistance": 0,
    "observation": 0,
    "audacity": 0
}

completed_missions = 0
secrets = 0
unlocked_achievements = []

inventory = [
    "Phone",
    "Water bottle",
    "Simple fishing gear"
]

active_missions = []
active_final_missions = None
own_missions = []

game_completed = False

file = "save.json"

def save_game():
    data = {
        "level": level,
        "xp": xp,
        "next_level": next_level,
        "gc": gc,
        "skills": skills,
        "completed_missions": completed_missions,
        "secrets": secrets,
        "unlocked_achievements": unlocked_achievements,
        "inventory": inventory,
        "active_missions": active_missions,
        "active_final_missions": active_final_missions,
        "own_missions": own_missions,
        "game_completed": game_completed
    }

    with open(file, "w") as file:
        json.dump(data, file, indent = 4)

def load_game():
    global level, xp, next_level, gc, skills, completed_missions, secrets, achievements, inventory, active_missions, active_final_missions, missions, game_completed

    if not os.path.exists(file):
        return False

    with open(file, "r") as file:
        data = json.load(file)

    level = data["level"]
    xp = data["xp"]
    next_level = data["next_level"]
    gc = data["gc"]
    skills = data["skills"]
    completed_missions = data["completed_missions"]
    secrets = data["secrets"]
    unlocked_achievements = data["unlocked_achievements"]
    inventory = data["inventory"]
    active_missions = data["active_missions"]
    active_final_missions = data["active_final_missions"]
    own_missions = data["own_missions"]
    game_completed = data["game_completed"]
    
    for mission in own_missions:
        if mission not in missions:
            missions.append(mission)
    return True

def new_mission():
    name = input("Name of the mission: ")
    xp_reward = int(input("Points of XP the mission is worth: "))
    gc_reward = int(input("Amount of GC the mission is worth: "))
    mission = {
        "name": name,
        "xp": xp_reward,
        "gc": gc_reward,
        "skills": {
            "exploration": int(input("Exploration points?: ")),
            "creativity": int(input("Creativity points?: ")),
            "resistance": int(input("Resistance points?: ")),
            "observation": int(input("Observation points?: ")),
            "audacity": int(input("Audacity points?: "))
        }
    }

    own_missions.append(mission)
    missions.append(mission)
    save_game()

    print("\nMission added!")

def add_mission(name, xp_reward, gc_reward, skills_reward):
    mission = {
        "name": name,
        "xp": xp_reward,
        "gc": gc_reward,
        "skills": skills_reward
    }

    own_missions.append(mission)
    missions.append(mission)
    save_game()
    
def unlock_achievement(achievement):
    global achievements

    if achievement not in achievements:
        achievements.append(achievement)

        print()
        print("ACHIEVEMENT UNLOCKED!")
        print(achievement)

        save_game()

def choose_missions():
    if len(missions) < 10:
        print("There is not enough missions.")
        return []

    return random.sample(missions, k=10)

def choose_final_mission():
    return random.choice(final_missions)

def level_up():
    global level, xp, next_level

    while xp >= next_level:
        xp -= next_level
        level += 1
        next_level += 150

        print()
        print("LEVEL UP!")
        print("Now you are level:", level)

def complete_mission(mission):
    global xp, gc, completed_missions

    print()
    print("Mission completed")
    print(mission["name"])

    xp += mission["xp"]
    gc += mission["gc"]

    for skill, points in mission["skills"].items():

        skills[skill] += points

    completed_missions += 1
    level_up()
    
    if gc >= 500:
        unlock_achievement("rich")
    save_game()
    
def activate_missions():
    global active_missions, active_final_missions
    
    active_missions = choose_missions()
    active_final_missions = choose_final_mission()
    
    return active_final_missions,active_missions
    
def search_mission(name):
    for mission in active_missions:
        if mission["name"].lower() == name.lower():
            return mission

    if active_final_mission is not None:
        if active_final_mission["name"].lower() == name.lower():
            if len(active_missions) == 0:
                return active_final_mission
            else:
                print("The final mission is still locked")
                print("Complete all normal missions first")
                return None

    return None

def shop():
    global gc

    print("\n=== SHOP ===")
    print("1. Drink (20 GC)")
    print("2. Snack (60 GC)")
    print("3. Souvenir (10 GC)")

    shopping_cart = int(input("What shall we shop?: "))

    if shopping_cart == 1:
        if gc >= 20:
            gc -= 20
            print("You now may buy a drink IRL! (yes, actually)")
        else:
            print("Not enough GC.")

    elif shopping_cart == 2:
        if gc >= 60:
            gc -= 60
            print("You may now buy a snack IRL!")
        else:
            print("Not enough GC.")

    elif shopping_cart == 3:
        if gc >= 10:
            gc -= 10
            print("Why would you want this? But alright, you may now buy a souvenir...")
        else:
            print("Not enough GC.")

    else:
        print("Invalid option.")

    save_game()
    
def unlock_achievement(achievement_id):
    global unlocked_achievements

    if achievement_id not in unlocked_achievements:

        unlocked_achievements.append(achievement_id)

        achievement = achievements[achievement_id]

        print()
        print("ACHIEVEMENT UNLOCKED!")
        print(achievement["name"])
        print(achievement["description"])

        save_game()

def show_screen():
    print()
    print("╔════════════════════════════════════╗")
    print("║            PLAY SCREEN             ║")
    print("╠════════════════════════════════════╣")
    print("║ LEVEL:", level)
    print("║ XP:", xp, "/", next_level)
    print("║ GC:", gc)
    print("╠════════════════════════════════════╣")
    print("║ EXPLORATION:", skills["exploration"])
    print("║ CREATIVITY:", skills["creativity"])
    print("║ RESISTANCE:", skills["resistance"])
    print("║ OBSERVATION:", skills["observation"])
    print("║ AUDACITY:", skills["audacity"])
    print("╠════════════════════════════════════╣")
    print("║ MISSIONS:", completed_missions)
    print("║ SECRETS:", secrets)
    print("║ ACHIEVEMENTS:", len(unlocked_achievements))
    print("╠════════════════════════════════════╣")
    print("║ INVENTORY:")
    for item in inventory:
        print("║ •", item)
    print("╚════════════════════════════════════╝")
    
def new_game():
    global level, xp, next_level, gc, skills, completed_missions, secrets, unlocked_achievements, inventory, active_missions, active_final_mission, game_completed

    level = 0
    xp = 0
    next_level = 100
    gc = 0

    skills = {
        "exploration": 0,
        "creativity": 0,
        "resistance": 0,
        "observation": 0,
        "audacity": 0
    }

    completed_missions = 0
    secrets = 0
    unlocked_achievements = []
    
    game_completed = False

    inventory = [
        "Phone",
        "Water bottle",
        "Simple fishing gear"
    ]

    active_missions = choose_missions()
    active_final_mission = choose_final_mission()

    save_game()

    print("\nNew game started!")
    
def continue_game():
    if load_game():
        print("\nGame loaded!")
        return True

    print("\nThere is no saved game")
    return False

def start_game():
    global game_completed
    
    while True:
        print("\n 1. Complete mission")
        print("2. Show stats")
        print("3. Check for level up")
        print("4. Show active missions")
        print("5. Shop")
        print("6. Achievements")
        print("0. Exit game")

        option = int(input("What are we gonna do?: "))

        if option == 1:
            mission_name = input(
                "What mission are we gonna complete?: "
            )

            mission = search_mission(mission_name)

            if mission is not None:

                if mission in active_missions:
                    complete_mission(mission)
                    active_missions.remove(mission)
                    
                    if completed_missions == 1:
                        unlock_achievement("first_steps")
                    
                    save_game()

                if len(active_missions) == 0:
                    print("\nAll normal missions completed")
                    print("Final mission unlocked!")

                elif mission == active_final_mission:
                    game_completed = True
                    unlock_achievement("game_completed")
                    
                    complete_mission(mission)
                    print("\nFinal mission completed!")
                    print("GAME COMPLETED!")
                    save_game()

        elif option == 2:
            show_screen()

        elif option == 3:
            level_up()

        elif option == 4:
            print("\n=== ACTIVE MISSIONS: ===")
            for mission in active_missions:
                print("-", mission["name"])
                
        elif option == 5:
            shop()
            
        elif option == 6:
            print("\n=== ACHIEVEMENTS ===")

            for achievement_id, achievement in achievements.items():

                if achievement_id in unlocked_achievements:
                    print("[UNLOCKED]", achievement["name"])
                    print("           ", achievement["description"])

                else:
                    print("[LOCKED]", achievement["name"])
        elif option == 0:
            print("Game exited")
            break

        else:
            print("Invalid option")

#Start menu
print("1. Add mission")
print("2. New game")
print("3. Continue")

menu = int(input("What are we gonna do?: "))

if menu == 1:
    new_mission()

elif menu == 2:
    new_game()

    print("\nYour missions are:")

    for mission in active_missions:
        print("-", mission["name"])

    print("- Final:", active_final_mission["name"])

    start_game()

elif menu == 3:
    if continue_game():

        print("\nYour missions are:")

        for mission in active_missions:
            print("-", mission["name"])

        print("- Final:", active_final_mission["name"])

        start_game()

else:
    print("Invalid option")
