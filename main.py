import time

from enchantments_finder import (
    is_first_offer_book,
    is_second_offer_book,
    get_first_offer_enchantment,
    get_second_offer_enchantment,
)
from block_interactions import (
    look_at_job_block_from_villager,
    break_block_ahead,
    place_lectern,
)
from villager_interactions import (
    open_villager_trading_dialog,
    exit_trading_dialog,
    look_at_villager_from_block,
)


def get_new_offer() -> None:
    exit_trading_dialog()
    look_at_job_block_from_villager()
    break_block_ahead()
    place_lectern()
    look_at_villager_from_block()
    open_villager_trading_dialog()


def main() -> None:
    time.sleep(4)

    while True:
        print("Checking for enchanted book offers...")
        if is_first_offer_book():
            print(f"First offer is enchantment {get_first_offer_enchantment()}")
        elif is_second_offer_book():
            print(f"Second offer is enchantment {get_second_offer_enchantment()}")
        else:
            print("No enchanted book offer found, trying again...")
            get_new_offer()


if __name__ == "__main__":
    main()
