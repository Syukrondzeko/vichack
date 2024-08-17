import sqlite3

import db_util

class MenuEntity:
    def __init__(self, menu_id, menu_name, price):
        self.id = menu_id
        self.menu_name = menu_name
        self.price = price

def get_all_menu() -> list[MenuEntity]:
    with sqlite3.connect(db_util.DB_URL) as connection:
        cursor = connection.execute(
            """
            SELECT * FROM menu
            """
        )

        return [ MenuEntity(row[0], row[1], row[2]) for row in cursor ]
    
def get_menu_by_name(menu_name: str) -> MenuEntity:
    with sqlite3.connect(db_util.DB_URL) as connection:
        cursor = connection.execute(
            f"""
            SELECT * FROM menu WHERE menu_name = "{menu_name}"
            """
        )

        rows = [ row for row in cursor ]
        if len(rows) == 0:
            return None

        return [ MenuEntity(row[0], row[1], row[2]) for row in cursor ][0]

if __name__ == "__main__":
    db_util.init_db()

    menus = get_all_menu()

    print(menus[1].__dict__)

    fried_chicken = get_menu_by_name(menu_name="fried chicken")

    print(fried_chicken.__dict__)
