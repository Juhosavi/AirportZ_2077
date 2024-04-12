import random
from search_db import search_db


def search_airport(screen_name):
    result = search_db(f"SELECT bandage, kerosene FROM inventory, player WHERE screen_name = '{screen_name}' AND player.inventory_id = inventory.inventory_id")
    bandage = random.randint(0,2)
    kerosene = random.randint(1,2)
    print(f"You found {bandage} bandage!")
    print(f"You found {kerosene} fuel!\n")
    bandage = result[0][0] + bandage
    kerosene = result[0][1] + kerosene
    sql = f"UPDATE inventory, player SET bandage = '{bandage}', kerosene = '{kerosene}' WHERE screen_name = '{screen_name}' AND player.inventory_id = inventory.inventory_id"
    search_db(sql)
