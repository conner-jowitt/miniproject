#!/usr/bin/env python3
# TODO change drinks/people to use database stuff, including description

import sys
import os
import menu
import store
from round import *

arguments = sys.argv

# ***************************************************************
# Other Functions
# ****************************************************************


def enter_integer(message="Please enter a number: ", err="Error! That is not a number!"):
    int_check = "False"
    while int_check == "False":
        inp = input(message)
        int_check = integer_validation(inp)
        if int_check == "False":
            print(err)
    return int_check


def integer_validation(integer):
    if str(integer).isnumeric():
        return int(integer)
    elif integer == "":
        return integer
    else:
        return "False"


def clear_screen():
    os.system("clear")


def concat_dict_key_values_to_string(orders):  # concatenate user + favourite into a single string for ease of display
    updated_order = []
    for key, value in orders.items():
        if value != "":
            updated_order.append(str(key) + ": " + str(value))
    return updated_order


def print_menu(input_menu, clear=False):
    if not clear:
        clear_screen()
    input_menu.print_ioptions()
    print("Leave blank to cancel")


def print_border(length=30):
    print("+" + "=" * length + "+")


def print_table(object_list, title, is_indexed=False):  # indexed = 0 or 1, when 1 prints an index for each item
    max_len = len(title)
    for thing in object_list:
        if len(thing) > max_len:
            max_len = len(thing)

    max_len += 2 + (is_indexed * 5)
    print_border(max_len)
    print("|" + title + " " * (max_len - len(title)) + "|")
    print_border(max_len)

    if not is_indexed:
        for thing in object_list:
            print("|" + thing + " " * (max_len - len(thing)) + "|")
    else:
        for i in range(len(object_list)):
            print("|" + f" [{i}] " + object_list[i] + " " * (max_len - len(object_list[i]) - 5) + "|")

    print_border(max_len)


def print_favs(list_of_favs):  # TODO remove global dependence
    clear_screen()
    current_favs = concat_dict_key_values_to_string(list_of_favs)
    if current_favs:
        print_table(current_favs, "Favourites")
    else:
        print("No favourites currently saved")


def print_round(round_to_print):
    if round_to_print:
        if len(round_to_print.get_orders()) != 0:
            print(round_to_print.get_orders())
        else:
            print("No one in order!")


def add_item(object_list, object_type):  # TODO clean, add drink description?
    to_add = input(f"Please enter a name to add to the list of {object_type} (leave blank to cancel): ")
    clear_screen()
    new_items = []
    while to_add != "":
        if to_add != "":
            if object_type == "people":
                added_to_db = store.save_new_person_to_db(to_add)
            else:
                added_to_db = store.save_new_drink_to_db(to_add)
            if added_to_db:
                new_items.append(to_add)
                print(to_add + " has been added to the list")
                print("Here's the new list:")
                print_table(object_list + new_items, object_type)
                to_add = input(f"Continue typing to add more {object_type} (Leave blank to cancel): ")
                clear_screen()
            else:
                print(f"{to_add} has not been added tot he list! please try again, or lave blank to cancel")
    return object_list + new_items


def remove_item(object_list, object_type):
    new_list = object_list
    to_rem = enter_integer("Which entry would you like to remove (Leave blank to cancel)? ",
                           "Entry not recognized! Nothing removed from list\n")
    while to_rem != "":
        if to_rem in range(len(new_list)):
            clear_screen()
            new_list.remove(new_list[to_rem])
            print(str(to_rem) + " has been removed from the list")
            print("Here's the new list:")
            print_table(new_list, object_type, True)
        else:
            print("Entry not recognized! Nothing removed from list\n")
            print_table(new_list, object_type, True)

        to_rem = enter_integer("Which entry would you like to remove (Leave blank to cancel)? ",
                               "Entry not recognized! Nothing removed from list\n")
        clear_screen()
    return new_list


def choose_item(object_list, object_type,
                input_message="Please select an option from the list (Leave blank to cancel): ",
                error_message="I can't find that item in the list sorry! Please try again (leave blank to cancel): "):
    print_table(object_list, object_type, True)
    chosen_item = enter_integer(input_message, "Please enter a number! ")

    while chosen_item != "":
        if chosen_item not in range(len(object_list)):
            clear_screen()
            print(error_message)
            print_table(object_list, object_type, True)
            chosen_item = enter_integer(input_message, "Please enter a number! ")
        else:
            return chosen_item

    return chosen_item


def update_round_drinks(drinks_list, current_round):
    clear_screen()
    print("Whose drink would you like to change? ")
    people = []
    for name in current_round.get_orders().keys():
        people.append(name)
    to_update = choose_item(people, "People")
    clear_screen()
    if to_update != menu_exit_value:
        val = choose_item(drinks_list, "Drinks")
        if val != menu_exit_value:
            current_round.update_drink(drinks_list[val], people[to_update])
            store.update_db_round_persons_drink(drinks_list[val], current_round.get_round_id(), people[to_update])


