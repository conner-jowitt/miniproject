import json
import sys
from connection import create_db_connection
from round import *

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


def save_new_round_to_db(round_brewer, brewer_fav):
    max_id = run_db_get_command(f"SELECT MAX(round_id) FROM round;", "Error reading data from server!\n" +
                                "function: load_active_column_from_DB\n" +
                                "when trying to get max_id")

    if type(max_id[0][0]) != type(0):
        max_id = [[0, 0],0]

    command = f"INSERT INTO round (round_id, user_id, drink_id, brewer_id, active)" + \
              f" VALUES ({max_id[0][0] + 1}, '{round_brewer}', '{brewer_fav}', '{round_brewer}', 1);"
    errors = run_db_set_command(command, "Error saving data to server!\nfunction: save_new_round_to_db\n" +
                                     "When creating new row with command:\n" +
                                     command)

    result = True
    result = (result and errors)

    return [result, max_id[0][0]+1]


def add_person_to_round(passed_round, new_person, new_drink):
    round_id = passed_round.get_round_id()
    round_brewer = passed_round.get_brew_maker()

    command = f"INSERT INTO round (round_id, brewer_id, user_id, drink_id, active)" + \
              f" VALUES ({round_id}, '{round_brewer}', '{new_person}', '{new_drink}', 1);"
    errors = run_db_set_command(command, "Error saving data to server!\nfunction: add_person_to_round\n" +
                                     "When creating new row with command:\n" +
                                     command)

    result = True
    result = (result and errors)

    return result


def load_all_from_db(table):
    results = run_db_get_command(f"SELECT * FROM {table};",
                                 "Error reading data from server!\nfunction: load_all_from_DB")
    return results


def load_all_active_from_db(table):
    results = run_db_get_command(f"SELECT * FROM {table} WHERE active=1;",
                                 "Error reading data from server!\nfunction: load_all_active_from_DB")
    return results


def load_some_rows_active_columns_from_db(columns, table, column_to_match, row_value_to_match, active_table=""):
    select_string = ""
    for item in columns:
        select_string += item + ", "
    select_string = select_string[:-2]
    if active_table:
        active_table += "."
    command = f"SELECT {select_string} FROM {table} WHERE {active_table}active=1 AND {column_to_match}='{row_value_to_match}';"
    results = run_db_get_command(command, "Error reading data from server!\nfunction: load_active_column_from_DB\n" +
                                 "When running command:\n" +
                                 command)
    return results


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


def load_active_column_from_join(columns, table1, table2, table1_join_column, table2_join_column):
    table = f"{table1} INNER JOIN {table2} ON {table1_join_column}={table2_join_column}"
    return load_active_columns_from_db(columns, table, table1)


def load_active_column_from_left_join(columns, table1, table2, table1_join_column, table2_join_column):
    table = f"{table1} LEFT JOIN {table2} ON {table1_join_column}={table2_join_column}"
    return load_active_columns_from_db(columns, table, table1)


def save_new_person_to_db(name_to_save):
    results = run_db_get_command(f"SELECT * FROM people WHERE full_name='{name_to_save}';",
                                 "Error reading data from server!\nfunction: save_person_to_db")
    if results:
        print("a person with that name already exists")
        return False
    else:
        save_to_new_db_row("people", ["person_id", "full_name", "active"], ["", name_to_save, 1])
        return True


def save_new_drink_to_db(drink_name, drink_description=""):
    results = run_db_get_command(f"SELECT * FROM drinks WHERE drink_name='{drink_name}';",
                                 "Error reading data from server!\nfunction: save_new_drink_to_db. Command:\n" +
                                 f"SELECT * FROM drinks WHERE drink_name='{drink_name}';")
    if results:
        print("A drink with that name already exists")
        return False
    else:
        save_to_new_db_row("drinks", ["drink_id", "drink_name", "drink_description", "active"],
                           ["", drink_name, drink_description, 1])
        return True


def save_to_new_db_row(table, columns, values):
    if (len(columns) != len(values)) or (len(columns) == 0):
        print("Error! column/value mismatch, please ensure the passed lists are of equal length")
        return False

    else:
        errors = []
        max_id = run_db_get_command(f"SELECT MAX({columns[0]}) FROM {table};", "Error reading data from server!\n" +
                                    "function: load_active_column_from_DB\n" +
                                    "when trying to get max_id")
        errors.append(run_db_set_command(f"INSERT INTO {table} ({columns[0]}) VALUES ({max_id[0][0] + 1});",
                                         "Error saving data to server!\nfunction: save_to_new_db_row\n" +
                                         "When creating new row with command:\n" +
                                         f"INSERT INTO {table} ({columns[0]}) VALUES ({max_id[0][0] + 1});")
                      )
        if len(columns) > 1:
            for i in range(len(columns)-1):
                errors.append(update_db_row_value(table,
                                                  columns[0],
                                                  max_id[0][0] + 1,
                                                  columns[i + 1],
                                                  values[i + 1]))
        result = True
        for res in errors:
            result = (result and res)
        return result


def update_db_row_value(table, row_id_to_change, row_id, column, value):
    return run_db_set_command(f"UPDATE {table} SET {column}='{value}' WHERE {row_id_to_change}='{row_id}';",
                              "Error saving data to server!\nupdate_db_row_value\n" +
                              "When updating new row with information. Command run:\n" +
                              f"UPDATE {table} SET {column}='{value}' WHERE {row_id_to_change}='{row_id}';")


def update_db_round_drink_row_value(table, new_drink_id, round_id, passed_name):
    command = f"UPDATE {table} SET drink_id='{new_drink_id}' WHERE round_id='{round_id}' AND user_id='{passed_name}';"
    return run_db_set_command(command,
                              "Error saving data to server!\nupdate_db_drink_row_value\n" +
                              "When updating new row with information. Command run:\n" +
                              command)


def run_db_get_command(command, error):
    db_connection = create_db_connection()
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
    db_connection = create_db_connection()
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
