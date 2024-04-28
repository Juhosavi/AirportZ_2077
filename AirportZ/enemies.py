import random

from search_db import search_db
class Enemy:
    def __init__(self, level, hp, name, mindmg, maxdmg, exp_per_kill):
        self.level = level
        self.hp = hp
        self.mindmg = mindmg
        self.maxdmg = maxdmg
        self.name = name
        self.exp_per_kill = exp_per_kill









def get_enemies(new_location):
    result = search_db(f"SELECT enemy_lvl, enemy_health, enemy_name, enemy_MINdmg, enemy_MAXdmg, exp_per_kill FROM enemy, airport WHERE airport.difficulty = enemy.enemy_lvl AND airport.ident = '{new_location}'")
    enemy_lvl, enemy_hp, name, mindmg, maxdmg, exp = result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5]
    enemy_amount = random.randint(1, 3)

    enemy_list = []
    while enemy_amount > len(enemy_list):
        enemy_list.append(Enemy(enemy_lvl, enemy_hp, name, mindmg, maxdmg, exp))

    # for enemy in enemy_list:
    #     print(enemy.hp)

    return enemy_list


# get_enemies("EFHK")