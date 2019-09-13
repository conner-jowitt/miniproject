#!/usr/bin/env python3

import sys
import os
import json
import menu

arguments = sys.argv


# ***************************************************************
# Classes
# ****************************************************************

class Round:
    def __init__(self):
        self.orders = {}
        brew_maker = ""

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

    def add_drink(self, drink, name):
        self.orders[name] = drink

    def end_round(self):
        orders = self.get_orders()
        self.clear_orders()
        return orders

    def get_orders(self):
        return self.orders

    def clear_orders(self):
        self.orders = {}


# ***************************************************************
# Save - Load Functions
# ***************************************************************

def load_items(file_name):
    file_lines = []
    try:
        with open(file_name, "r") as open_file:
            file_data = open_file.readlines()
            for i in range(len(file_data)):
                file_lines.append(file_data[i][:-1].strip())
            return file_lines
    except FileNotFoundError:
        print(f"There isn't a file called {file_name}!")
        input("")
        quit()


def save_items(file_name, items):
    open_file = open(file_name, "w")
    for item in items:
        open_file.write(item + "\n")
    open_file.close()


def json_load(file_name):
    result = {}
    try:
        with open(file_name, "r") as f:
            result = json.load(f)
    except FileNotFoundError:
        print(f"There isn't a file called {file_name}!")
        input("")
        quit()
    return result


def json_save(file_name, items):
    try:
        with open(file_name, "w") as f:
            json.dump(items, f)
    except Exception as e:
        print(e)
        input("")


# ***************************************************************
# Other Functions
# ****************************************************************

def enter_int(message="Please enter a number: ", err="Error! That is not a number!"):
    inp = "bluh"
    while inp == "bluh":
        inp = input(message)
        if inp.isnumeric():
            return int(inp)
        elif inp == "":
            return inp
        else:
            print(err)
            inp = "bluh"


def clear_screen():
    os.system("clear")


def concat_favs(orders):  # concatenate user + favourite into a single string for ease of display
    updated_order = []
    for key, value in orders.items():
        if value != "":
            updated_order.append(key + ": " + value)
    return updated_order


def print_menu(men, clear=False):
    if not clear:
        clear_screen()
    men.print_ioptions()
    print("Leave blank to cancel")


def print_border(length=30):
    print("+" + "=" * length + "+")


def print_table(items, title, indexed=0):  # indexed = 0 or 1, when 1 prints an index for each item
    max_len = len(title)
    for thing in items:
        if len(thing) > max_len:
            max_len = len(thing)
    max_len += 2 + (indexed * 5)
    print_border(max_len)
    print("|" + title + " " * (max_len - len(title)) + "|")
    print_border(max_len)
    if indexed == 0:
        for thing in items:
            print("|" + thing + " " * (max_len - len(thing)) + "|")
    else:
        for i in range(len(items)):
            print("|" + f" [{i}] " + items[i] + " " * (max_len - len(items[i]) - 5) + "|")
    print_border(max_len)


def print_favs():
    clear_screen()
    current_favs = concat_favs(favs)
    if current_favs:
        print_table(current_favs, "Favourites")
    else:
        print("No favourites currently saved")


def print_rounds(round):
    if rounds:
        if len(rounds.get_orders()) != 0:
            print(rounds.get_orders())
        else:
            print("No one in order!")


def add_item(lists, obje):
    to_add = input(f"Please enter a name to add to the list of {obje} (leave blank to cancel): ")
    clear_screen()
    while to_add != "":
        if to_add != "":
            lists.append(to_add)
            print(to_add + " has been added to the list")
            print("Here's the new list:")
            print_table(lists, obje)
            to_add = input(f"Continue typing to add more {obje} (Leave blank to cancel): ")
            clear_screen()


def remove_item(lists, obje):
    to_rem = enter_int("Which entry would you like to remove (Leave blank to cancel)? ",
                       "Entry not recognized! Nothing removed from list\n")
    while to_rem != "":
        if to_rem in range(len(lists)):
            clear_screen()
            lists.remove(lists[to_rem])
            print(str(to_rem) + " has been removed from the list")
            print("Here's the new list:")
            print_table(lists, obje, 1)
        else:
            print("Entry not recognized! Nothing removed from list\n")
            print_table(lists, obje, 1)
        to_rem = enter_int("Which entry would you like to remove (Leave blank to cancel)? ",
                           "Entry not recognized! Nothing removed from list\n")
        clear_screen()


def choose_item(lists, obj, message="Please select an option from the list (Leave blank to cancel): ",
                err="I can't find that item in the list sorry! Please try again (leave blank to cancel): "):
    print_table(lists, obj, 1)
    fav_choice_name = enter_int(message, "Please enter a number! ")
    while fav_choice_name != "":
        if fav_choice_name not in range(len(lists)):
            clear_screen()
            print(err)
            print_table(lists, obj, 1)
            fav_choice_name = enter_int(message, "Please enter a number! ")
        else:
            return fav_choice_name
    return fav_choice_name


def add_favs(peeps, bevs):
    clear_screen()
    print_favs()
    fav_choice_name = choose_item(peeps, "People")
    while fav_choice_name != "":
        clear_screen()
        if favs[peeps[fav_choice_name]] != "":
            print(f"{peeps[fav_choice_name]} already has {favs[peeps[fav_choice_name]]} as their favourite drink, "
                  f"this will overwrite that!")
        fav_choice_drink = choose_item(bevs, "People")
        if fav_choice_drink != "":
            favs[peeps[int(fav_choice_name)]] = bevs[int(fav_choice_drink)]
        json_save("favs.txt", favs)
        print_favs()
        fav_choice_name = choose_item(peeps, "People")
    print_favs()
    print_menu(menu2, True)


