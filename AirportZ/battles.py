import random
import time
import sys
import colorama
from input_validation import input_check
from search_db import search_db
from animation import player_tombstone
from enemies import get_enemies
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


def player_death():
    clear_screen()
    print("You died.\n\n\n")
    time.sleep(3)
    clear_screen()
    player_tombstone()


def clear_screen():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


def battle_loop(screen_name, new_location, player_lvl, player_maxhp, enemy_maxhp, enemy_amount, enemy_list):
    # result = search_db(f"SELECT enemy_lvl, enemy_MINdmg, enemy_MAXdmg, exp_per_kill FROM enemy, airport WHERE airport.difficulty = enemy.enemy_lvl AND airport.ident = '{new_location}'")
    # zombie_lvl, enemy_mindmg, enemy_maxdmg, exp_per_kill = result[0][0], result[0][1], result[0][2], result[0][3]
    result = search_db(f"SELECT player_health, experience, bandage, min_dmg, max_dmg FROM player, player_dmg, inventory WHERE player.inventory_id = inventory.inventory_id AND player.player_lvl = player_dmg.player_lvl AND screen_name = '{screen_name}'")
    player_hp, experience, bandages, player_min_dmg, player_max_dmg = result[0][0], result[0][1], result[0][2], result[0][3], result[0][4]
    exp_per_kill = enemy_list[0].exp_per_kill
    while True:
        i = 0
        while i < len(enemy_list):
            if enemy_list[i].hp <= 0:
                enemy_list.pop(i)
            i = i + 1
        if len(enemy_list) == 0:
            victory(enemy_amount, exp_per_kill, experience, player_hp, bandages, screen_name, new_location)
            break
        if player_hp <= 0:
            player_death()
        print_ui(player_lvl, player_hp, player_maxhp, bandages, enemy_list, enemy_maxhp)
        actions = len(enemy_list) + 1
        if actions == 2:
            player_choice = (input("Select your action.\n\n 1. Attack! \n 2. Use bandage. \n\n Action (1-2):  "))
            player_choice = input_check(player_choice, actions)
        elif actions == 3:
            player_choice = (input("Select your action.\n\n 1. Attack first zombie! \n 2. Attack second zombie! \n 3. Use bandage. \n\n Action (1-3):  "))
            player_choice = input_check(player_choice, actions)
        elif actions == 4:
            player_choice = (input("Select your action.\n\n 1. Attack first zombie! \n 2. Attack second zombie! \n 3. Attack third zombie! \n 4. Use bandage. \n\n Action (1-4):  "))
            player_choice = input_check(player_choice, actions)
        if player_choice == 1:
            enemy_list = player_turn(player_min_dmg, player_max_dmg, enemy_list, player_choice - 1)
        elif player_choice == 2:
            if actions > 2:
                enemy_list = player_turn(player_min_dmg, player_max_dmg, enemy_list, player_choice - 1)
            else:
                bandages, player_hp = use_bandage(bandages, player_hp, player_maxhp)
        elif player_choice == 3:
            if actions > 3:
                enemy_list = player_turn(player_min_dmg, player_max_dmg, enemy_list, player_choice - 1)
            else:
                bandages, player_hp = use_bandage(bandages, player_hp, player_maxhp)
        if player_choice == 4:
            bandages, player_hp = use_bandage(bandages, player_hp, player_maxhp)
        for enemy in enemy_list:
            if enemy.hp > 0:
                player_hp = enemy_turn(enemy.mindmg, enemy.maxdmg, player_hp)


def print_ui(player_lvl, player_hp, player_maxhp, bandages, enemy_list, enemy_maxhp):
    print(f"{Fore.GREEN}Player LVL.{player_lvl}  HP {player_hp}/{player_maxhp}   Bandages: {bandages}   "
          f"{Fore.WHITE}vs{Fore.RED}    Zombie LVL.{enemy_list[0].level}  HP {enemy_list[0].hp}/{enemy_maxhp}")
    i = 1
    while i < len(enemy_list):
        print(f"                                          {Fore.WHITE}vs{Fore.RED}    Zombie LVL.{enemy_list[i].level}  HP {enemy_list[i].hp}/{enemy_maxhp}\n")
        i = i + 1
    print("\n")


def credits():
    time.sleep(1)
    print(f"        DEVELOPER TEAM \n")
    time.sleep(0.5)
    print("        Tero Kettunen")
    time.sleep(0.5)
    print("         Saija Remes")
    time.sleep(0.5)
    print("       Juho Savinainen")
    time.sleep(0.5)
    print("")
    time.sleep(0.5)
    print("")
    time.sleep(0.5)
    print("")
    time.sleep(0.5)
    print("")
    time.sleep(3)
    clear_screen()
    exit()


