import json
import sys
#from connection import create_db_connection
from round import *
import connection

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
        print(f"There isn't a file called {file_name}, a blank file has been created")
        new_file = open(file_name, "w")
        new_file.close()
        input("")
        return []


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
        print(f"There isn't a file called {file_name}, a blank file has been created")
        with open(file_name, "w") as f:
            json.dump({}, f)
        input("")
    return result


def json_save(file_name, items):
    try:
        with open(file_name, "w") as f:
            json.dump(items, f)
    except Exception as e:
        print(e)
        input("")

# ***************************************************************
# DATABASE SAVING/LOADING FUNCTIONS
# ***************************************************************


def update_db_round_persons_drink(new_drink_id, round_id, passed_name):
    command = f"UPDATE round SET drink_id='{new_drink_id}' WHERE round_id='{round_id}' AND user_id='{passed_name}';"
    return run_db_set_command(command,
                              "Error saving data to server!\nupdate_db_drink_row_value\n" +
                              "When updating new row with information. Command run:\n" +
                              command)


def add_person_to_round_from_object(passed_round, new_person, new_drink):
    round_id = passed_round.get_round_id()
    round_brewer = passed_round.get_brew_maker()

    command = f"INSERT INTO round (round_id, brewer_id, user_id, drink_id, active)" + \
              f" VALUES ({round_id}, '{round_brewer}', '{new_person}', '{new_drink}', 1);"
    return run_db_set_command(command, "Error saving data to server!\nfunction: add_person_to_round\n" +
                              "When creating new row with command:\n" + command)


def add_person_to_round_from_round_id(round_id, new_person, new_drink):
    round_ids_and_brewers = load_some_rows_active_columns_from_db(["round_id", "brewer_id"],
                                                                  "round",
                                                                  "round_id",
                                                                  round_id)
    if round_ids_and_brewers:
        round_id_list = []
        for item in round_ids_and_brewers:
            round_id_list.append(item[0])
            if item[0] == round_id:
                round_brewer = item[1]
        if round_id not in round_id_list:
            return False
        else:
            command = f"INSERT INTO round (round_id, brewer_id, user_id, drink_id, active)" + \
                      f" VALUES ({round_id}, '{round_brewer}', '{new_person}', '{new_drink}', 1);"
            return run_db_set_command(command, "Error saving data to server!\nfunction: add_person_to_round\n" +
                                      "When creating new row with command:\n" +
                                      command)
    else:
        return False


def save_new_round_to_db_from_id(round_brewer, brewer_fav):
    max_id = get_db_max_round_id()
    if max_id:
        if type(max_id[0][0]) != type(0):
            max_id = [[0, 0], 0]

        command = f"INSERT INTO round (round_id, user_id, drink_id, brewer_id, active)" + \
                  f" VALUES ({max_id[0][0] + 1}, '{round_brewer}', '{brewer_fav}', '{round_brewer}', 1);"
        errors = run_db_set_command(command, "Error saving data to server!\nfunction: save_new_round_to_db\n" +
                                    "When creating new row with command:\n" +
                                    command)

        result = True
        result = (result and errors)

        return [result, max_id[0][0]+1]
    else:
        return False


def save_new_round_to_db_from_name(round_brewer, brewer_fav):
    person_id = get_person_id_from_name(round_brewer)
    if not person_id:
        return False
    else:
        drink_id = get_drink_id_from_name(brewer_fav)
        if not drink_id:
            return False
        else:
            return save_new_round_to_db_from_id(person_id, drink_id)


def save_new_person_to_db(name_to_save):
    command = f"SELECT * FROM people WHERE full_name='{name_to_save}';"
    results = run_db_get_command(command,
                                 "Error reading data from server!\nfunction: save_person_to_db, Command:\n" +
                                 command)
    if results:
        print("a person with that name already exists")
        return False
    else:
        return save_person_to_new_db_row(["person_id", "full_name", "active"], ["", name_to_save, 1])