def remove_person_from_round(current_round):
    clear_screen()
    print("Who do you want to remove from the round? ")
    people = []
    for name in current_round.get_orders().keys():
        people.append(name)
    to_remove = choose_item(people, "People")
    clear_screen()
    if to_remove != menu_exit_value:
        current_round.remove_person_from_round(people[to_remove])


# ***************************************************************
# Menus
# ****************************************************************

def main_menu(drinks_list, names_list, favs_list, active_round_dict):
    choice = -1
    print_menu(menu1)

    while choice != menu_exit_value:
        choice = enter_integer("Choice: ", "I don't recognize that choice sorry!")

        if choice == 0:  # Show People
            clear_screen()
            print_table(names_list, "People")
            print_menu(menu1, True)

        elif choice == 1:  # Show drinks
            clear_screen()
            print_table(drinks_list, "Drinks")
            print_menu(menu1, True)

        elif choice == 2:  # Add people
            clear_screen()
            print("Current list: ")
            print_table(names_list, "People")
            names_list = add_item(names_list, "people")
            for list_person in names_list:
                if list_person not in favs_list.keys():
                    favs_list[list_person] = ""
            print_menu(menu1, True)

        elif choice == 3:  # Add drinks
            clear_screen()
            print("Current list: ")
            print_table(drinks_list, "Drinks")
            drinks_list = add_item(drinks_list, "drinks")
            print_menu(menu1, True)

        elif choice == 4:  # remove people
            clear_screen()
            print("Current list: ")
            print_table(names_list, "People", True)
            names_list = remove_item(names_list, "People")
            for list_person in favs_list.keys():  # don't forget to remove their favourite!
                if list_person not in names_list:
                    favs_list[list_person] = ""
            store.json_save("favs.txt", favs_list)
            print_menu(menu1)

        elif choice == 5:  # remove drinks
            clear_screen()
            print("Current list: ")
            print_table(drinks_list, "Drinks", True)
            drinks_list = remove_item(drinks_list, "Drinks")
            for name, favourite_drink in favs_list.items():  # remove this drink from all favourites too!
                if favourite_drink not in drinks_list:
                    favs_list[name] = ""
            store.json_save("favs.txt", favs_list)
            print_menu(menu1)

        elif choice == 6:  # all favourite options currently
            favourites_menu(names_list, drinks_list, favs_list)  # TODO use database

        elif choice == 7:  # Rounds stuff
            if len(active_round_dict) == 0:
                print("There is currently no active round! Creating a new round!")
                input("")
                clear_screen()
                new_brewer = choose_item(names_list, "People", "Please choose wo will be making the round "
                                                               "(leave blank to cancel)")
                if new_brewer == "":
                    print("No one selected, press enter to return to main menu")
                    input("")
                    clear_screen()
                    print_menu(menu1)
                else:
                    new_brewer_fav = favs_list[names_list[new_brewer]]
                    if not new_brewer_fav:
                        new_brewer_fav = "no fav"
                    new_round_id = store.save_new_round_to_db_from_id(names_list[new_brewer], new_brewer_fav)[1]
                    print(f"{names_list[new_brewer]} has been selected to make this round. press enter to go to the "
                          f"edit round menu")
                    input("")
                    active_round_dict[new_round_id] = new_brewer_fav
                    new_round = Round(names_list[new_brewer], new_round_id, {names_list[new_brewer]: new_brewer_fav})
                    round_menu(drinks_list, names_list, new_round, favs_list)
            else:
                select_a_round(active_round_dict, drinks_list, names_list, favs_list)
            active_round_dict = load_active_rounds()

        elif choice == menu_exit_value:  # exit
            print("Thank you for using brIW!\nGoodbye!")

        else:  # Anything else
            print("Sorry, I don't recognise that choice! Please try again")


def favourites_menu(names_list, drinks_list, favs_list):
    clear_screen()
    print_favs(favs_list)
    fav_choice_name = choose_item(names_list, "People")
    while fav_choice_name != "":
        clear_screen()

        if favs_list[names_list[fav_choice_name]] != "":
            print(
                f"{names_list[fav_choice_name]} already has {favs_list[names[fav_choice_name]]} as their favourite "
                f"drink, this will overwrite that!")
        fav_choice_drink = choose_item(drinks_list, "Drinks")

        if fav_choice_drink != "":
            favs[names_list[int(fav_choice_name)]] = drinks_list[int(fav_choice_drink)]

        store.json_save("favs.txt", favs)  # TODO new saving method
        print_favs(favs_list)
        fav_choice_name = choose_item(names_list, "People")

    print_favs(favs_list)
    print_menu(menu1, True)


def new_round_or_active_round():
    print("1 new round")
    # create_new_round()
    print("2 old round")
    # select_a_round()
    pass