# ***************************************************************
# Menus
# ****************************************************************

def main_menu():
    choice = -1
    print_menu(menu1)
    while choice != menu_exit_value:
        choice = enter_int("Choice: ", "I don't recognize that choice sorry!")
        if choice == 0:  # Show People
            clear_screen()
            print_table(names, "People")
            print_menu(menu1, True)
        elif choice == 1:  # Show drinks
            clear_screen()
            print_table(drinks, "Drinks")
            print_menu(menu1, True)
        elif choice == 2:  # Add people
            clear_screen()
            print("Current list: ")
            print_table(names, "People")
            add_item(names, "people")
            for person in names:
                if person not in favs.keys():
                    favs[person] = ""
            save_items("names.txt", names)
            print_menu(menu1, True)
        elif choice == 3:  # Add drinks
            clear_screen()
            print("Current list: ")
            print_table(drinks, "Drinks")
            add_item(drinks, "drinks")
            save_items("drinks.txt", drinks)
            print_menu(menu1, True)
        elif choice == 4:  # remove people
            clear_screen()
            print("Current list: ")
            print_table(names, "People", 1)
            remove_item(names, "People")
            for person in favs.keys():  # don't forget to remove their favourite!
                if person not in names:
                    favs[person] = ""
            save_items("names.txt", names)
            json_save("favs.txt", favs)
            print_menu(menu1)
        elif choice == 5:  # remove drinks
            clear_screen()
            print("Current list: ")
            print_table(drinks, "Drinks", 1)
            remove_item(drinks, "Drinks")
            for name, drink in favs.items():  # remove this drink from all favourites too!
                if drink not in drinks:
                    favs[name] = ""
            save_items("drinks.txt", drinks)
            json_save("favs.txt", favs)
            print_menu(menu1)
        elif choice == 6:  # all favourite options currently
            favourites_menu()
        elif choice == 7:  # Rounds stuff
            round_menu()
        elif choice == menu_exit_value:  # exit
            print("Thank you for using brIW!\nGoodbye!")
        else:  # Anything else
            print("Sorry, I don't recognise that choice! Please try again")


def favourites_menu():  # TODO think of other favourite options, if none then skip this menu to add_favs() menu
    print_favs()
    print_menu(menu2, True)
    choice = -1
    while choice != "":
        choice = enter_int("Please type your selection: ", "I don't recognize that choice sorry!")
        if choice == 0:  # edit favourites
            add_favs(names, drinks)
        elif choice == "":
            print_menu(menu1)
        else:
            print("I don't recognize that choice sorry!")


def round_menu():  # TODO refactor! skip this menu completely,not useful
    clear_screen()
    global rounds
    global round_number
    print_rounds(rounds)
    print_menu(menu3, True)
    choice = 0
    while choice != "":
        choice = enter_int("Please type your selection: ", "I don't recognize that choice sorry!")
        if choice == 0:  # close the current round and open a new one
            rounds = Round()
            rounds.clear_orders()
            round_number += 1
            if menu3.get_length() == 1:
                menu3.add_option("Edit current round")
            print("Old round has been closed, taking you to the edit menu")
            input("Press enter to proceed")
            edit_round_menu()
            print_menu(menu3)
        elif choice == 1 and rounds:  # edit the current round
            edit_round_menu()
        elif choice != "":
            print("I don't recognize that choice sorry!")
    print_menu(menu1, False)


def edit_round_menu():  # TODO refactor to include round_menu() options
    clear_screen()
    if len(rounds.get_orders()) != 0:
        print(rounds.get_orders())
    print_menu(menu4, True)
    choice = 0
    while choice != "":
        choice = enter_int("Please type your selection: ", "I don't recognize that choice sorry!")
        if choice == 0:
            val = choose_item(names, "People")
            if val != "":
                rounds.add_person(names[val])
            clear_screen()
            print(rounds.get_orders())
            print_menu(menu4, True)
        if choice == 1:
            val = choose_item(drinks, "Drinks")
            if val != "":
                clear_screen()
                print("Who do you want to add this drink to?")
                people = []
                for name in list(list(rounds.get_orders().keys())):
                    people.append(name)
                print_table(people, "Current Orderers", 1)
                to_update = choose_item(people, "People")
                if to_update != "":
                    rounds.add_drink(val, to_update)
            clear_screen()
            print(rounds.get_orders())
            print_menu(menu4, True)
        if choice == 2:
            clear_screen()
            print(rounds.get_orders())
            print_menu(menu4, True)
        if choice == 3:
            clear_screen()
            orders = rounds.end_round()
            print(orders)
            choice = ""
            input("Press enter to return to the main menu.")
            menu3.remove_option("Edit current round")
            json_save("new_order.txt", orders)
        clear_screen()
        print(rounds.get_orders())
        print_menu(menu3, True)


names = load_items("names.txt")
drinks = load_items("drinks.txt")
menu_exit_value = ""
menu2_exit_value = ""
favs = json_load("favs.txt")
round_number = 0
rounds = Round()
menu1 = menu.Menu(["View People", "View Drinks", "Add People", "Add Drinks", "Remove People", "Remove Drinks",
                   "Update Favourites", "Create Order"])
menu2 = menu.Menu(["Add/Update a favourite"])
menu3 = menu.Menu(["Create new round"])
menu4 = menu.Menu(["Add people", "Update drinks", "Get current order", "End current round"])

if len(arguments) != 1:  # If there are any arguments just run those and skip the rest
    for arg in arguments[1:]:
        if arg == "get-people":
            print_table(names, "People")
        elif arg == "get-drinks":
            print_table(drinks, "Drinks")
        else:
            print("Argument not recognized: ", arg)
else:  # Otherwise open the application in UI mode
    main_menu()
