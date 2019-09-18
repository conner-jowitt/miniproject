#!/usr/bin/env python3

import sys
import os
import menu
import store

arguments = sys.argv


# ***************************************************************
# Classes
# ****************************************************************

class Round:
    def __init__(self, loaded_dict={}):
        if len(loaded_dict):
            self.brew_maker = list(loaded_dict.keys())[0]
            self.orders = loaded_dict[list(loaded_dict.keys())[0]]
        else:
            self.brew_maker = ""
            self.orders = {}

    def add_person(self, person):
        is_in = False
        for i in range(len(self.orders)):
            if person in list(self.orders.keys()):
                is_in = True
        if not is_in:
            if person in favs.keys():
                self.orders[person] = favs[person]
            else:
                self.orders[person] = ""

    def update_drink(self, drink, name):
        self.orders[name] = drink

    def end_round(self):
        orders = self.get_orders()
        self.clear_orders()
        self.brew_maker = ""
        return orders

    def get_orders(self):
        return self.orders

    def get_brew_maker(self):
        return self.brew_maker

    def new_brew_maker(self, name):
        self.brew_maker = name

    def clear_orders(self):
        self.orders = {}

    def class_dict_to_save(self):
        return {self.brew_maker: self.orders}

    def remove_person_from_round(self, name):
        if name in self.orders.keys():
            self.orders.pop(name)


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


def concat_favs(orders):  # concatenate user + favourite into a single string for ease of display
    updated_order = []
    for key, value in orders.items():
        if value != "":
            updated_order.append(key + ": " + value)
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


def print_favs():
    clear_screen()
    current_favs = concat_favs(favs)
    if current_favs:
        print_table(current_favs, "Favourites")
    else:
        print("No favourites currently saved")


def print_round(round):  # TODO rename variables to remove global dependence
    if round:
        if len(round.get_orders()) != 0:
            print(round.get_orders())
        else:
            print("No one in order!")


def add_item(object_list, object_type):
    to_add = input(f"Please enter a name to add to the list of {object_type} (leave blank to cancel): ")
    clear_screen()
    to_return = object_list
    while to_add != "":
        if to_add != "":
            to_return.append(to_add)
            print(to_add + " has been added to the list")
            print("Here's the new list:")
            print_table(to_return, object_type)
            to_add = input(f"Continue typing to add more {object_type} (Leave blank to cancel): ")
            clear_screen()
    return to_return


def remove_item(object_list, object_type):
    to_rem = enter_integer("Which entry would you like to remove (Leave blank to cancel)? ",
                           "Entry not recognized! Nothing removed from list\n")
    while to_rem != "":
        if to_rem in range(len(object_list)):
            clear_screen()
            object_list.remove(object_list[to_rem])
            print(str(to_rem) + " has been removed from the list")
            print("Here's the new list:")
            print_table(object_list, object_type, True)
        else:
            print("Entry not recognized! Nothing removed from list\n")
            print_table(object_list, object_type, True)
        to_rem = enter_integer("Which entry would you like to remove (Leave blank to cancel)? ",
                               "Entry not recognized! Nothing removed from list\n")
        clear_screen()


def choose_item(object_list, object_type,
                input_message="Please select an option from the list (Leave blank to cancel): ",
                error_message="I can't find that item in the list sorry! Please try again (leave blank to cancel): "):
    print_table(object_list, object_type, True)
    fav_choice_name = enter_integer(input_message, "Please enter a number! ")
    while fav_choice_name != "":
        if fav_choice_name not in range(len(object_list)):
            clear_screen()
            print(error_message)
            print_table(object_list, object_type, True)
            fav_choice_name = enter_integer(input_message, "Please enter a number! ")
        else:
            return fav_choice_name
    return fav_choice_name


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

