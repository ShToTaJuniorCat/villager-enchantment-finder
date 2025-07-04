import time

from src.enchantments_finder import (
    is_first_offer_book,
    is_second_offer_book,
    get_first_offer_enchantment,
    get_second_offer_enchantment,
    is_enchantment_a_target,
)
from src.block_interactions import (
    look_at_job_block_from_villager,
    break_block_ahead,
    place_lectern,
)
from src.villager_interactions import (
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
        if is_first_offer_book():
            first_offer_enchantment = get_first_offer_enchantment()
            print(f"First offer is enchantment {first_offer_enchantment}")

            if is_enchantment_a_target(first_offer_enchantment):
                print("Found target enchantment offer!")
                # break
        elif is_second_offer_book():
            second_offer_enchantment = get_second_offer_enchantment()
            print(f"Second offer is enchantment {second_offer_enchantment}")
            
            if is_enchantment_a_target(second_offer_enchantment):
                print("Found target enchantment offer!")
                # break

        print("No target enchantment offer found, trying again...")
        get_new_offer()


if __name__ == "__main__":
    main()