def save_new_drink_to_db(drink_name, drink_description=""):
    command = f"SELECT * FROM drinks WHERE drink_name='{drink_name}';"
    results = run_db_get_command(command,
                                 "Error reading data from server!\nfunction: save_new_drink_to_db. Command:\n" +
                                 command)
    if results:
        print("A drink with that name already exists")
        return False
    else:
        return save_drink_to_new_db_row(["drink_id", "drink_name", "drink_description", "active"],
                                  ["", drink_name, drink_description, 1])


def load_active_column_from_join(columns, table1, table2, table1_join_column, table2_join_column):
    table = f"{table1} INNER JOIN {table2} ON {table1_join_column}={table2_join_column}"
    return load_active_columns_from_db(columns, table, table1)


def load_active_column_from_left_join(columns, table1, table2, table1_join_column, table2_join_column):
    table = f"{table1} LEFT JOIN {table2} ON {table1_join_column}={table2_join_column}"
    return load_active_columns_from_db(columns, table, table1)


def load_active_columns_from_db(columns, table, active_table=""):
    select_string = ""
    for item in columns:
        select_string += item + ", "
    select_string = select_string[:-2]
    if active_table:
        active_table += "."
    results = run_db_get_command(f"SELECT {select_string} FROM {table} WHERE {active_table}active=1;",
                                 "Error reading data from server!\nfunction: load_active_column_from_DB")
    return results


def save_drink_to_new_db_row(columns, values):
    if (len(columns) != len(values)) or (len(columns) == 0):
        return False

    else:
        errors = []
        max_id = get_db_max_drink_id()
        if max_id:
            errors.append(make_new_db_row("drinks", columns[0], max_id[0][0]+1))
            if len(columns) > 1:
                errors.append(update_db_row_multiple_columns("drinks", columns[0], max_id[0][0]+1, columns[1:], values[1:]))
            result = True
            for res in errors:
                result = (result and res)
            return result
        else:
            return False


def save_person_to_new_db_row(columns, values):
    if (len(columns) != len(values)) or (len(columns) == 0):
        return False

    else:
        errors = []
        max_id = get_db_max_person_id()
        if max_id:
            errors.append(make_new_db_row("people", columns[0], max_id[0][0]+1))
            if len(columns) > 1:
                errors.append(update_db_row_multiple_columns("people", columns[0], max_id[0][0]+1, columns[1:], values[1:]))
            result = True
            for res in errors:
                result = (result and res)
            return result
        else:
            return False


def save_to_new_db_row(table, columns, values):
    if (len(columns) != len(values)) or (len(columns) == 0):
        return False

    else:
        errors = []
        max_id = get_db_max_round_id()
        if max_id:
            errors.append(make_new_db_row(table, columns[0], max_id[0][0]+1))
            if len(columns) > 1:
                errors.append(update_db_row_multiple_columns(table, columns[0], max_id[0][0]+1, columns[1:], values[1:]))
            result = True
            for res in errors:
                result = (result and res)
            return result
        else:
            return False


def update_db_row_multiple_columns(table, column_to_match, column_key_to_match, columns_to_update, new_column_values):
    if len(columns_to_update) != len(new_column_values):
        return False
    else:
        errors = []
        for i in range(len(columns_to_update)):
            errors.append(update_db_row_value(table, column_to_match,
                                              column_key_to_match,
                                              columns_to_update[i],
                                              new_column_values[i])
                          )
    result = True
    for error in errors:
        result = result and error
    return result


def load_some_rows_active_columns_from_db(columns, table, column_to_match, row_value_to_match): # Tested
    select_string = ""
    for item in columns:
        select_string += item + ", "
    select_string = select_string[:-2]
    command = f"SELECT {select_string} FROM {table} WHERE active=1" \
              f" AND {column_to_match}='{row_value_to_match}';"
    return run_db_get_command(command,
                              "Error reading data from server!\nfunction: load_active_column_from_DB\n" +
                              "When running command:\n" + command)


def load_rows_matching_single_column_value(table, column_to_match, row_value_to_match):
    command = f"SELECT * FROM {table} WHERE active=1 AND {column_to_match}='{row_value_to_match}';"
    return run_db_get_command(command,
                              "Error reading data from server!\nfunction: load_rows_matching_single_column_value\n" +
                              "When running command:\n" + command)