def main_menu(drinks_list, names_list, favs_list, current_round):
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
            for person in names_list:
                if person not in favs_list.keys():
                    favs_list[person] = ""
            store.save_items("names.txt", names_list)
            print_menu(menu1, True)
        elif choice == 3:  # Add drinks
            clear_screen()
            print("Current list: ")
            print_table(drinks_list, "Drinks")
            drinks_list = add_item(drinks_list, "drinks")
            store.save_items("drinks.txt", drinks_list)
            print_menu(menu1, True)
        elif choice == 4:  # remove people
            clear_screen()
            print("Current list: ")
            print_table(names_list, "People", True)
            remove_item(names_list, "People")
            for person in favs_list.keys():  # don't forget to remove their favourite!
                if person not in names_list:
                    favs_list[person] = ""
            store.save_items("names.txt", names_list)
            store.json_save("favs.txt", favs_list)
            print_menu(menu1)
        elif choice == 5:  # remove drinks
            clear_screen()
            print("Current list: ")
            print_table(drinks_list, "Drinks", True)
            remove_item(drinks_list, "Drinks")
            for name, drink in favs_list.items():  # remove this drink from all favourites too!
                if drink not in drinks_list:
                    favs_list[name] = ""
            store.save_items("drinks.txt", drinks_list)
            store.json_save("favs.txt", favs_list)
            print_menu(menu1)
        elif choice == 6:  # all favourite options currently
            favourites_menu(names_list, drinks_list, favs_list)
        elif choice == 7:  # Rounds stuff
            if current_round.get_brew_maker() == "":
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
                    current_round.new_brew_maker(names_list[new_brewer])
                    print(f"{names_list[new_brewer]} has been selected to make this round. press enter to go to the "
                          f"edit round menu")
                    input("")
                    round_menu(drinks_list, names_list, current_round)
            else:
                round_menu(drinks_list, names_list, current_round)
        elif choice == menu_exit_value:  # exit
            print("Thank you for using brIW!\nGoodbye!")
        else:  # Anything else
            print("Sorry, I don't recognise that choice! Please try again")


def favourites_menu(names_list, drinks_list, favs_list):
    clear_screen()
    print_favs()
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
        store.json_save("favs.txt", favs)
        print_favs()
        fav_choice_name = choose_item(names_list, "People")
    print_favs()
    print_menu(menu1, True)


def round_menu(drinks_list, names_list, current_round):
    # TODO add remove people menu option
    clear_screen()
    print_round(current_round)
    print_menu(menu3, True)
    choice = 0
    while choice != menu_exit_value:
        choice = enter_integer("Please type your selection: ", "I don't recognize that choice sorry!")
        if choice == 0: # Add People
            val = choose_item(names_list, "People")
            if val != "":
                current_round.add_person(names_list[val])
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
        elif choice == 2: # Edit drinks
            update_round_drinks(drinks_list, current_round)
            clear_screen()
            store.json_save("saved_round.txt", current_round.class_dict_to_save())
            print(current_round.get_orders())
            print_menu(menu3, True)
        elif choice == 3: # Print round
            clear_screen()
            print(current_round.get_orders())
            print_menu(menu3, True)
        elif choice == 4: # Close round
            clear_screen()
            # TODO save metadata to allow stats? will possibly be using database anyway so may not be necessary
            orders = current_round.end_round()
            store.json_save("saved_round.txt", current_round.class_dict_to_save())
            print(orders)
            choice = menu_exit_value
            input("Press enter to return to the main menu.")
        else:
            print("That option is not in the list!")
        clear_screen()
        print_round(current_round)
        print_menu(menu3, True)
    clear_screen()
    print_menu(menu1, False)


names = store.load_items("names.txt")
drinks = store.load_items("drinks.txt")
menu_exit_value = ""
favs = store.json_load("favs.txt")
round_number = 0
saved_round = Round(store.json_load("saved_round.txt"))
menu1 = menu.Menu(["View People", "View Drinks", "Add People", "Add Drinks", "Remove People", "Remove Drinks",
                   "Update Favourites", "Update Round"])
menu2 = menu.Menu(["Add/Update a favourite"])
menu3 = menu.Menu(["Add people", "Remove people", "Update drinks", "Get current order", "End current round"])

if __name__ == "__main__":
    if len(arguments) != 1:  # If there are any arguments just run those and skip the rest
        for arg in arguments[1:]:
            if arg == "get-people":
                print_table(names, "People")
            elif arg == "get-drinks":
                print_table(drinks, "Drinks")
            elif arg == "get-favourites":
                print_table(concat_favs(favs), "Favourites")
            elif arg == "get-order":
                if saved_round.get_brew_maker() != "":
                    print_table(concat_favs(saved_round.get_orders()), "Orders")
                else:
                    print("No round in progress! \n")
            else:
                print("Argument not recognized: ", arg)
    else:  # Otherwise open the application in UI mode
        main_menu(drinks, names, favs, saved_round)
