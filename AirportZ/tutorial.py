import random
import time
import sys
import colorama
from input_validation import input_check
from search_db import search_db
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
from battles import battle_start


# DISCLAIMER: Prologue-funktio on täynnä dialogia, joten se on funktiona huomattavasti pitempi kuin yksikään toinen
# funktio pelissä. Prologue on olemassa vain johdantona peliin uudelle pelaajalle.
# Funktiossa pelaaja voi valita vaihtoehdoista, joista useimmista ei tapahdu mitään erilaista.
# Tämä tapahtuu vain siksi, että pelaaja totuttelee käyttämään valintoja pelaamiseen, ja feikkivalinnoista
# hänelle voi syntyä kuitenkin immersio peliin.
# Tätä ns. tutoriaalia ei ole pakko pelata, vaan sen voi skippaa.

def npc_talk(string):
    for char in string:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)


def clearscreen():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


def player_death():
    clearscreen()
    print("You died.\n\n\n")
    time.sleep(3)
    clearscreen()
    print("GAME OVER.\n\n\n")
    time.sleep(3)
    exit()


def prologue(name):
    result = search_db(f"SELECT airport.name, ident FROM airport, player WHERE player.location = airport.ident AND screen_name = '{name}'")
    location, location_ident = result[0][0], result[0][1]
    destination = search_db(f"SELECT airport.name FROM airport, player WHERE screen_name = '{name}' AND player.destination = airport.ident")[0][0]
    clearscreen()
    print('"..hey..."\n\n\n\n\n')
    time.sleep(3)
    clearscreen()
    print('"..Hey..!"\n\n\n\n\n')
    time.sleep(3)
    clearscreen()
    npc_talk(". . . . . . . .")
    time.sleep(2)
    clearscreen()
    print(f'"WAKE UP {name}!!!"\n\n\n\n\n')
    time.sleep((3))
    clearscreen()
    print("You open your eyes. As your vision clears, you recognise your friend, hunched over you.\n\n")
    selection1 = input('        1. "What\'s going on..?"\n        2. "My head hurts.."\n\n\nSelect your response (1-2): ')
    selection1 = input_check(selection1, 2)
    clearscreen()
    npc_talk(f'"You blacked out after you got hit. We\'re still at {location}. But you have to get out of here!"')
    time.sleep(1)
    print("\n\nHer voice has an edge of panic to it. You hear growling from outside, like a pack of animals is circling the building.\n\n")
    selection2 = input('         1. "What\'s that sound?"\n         2. "My head hurts.."\n\n\nSelect your response (1-2): ')
    selection2 = input_check(selection2, 2)
    clearscreen()
    npc_talk('"Let\'s get you patched up first. Here." ')
    time.sleep(1)
    print("She hands you a bandage.")
    time.sleep(1)
    npc_talk('"Use this. Your health isn\'t looking great."')
    print("\n")
    time.sleep(2)
    print("Your current health is 50/100. You now have a bandage in your inventory. A bandage will heal you for 50 health points.\n\n")
    selection3 = input('        1. "Thanks, I\'ll use it."\n\n\nSelect your response (1): ')
    selection3 = input_check(selection3, 1)
    clearscreen()
    print("\nYou used a bandage. Your health is now 100/100.\n\n\n\n")
    time.sleep(3)
    clearscreen()
    npc_talk('"We don\'t have much time. Listen..."\n\n')
    time.sleep(1)
    print("She gasps in pain and holds a palm to her stomach. A dark pooling of blood oozes between her fingers.\n")
    time.sleep(3.5)
    npc_talk('" ...I\'m not going to make it. I got ... bit by one of those damn monsters."\n\n')
    time.sleep(2)
    npc_talk('"Take this." ')
    time.sleep(2)
    print("She holds out a handgun. You reach for it.\n")
    time.sleep(2)
    npc_talk(f'"There is a vaccine for the virus.. Get yourself to {destination}. I don\'t care how you do it, just promise me you\'ll make it." ')
    time.sleep(1)
    print("Her eyes plead with you.\n")
    time.sleep(2)
    npc_talk('"...My son was taken there. Please, find him and make sure he\'s safe!"')
    time.sleep(2)
    selection4 = input('\n\n        1. "I promise I\'ll find him."\n        2. "Whatever, buddy. Thanks for the gun."\n\n\nSelect your response (1): ')
    selection4 = input_check(selection4, 2)
    clearscreen()
    npc_talk(('"......."\n\n'))
    time.sleep(2)
    npc_talk('"There\'s a plane in the hangar with enough fuel to get you to another airport. After that, you\'re going to have to find more to make your way forward."\n\n')
    time.sleep(2)
    print("A violent banging on the door accompanies the growling.\n")
    time.sleep(1)
    npc_talk('"Any second now they\'ll break through that door."')
    time.sleep(2)
    print(" Your friend slumps down against the wall. She looks at you.\n")
    time.sleep(2)
    npc_talk('"I\'m going to need you to do me one last favor.')
    time.sleep(2)
    npc_talk(' I need you to make sure I won\'t turn into one of those undead bastards."')
    time.sleep(3)
    selection5 = input('\n\n        1. Shoot her.\n        2. Walk away.\n\n\nSelect your response (1-2): ')
    selection5 = input_check(selection5, 2)
    if selection5 == 1:
        clearscreen()
        npc_talk('"Thank you.. "')
        time.sleep(1)
        print(" she whispers, as you raise the gun.\n\n")
        time.sleep(2)
        print("The crash of the door breaking is drowned out by the sound of your gunfire. You have no time to cover the body.\n")
        time.sleep(3)
        print("As you turn to the hangar, your path is blocked by a zombie. You'll have to fight your way through.")
    elif selection5 == 2:
        clearscreen()
        print("As you turn away from your friend, the door breaks and a zombie crashes in.\n")
        time.sleep(3)
        print("It lets out an inhuman screech and stumbles toward your friend, who raises her arms in vain to try to protect herself.\nThe zombie sinks its teeth into her forearm and she screams out.\n")
        time.sleep(3)
        print("Another zombie launches itself at you. You're out of options. You have to fight your way out.")
    time.sleep(5)
    battle_start(name, location_ident)


def play_prologue(name):
    choice = input("Do you want to play the prologue? Yes(1) / No(2): ")
    choice = input_check(choice, 2)
    clearscreen()
    if choice == 1:
        prologue(name)