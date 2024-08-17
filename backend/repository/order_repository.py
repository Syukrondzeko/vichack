import sqlite3
from enum import Enum
from typing import Optional

import db_util

class OrderStatus(Enum):
    WAITING_FOR_QUANTITY = "WAITING_FOR_QUANTITY"
    INFO_COMPLETE = "INFO_COMPLETE"

class OrderEntity:
    def __init__(self, order_id, menu_id, quantity, status):
        self.id = order_id
        self.menu_id = menu_id
        self.quantity = quantity
        self.status = status

def insert_order(menu_id: int) -> None:
    with sqlite3.connect(db_util.DB_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            INSERT INTO orders VALUES (NULL, {menu_id}, NULL, "{OrderStatus.WAITING_FOR_QUANTITY.value}")
            """
        )
        connection.commit()

def get_order_by_menu_id(menu_id: int) -> Optional[OrderEntity]:
    with sqlite3.connect(db_util.DB_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            SELECT * FROM orders WHERE menu_id = {menu_id}
            """
        )

        rows = [ row for row in cursor ]
        if len(rows) == 0:
            return None
        
        return [ OrderEntity(row[0], row[1], row[2], row[3]) for row in rows ][0]
    
def get_last_order() -> Optional[OrderEntity]:
    with sqlite3.connect(db_util.DB_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            SELECT * FROM orders
            ORDER BY order_id
            LIMIT 1
            """
        )

        rows = [ row for row in cursor ]
        if len(rows) == 0:
            return None
        
        return [ OrderEntity(row[0], row[1], row[2], row[3]) for row in rows ][0]
    
def get_incomplete_orders() -> list[OrderEntity]:
    with sqlite3.connect(db_util.DB_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            SELECT * FROM orders
            WHERE status != '{OrderStatus.INFO_COMPLETE.value}'
            """
        )
        
        return [ OrderEntity(row[0], row[1], row[2], row[3]) for row in cursor ]
    
def delete_order_by_id(order_id: int) -> None:
    with sqlite3.connect(db_util.DB_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            DELETE FROM orders
            WHERE order_id == {order_id}
            """
        )

        connection.commit()
        
        return [ OrderEntity(row[0], row[1], row[2], row[3]) for row in cursor ]
    
def update_order_quantity(order_id: int, quantity: str) -> None:
    with sqlite3.connect(db_util.DB_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"""
            UPDATE orders
            SET quantity = "{quantity}", status = "{OrderStatus.INFO_COMPLETE.value}"
            WHERE order_id == {order_id}
            """
        )

        connection.commit()

if __name__ == "__main__":
    """Sanity Check"""
    db_util.init_db()

    menu_id = 1

    # insert an order
    insert_order(menu_id)

    # Get order by menu id
    order = get_order_by_menu_id(menu_id)

    # update order quantity
    update_order_quantity(order.id, "1 bucket")

    # get the updated order
    updated_order = get_order_by_menu_id(menu_id)

    assert updated_order.menu_id == 1
    assert updated_order.quantity == "1 bucket"
    assert updated_order.status == OrderStatus.INFO_COMPLETE.value
        