def game_completed(screen_name):
    print("\n\nYou have arrived at your destination! You received a vaccine for the virus!\n")
    battles_won = search_db(f"SELECT battles_won FROM player WHERE screen_name = '{screen_name}'")[0][0]
    time.sleep(3)
    print(f"You won {battles_won} battles during your playthrough! How awesome is that?!")
    time.sleep(3)
    clear_screen()
    credits()


def destination_check(screen_name, new_location):
    destination = search_db(f"SELECT destination FROM player WHERE screen_name = '{screen_name}'")[0][0]
    if new_location == destination:
        game_completed(screen_name)


def victory(enemy_amount, exp_per_kill, experience, player_hp, bandages, screen_name, new_location):
    print(f"Congratulations! You won the battle! You gained {enemy_amount * exp_per_kill} experience points.\n")
    current_lvl = search_db(f"SELECT player_lvl FROM player WHERE screen_name = '{screen_name}'")[0][0]
    battles_won = search_db(f"SELECT battles_won FROM player WHERE screen_name = '{screen_name}'")[0][0]
    experience = experience + enemy_amount * exp_per_kill
    if experience >= 10 and experience < 20 and current_lvl == 1:
        print(f"You leveled up! You are now LVL {current_lvl + 1}.\n")
        search_db(f"UPDATE player SET player_lvl = {current_lvl + 1} WHERE screen_name = '{screen_name}'")
    elif experience >= 20 and current_lvl == 2:
        print(f"You leveled up! You are now LVL {current_lvl + 1}.\n")
        search_db(f"UPDATE player SET player_lvl = {current_lvl + 1} WHERE screen_name = '{screen_name}'")
    search_db(f"UPDATE player, inventory, airport SET experience = '{experience}', player_health = '{player_hp}', bandage = '{bandages}', player.location = '{new_location}', player.battles_won = '{battles_won + 1}' WHERE screen_name = '{screen_name}'")
    destination_check(screen_name, new_location)


def player_turn(player_min_dmg, player_max_dmg, enemy_list, player_choice):
    dmg = random.randint(player_min_dmg, player_max_dmg)
    print(f"\nYou attack with your weapon! You inflict {dmg} damage on the enemy.\n")
    enemy_list[player_choice].hp = enemy_list[player_choice].hp - dmg
    time.sleep(2)
    return enemy_list


def enemy_turn(enemy_mindmg, enemy_maxdmg, player_hp):
    enemy_dmg = random.randint(enemy_mindmg, enemy_maxdmg)
    print(f"{Fore.RED}The zombie hits you! It inflicts {enemy_dmg} damage.\n")
    player_hp = player_hp - enemy_dmg
    time.sleep(2)
    return player_hp


def use_bandage(bandages, player_hp, player_maxhp):
    if bandages > 0:
        if player_hp <= player_maxhp - 50:
            player_hp = player_hp + 50
            print(f"\nYou use a bandage. Your health is now {player_hp}/{player_maxhp}.\n")
            bandages = bandages - 1
            time.sleep(1)
        elif player_hp > player_maxhp - 50:
            player_hp = player_maxhp
            print(f"\nYou use a bandage. Your health is now {player_hp}/{player_maxhp}.\n")
            bandages = bandages - 1
            time.sleep(2)
    else:
        print("\nYou have no bandages! Your turn ends.\n")
        time.sleep(2)

    return bandages, player_hp


def battle_start(screen_name, new_location):
    sql = f"SELECT player.player_lvl FROM player WHERE screen_name = '{screen_name}'"
    player_lvl = search_db(sql)[0][0]
    # sql = f"SELECT enemy_health FROM enemy, airport WHERE airport.difficulty = enemy.enemy_lvl AND airport.ident = '{new_location}'"
    # enemy_hp = search_db(sql)[0][0]
    enemy_list = get_enemies(new_location)
    enemy_maxhp = enemy_list[0].hp
    if player_lvl == 1:
        player_maxhp = 100
    elif player_lvl == 2:
        player_maxhp = 150
    else:
        player_maxhp = 200
    clear_screen()
    enemy_amount = len(enemy_list)
    print(f"The battle begins! You are facing {enemy_amount} zombie(s).\n\n\n\n")
    time.sleep(3)
    clear_screen()
    battle_loop(screen_name, new_location, player_lvl, player_maxhp, enemy_maxhp, enemy_amount, enemy_list)