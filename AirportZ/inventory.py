from search_db import search_db


def create_inventory():
    sql = f"INSERT INTO inventory (bandage, kerosene, weapon) VALUES (0, 0, '')"
    search_db(sql)
    inventory_id = search_db("SELECT MAX(inventory_id) FROM inventory")
    inv_id = int(inventory_id[0][0])
    print(f"New inventory for the new player")
    return inv_id


def print_inventory(name):
    sql = f"SELECT * FROM inventory, player WHERE inventory.inventory_id = player.inventory_id AND screen_name = '{name}'"
    result = search_db(sql)
    if result:
        print(f"Bandages: {result[0][1]}")
        print(f"Fuel: {result[0][2]}")
        print(f"Weapon: {result[0][3]}")
    else:
        print("Inventory not found.")
