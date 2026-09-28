import random
from missions import missions, final_missions

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
achievements = 0

inventory = [
    "Phone",
    "Water bottle",
    "Simple fishing gear"
]

active_missions = []
active_final_missions = []

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

    missions.append(mission)

    print()
    print("MISSION ADDED!")

def add_mission(name, xp_reward, gc_reward, skills_reward):
    mission = {
        "name": name,
        "xp": xp_reward,
        "gc": gc_reward,
        "skills": skills_reward
    }

    missions.append(mission)


def choose_missions():
    if len(missions) < 10:
        print("There is not enough missions.")
        return []

    return random.sample(missions, k=10)


def choose_final_mission():
    return random.choice(final_missions)


def level_up():
    global level
    global xp
    global next_level

    while xp >= next_level:
        xp -= next_level
        level += 1
        next_level += 150

        print()
        print("LEVEL UP!")
        print("Now you are level:", level)


def complete_mission(mission):
    global xp
    global gc
    global completed_missions

    print()
    print("MISSION COMPLETED")
    print(mission["name"])

    xp += mission["xp"]
    gc += mission["gc"]

    for skill, points in mission["skills"].items():

        skills[skill] += points

    completed_missions += 1
    level_up()
    
def activate_missions():
    global active_missions
    global active_final_missions
    
    active_missions = choose_missions()
    active_final_missions = choose_final_mission()
    
    return active_final_missions,active_missions
    
def search_mission(name):
    global active_missions
    global active_final_missions
    
    for mission in active_missions:
    
            if mission["name"].lower() == name.lower():
                return mission
    
    if active_final_missions["name"].lower() == name.lower():
        return active_final_missions
    
    return None

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
    print("║ ACHIEVEMENTS:", achievements)
    print("╠════════════════════════════════════╣")
    print("║ INVENTORY:")
    for item in inventory:
        print("║ •", item)
    print("╚════════════════════════════════════╝")
    
def start_game():
    while True:
        print("\n 1. Complete mission")
        print("2. Show stats")
        print("3. Check for level up")
        print("4. Show active missions")
        print("5. Exit game")

        option = int(input("What are we gonna do?: "))

        if option == 1:
            mission_name = input(
                "What mission are we gonna complete?: "
            )

            mission = search_mission(mission_name)

            if mission is not None:
                complete_mission(mission)

                if mission in active_missions:
                    active_missions.remove(mission)
                elif mission == active_final_missions:
                    print("FINAL MISSION COMPLETED!")

            else:
                print("Mission not found.")

        elif option == 2:
            show_screen()

        elif option == 3:
            level_up()

        elif option == 4:
            print("\nACTIVE MISSIONS:")
            for mission in active_missions:
                print("-", mission["name"])

        elif option == 5:
            print("GAME EXITED.")
            break

        else:
            print("Invalid option.")

#Start menu
print("1. Add mission")
print("2. Start game")
menu = int(input("What are we gonna do?: "))

if menu == 1:
    new_mission()
    
elif menu == 2:

    activate_missions()

    print("\nYour missions are:")

    for mission in active_missions:
        print("-", mission["name"])

    print("- Final:", active_final_missions["name"])

    start_game()
