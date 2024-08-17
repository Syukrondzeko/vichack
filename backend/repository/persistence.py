import shelve
import mapper.wav_mapper as wav_mapper

ORDER_FILENAME = "./restaurant_data/order"
STATE_FILENAME = "./restaurant_data/state"

def initialize_order_db() -> None:
    with shelve.open(ORDER_FILENAME) as order_entity:
        order_entity["orders"] = []

def intialize_state_db() -> None:
    with shelve.open(STATE_FILENAME) as state_entity:
        state_entity["state"] = "START"

def create_order(menu_name: str) -> None:
    with shelve.open(ORDER_FILENAME,writeback=True) as order_entity:
        order_entity["orders"].append({"menu_name": menu_name})

def get_all_orders() -> list[dict]:
    with shelve.open(ORDER_FILENAME) as order_entity:
        return order_entity["orders"]
    
def get_last_order() -> dict:
    with shelve.open(ORDER_FILENAME) as order_entity:
        return order_entity["orders"][-1]
    
def update_last_order_quantity(quantity: str) -> None:
    with shelve.open(ORDER_FILENAME, writeback=True) as order_entity:
        order_entity["orders"][-1]["quantity"] = quantity

def get_state() -> str:
    with shelve.open(STATE_FILENAME) as state_entity:
        return state_entity["state"]

def update_state(new_state: str) -> None:
    with shelve.open(STATE_FILENAME, writeback=True) as state_entity:
        state_entity["state"] = new_state

if __name__ == "__main__":
    """
    Sanity check
    """
    initialize_order_db()
    create_order("fried chicken drumstick")
    assert get_all_orders() == [{'menu_name': 'fried chicken drumstick'}]
    update_last_order_quantity(quantity="1 bucket")
    assert get_last_order() == {'menu_name': 'fried chicken drumstick', 'quantity': '1 bucket'}

    intialize_state_db()
    assert get_state() == "START"
    update_state("GREET")
    assert get_state() == "GREET"
