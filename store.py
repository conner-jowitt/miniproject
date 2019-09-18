import json

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