def update_db_row_value(table, row_id_to_change, row_id, column, value): # Tested
    command = f"UPDATE {table} SET {column}='{value}' WHERE {row_id_to_change}='{row_id}';"
    return run_db_set_command(command,
                              "Error saving data to server!\nupdate_db_row_value\n" +
                              "When updating new row with information. Command run:\n" +
                              command)


def make_new_db_row(table, id_column_name, id_for_new_row):
    command = f"INSERT INTO {table} ({id_column_name}) VALUES ({id_for_new_row});"
    return run_db_set_command(command,
                              "Error saving data to server!\nfunction: save_to_new_db_row\n" +
                              "When creating new row with command:\n" +
                              command)


def load_all_active_from_db(table):
    results = run_db_get_command(f"SELECT * FROM {table} WHERE active=1;",
                                 "Error reading data from server!\nfunction: load_all_active_from_DB")
    return results


def load_all_from_db(table):
    command = f"SELECT * FROM {table};"
    return run_db_get_command(command, "Error reading data from server!\nfunction: load_all_from_DB")


def get_db_max_round_id():
    command = f"SELECT MAX(round_id) FROM round;"
    return run_db_get_command(command, "Error reading data from server!\n" +
                              "when trying to get max_id with command:" +command)


def get_db_max_person_id():
    command = "SELECT MAX(person_id) FROM people;"
    return run_db_get_command(command, "Error reading data from server!\n" +
                              "when trying to get max_id with command:\n" + command)


def get_db_max_drink_id():
    command = "SELECT MAX(drink_id) FROM drinks;"
    return run_db_get_command(command, "Error reading data from server!\n" +
                              "when trying to get max_id with command:\n" + command)


def get_person_id_from_name(person_name): #Tested
    if is_active_in_db("people", "full_name", person_name):
        name_row = load_rows_matching_single_column_value("people", "full_name", person_name)
        return name_row[0][0]
    else:
        return False


def get_person_name_from_id(person_id): #Tested
    if is_active_in_db("people", "person_id", person_id):
        name_row = load_rows_matching_single_column_value("people", "person_id", person_id)
        return name_row[0][1]
    else:
        return False


def get_drink_id_from_name(drink_name): #Tested
    if is_active_in_db("drinks", "drink_name", drink_name):
        drink_row = load_rows_matching_single_column_value("drinks", "drink_name", drink_name)
        return drink_row[0][0]
    else:
        return False


def get_drink_name_from_id(drink_id): #Tested
    if is_active_in_db("drinks", "drink_id", drink_id):
        drink_row = load_rows_matching_single_column_value("drinks", "drink_id", drink_id)
        return drink_row[0][1]
    else:
        return False


def is_in_db(table, column_to_check, looking_for_value): #Tested
    result = run_db_get_command(f"SELECT * FROM {table} WHERE {column_to_check}='{looking_for_value}';",
                                "Error reading data from server!\n" +
                                "function: load_active_column_from_DB\n" +
                                "when trying to get max_id")
    if result:
        return True
    else:
        return False

def is_active_in_db(table, column_to_check, looking_for_value): # Tested
    result = run_db_get_command(f"SELECT * FROM {table} WHERE {column_to_check}='{looking_for_value}' AND active=1;",
                                "Error reading data from server!\n" +
                                "function: load_active_column_from_DB\n" +
                                "when trying to get max_id")
    if result:
        return True
    else:
        return False


def run_db_get_command(command, error):
    db_connection = connection.create_db_connection()
    cursor = db_connection.cursor()
    try:
        cursor.execute(command)
        results = cursor.fetchall()
        db_connection.close()
        return results
    except Exception:
        print(error)
        print(sys.exc_info())
        input("")
        db_connection.close()
        return False


def run_db_set_command(command, error):
    db_connection = connection.create_db_connection()
    cursor = db_connection.cursor()
    try:
        cursor.execute(command)
        db_connection.close()
        return True
    except Exception:
        print(error)
        print(sys.exc_info())
        input("")
        db_connection.close()
        return False