def select_a_round(rounds_dict, drinks_list, names_list, favourite_list):
    rounds_list = []
    for key, value in rounds_dict.items():
        rounds_list.append([key, value])
    print_table(concat_dict_key_values_to_string(rounds_dict), "Brewers!", True)
    to_rem = enter_integer("Which round do you want to edit/close? (leave blank to cancel) ",
                           "Entry not recognized! try again!\n")
    while to_rem != "":
        if to_rem in range(len(concat_dict_key_values_to_string(rounds_dict))):
            clear_screen()
            db_loaded_round = store.load_some_rows_active_columns_from_db(["user_id", "drink_id"],
                                                                          "round",
                                                                          "round_id",
                                                                          rounds_list[to_rem][0])
            loaded_round_orders = {}
            for row in db_loaded_round:
                loaded_round_orders[row[0]] = row[1]
            round_to_pass = Round(rounds_list[to_rem][1], rounds_list[to_rem][0], loaded_round_orders)
            round_menu(drinks_list, names_list, round_to_pass, favourite_list)
            return True
        else:
            print("Entry not recognized! Please choose an item from the list\n")
            print_table(concat_dict_key_values_to_string(rounds_dict), "Brewers!", True)

        to_rem = enter_integer("Which round do you want to edit/close? (leave blank to cancel) ",
                               "Entry not recognized! try again!\n")
        clear_screen()
    return False


def round_menu(drinks_list, names_list, current_round, favourite_list):
    # TODO add remove people menu option
    clear_screen()
    print_round(current_round)
    print_menu(menu3, True)
    choice = 0

    while choice != menu_exit_value:
        choice = enter_integer("Please type your selection: ", "I don't recognize that choice sorry!")

        if choice == 0:  # Add People
            val = choose_item(names_list, "People")
            if val != "":
                if not current_round.is_person_in_round(names_list[val]):
                    store.add_person_to_round(current_round, names_list[val], favourite_list[names_list[val]])
                current_round.add_person(names_list[val], favourite_list[names_list[val]])
            clear_screen()
            store.json_save("saved_round.txt", current_round.class_dict_to_save())
            print(current_round.get_orders())
            print_menu(menu3, True)

        elif choice == 1:  # Remove people
            remove_person_from_round(current_round)
            clear_screen()
            store.json_save("saved_round.txt", current_round.class_dict_to_save())
            print(current_round.get_orders())
            print_menu(menu3, True)

        elif choice == 2:  # Edit drinks
            update_round_drinks(drinks_list, current_round)
            clear_screen()
            store.json_save("saved_round.txt", current_round.class_dict_to_save())
            print(current_round.get_orders())
            print_menu(menu3, True)

        elif choice == 3:  # Print round
            clear_screen()
            print(current_round.get_orders())
            print_menu(menu3, True)

        elif choice == 4:  # Close round
            clear_screen()
            store.update_db_row_value("round", "round_id", current_round.get_round_id(), "active", 0)
            choice = menu_exit_value
            input("Press enter to return to the main menu.")

        else:
            print("That option is not in the list!")

        clear_screen()
        print_round(current_round)
        print_menu(menu3, True)

    clear_screen()
    print_menu(menu1, False)


# TODO refactor so these aren't required - pass all data?
def load_names_from_db():
    names_from_db = store.load_all_active_from_db("people")
    names_to_return = []
    for person in names_from_db:
        names_to_return.append(str(person[1]).strip())
    return names_to_return


def load_drinks_from_db():
    drinks_from_db = store.load_all_active_from_db("drinks")
    drinks_to_return = []
    for drink in drinks_from_db:
        drinks_to_return.append(drink[1])
    return drinks_to_return


def load_favs_from_db():
    favs_from_db = store.load_active_column_from_left_join(["people.full_name", "drinks.drink_name"],
                                                           "people", "drinks", "people.favourite_drink_id",
                                                           "drinks.drink_id")
    favs_to_return = {}
    for item in favs_from_db:
        if item[1]:
            favs_to_return[str(item[0]).strip()] = item[1]
        else:
            favs_to_return[str(item[0]).strip()] = ""
    return favs_to_return

def load_active_rounds():
    active_rounds = {}
    rounds_from_db = store.load_all_active_from_db("round")
    for row in rounds_from_db:
        active_rounds[row[0]] = row[4]
    return active_rounds


names = load_names_from_db()
drinks = load_drinks_from_db()
favs = load_favs_from_db()
active_rounds = load_active_rounds()

menu_exit_value = ""

menu1 = menu.Menu(["View People", "View Drinks", "Add People", "Add Drinks", "Remove People", "Remove Drinks",
                   "Update Favourites", "Update Round"])

menu2 = menu.Menu(["Add/Update a favourite"])

menu3 = menu.Menu(["Add people", "Remove people", "Update drinks", "Get current order", "End current round"])

# ***************************************************************
# Main App Function
# ****************************************************************


def run_briw():
    if len(arguments) != 1:  # If there are any arguments just run those and skip the rest
        for arg in arguments[1:]:

            if arg == "get-people":
                print_table(names, "People")

            elif arg == "get-drinks":
                print_table(drinks, "Drinks")

            elif arg == "get-favourites":
                print_table(concat_dict_key_values_to_string(favs), "Favourites")

            else:
                print("Argument not recognized: ", arg)

    else:  # Otherwise open the application in UI mode
        main_menu(drinks, names, favs, active_rounds)


if __name__ == "__main__":
    run_briw()
