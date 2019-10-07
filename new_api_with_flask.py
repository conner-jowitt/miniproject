from flask import Flask, jsonify, request, render_template, redirect
import store

app = Flask(__name__)


# ****************************************************************
# * Functions
# ****************************************************************


def clean_input(user_input):
    special_chars = "%&£$^!()*+=~[]{}/?<>,.`,;:@#'\"\\"
    user_input = user_input.strip((special_chars + " "))
    result = ""
    for char in user_input:
        if char not in special_chars:
            result += char
    return result


def return_json(column_headers, db_rows):
    if len(column_headers) != len(db_rows[0]):
        raise Exception
    else:
        return_dict = {}
        for i in range(len(db_rows)):
            return_dict[i+1] = {}
            for j in range(len(column_headers)):
                return_dict[i+1][column_headers[j]] = db_rows[i][j]

    return return_dict


# ****************************************************************
# * Website contents pages
# ****************************************************************


@app.route("/", methods=["GET"])
def home_page():
    return {"/favourites": "View or update favourites",
            "/rounds": "Create a new round or add people to an open round",
            "/api": {"/people": "lists all people, even those that aren't active",
                     "/people-a": "lists only active people",
                     "/drinks": "lists all drinks, even those which aren't active",
                     "/drinks-a": "lists only active drinks",
                     "/rounds": "lists all rounds, even those which aren't active",
                     "/rounds-a": "lists only active rounds"}
            }


@app.route("/api", methods=["GET"])
def api_page():
    return {"/people": "lists all people, even those that aren't active",
            "/people-a": "lists only active people",
            "/drinks": "lists all drinks, even those which aren't active",
            "/drinks-a": "lists only active drinks",
            "/rounds": "lists all rounds, even those which aren't active",
            "/rounds-a": "lists only active rounds"
            }


# ****************************************************************
# * Website main user pages
# ****************************************************************


@app.route("/people", methods=["GET", "POST"])
def update_people():
    # TODO actual page
    if request.method == "GET":
        people = store.load_all_from_db("people")
        people_list = []
        if people:
            for person in people:
                people_list.append(person[1])
        return render_template("people_page.html", person="  none  ")

    # TODO add person to DB, and favourite drink, reload GET page
    # TODO make sure everything is active when already in DB
    # TODO actual errors
    if request.method == "POST":
        person_name = clean_input(request.form.get("input_name")).lower()

        if not person_name:
            return {"you": "messed up"}
        
        if store.is_in_db("people", "full_name", person_name):
            # person is in db already, check they're active & reactivate if not?
            return {}
        else:
            store.save_new_person_to_db(person_name)
            store.update_db_row_value("people", "full_name", person_name, "favourite_drink_id", 1)
            return render_template("people_page.html", person=person_name.capitalize())

    else:
        return "Hello World!"


@app.route("/drinks", methods=["GET", "POST"])
def update_drinks():
    # TODO actual page
    if request.method == "GET":
        drinks = store.load_all_from_db("drinks")
        drinks_list = []
        if drinks:
            for item in drinks:
                drinks_list.append([item[1], item[2]])
        return render_template("drinks_page.html", drinks=drinks_list)

    # TODO add person to DB, and favourite drink, reload GET page
    # TODO make sure everything is active when already in DB
    # TODO actual errors
    if request.method == "POST":
        person_name = clean_input(request.form.get("input_name")).lower()

        if not person_name:
            return {"you": "messed up"}
        
        if store.is_in_db("people", "full_name", person_name):
            # person is in db already, check they're active & reactivate if not?
            return {}
        else:
            store.save_new_person_to_db(person_name)
            store.update_db_row_value("people", "full_name", person_name, "favourite_drink_id", 1)
            return render_template("people_page.html", person=person_name.capitalize())

    else:
        return "Hello World!"


@app.route("/favourites", methods=["GET", "POST"])
def update_favourites():
    if request.method == "GET":
        return render_template("favourites_page.html")
    

    elif request.method == "POST":
        person_name = clean_input(request.form.get("input_name")).lower()
        drink_name = clean_input(request.form.get("input_drink")).lower()
        if not drink_name:
            person_id = store.get_person_id_from_name(person_name)
            if not person_id:
                return {"you": "messed up"}
            person_fav_id = store.load_some_rows_active_columns_from_db(["favourite_drink_id"], "people", "person_id", person_id)[0][0]
            drink_name = store.load_some_rows_active_columns_from_db(["drink_name"], "drinks", "drink_id", person_fav_id)[0][0]
            return render_template("display_fav_drink.html", person=person_name.capitalize(), drink=drink_name)

        else:
            drinks = store.load_some_rows_active_columns_from_db(["drink_id"], "drinks", "drink_name", drink_name)
            if drinks:
                input_drink_id = drinks[0][0]
            else:
                return {"you": "messed up!"}
            person = store.load_some_rows_active_columns_from_db(["person_id"], "people", "full_name", person_name)            
            if person:
                store.update_db_row_value("people", "full_name", person_name, "favourite_drink_id", input_drink_id)
                return render_template("display_fav_drink.html", person=person_name.capitalize(), drink=drink_name)
            else:
                return {"you": "messed up!"}

    else:
        return "Hello World"


@app.route("/rounds", methods=["GET", "POST"])
def update_round():
    # TODO better errors!
    # TODO refactor, split into functions for easier reading/updating?
    if request.method == "GET":
        active_rounds = store.load_all_active_from_db("round")
        if active_rounds:
            orders = []
            brewer = store.get_person_name_from_id(active_rounds[0][4])
            brewer = brewer.capitalize()
            for row in active_rounds:
                person = store.get_person_name_from_id(row[1]).capitalize()
                drink = store.get_drink_name_from_id(row[2])
                orders.append([person, drink])
            return render_template("display_round_data.html", round=orders, brewer=brewer)
        else:
            return render_template("display_round_data.html", brewer="none")

    elif request.method == "POST":
        person_name = clean_input(request.form.get("input_name")).lower()
        drink_name = clean_input(request.form.get("input_drink")).lower()
        
        person_id = store.get_person_id_from_name(person_name)
        
        if not person_id:
            return {"you": "messed up"}        

        if not drink_name:
            person_id = store.get_person_id_from_name(person_name)
            person_fav_id = store.load_some_rows_active_columns_from_db(["favourite_drink_id"], "people", "person_id", person_id)[0][0]
            drink_name = store.load_some_rows_active_columns_from_db(["drink_name"], "drinks", "drink_id", person_fav_id)[0][0]

        active_rounds = store.load_all_active_from_db("round")
        if active_rounds:
            brewer = store.get_person_name_from_id(active_rounds[0][4])
            brewer = brewer.capitalize()
            orders = []
            for row in active_rounds:
                person = store.get_person_name_from_id(row[1]).capitalize()
                drink = store.get_drink_name_from_id(row[2])
                orders.append([person, drink])
            if not store.is_active_in_db("drinks", "drink_name", drink_name):
                return {"you": "messed up!"}
            elif store.is_active_in_db("people", "full_name", person_name):
                people_in_round = []
                for row in active_rounds:
                    people_in_round.append(int(row[1]))
                if int(person_id) in people_in_round:
                    drink_id = store.get_drink_id_from_name(drink_name)
                    store.update_db_row_value("round", "user_id", person_id, "drink_id", drink_id)
                    for order in orders:
                        if person_name.capitalize() == order[0]:
                            order[1] = drink_name
                    return render_template("display_round_data.html", round=orders, brewer=brewer)
                else:
                    person_id = store.get_person_id_from_name(person_name)
                    drink_id = store.get_drink_id_from_name(drink_name)
                    store.add_person_to_round_from_round_id(active_rounds[0][0], person_id, drink_id)
                    orders.append([person_name.capitalize(), drink_name])
                    return render_template("display_round_data.html", round=orders, brewer=brewer)
            else:
                return {"you": "messed up!"}
        else:
            store.save_new_round_to_db_from_name(person_name, drink_name)
            orders = [[person_name.capitalize(), drink_name]]
            return render_template("display_round_data.html", round=orders, brewer=person_name.capitalize())
    else:
        return "Hello World"


@app.route("/clearround", methods=["POST"])
def clear_round():
    store.update_db_row_value("round", "active", 1, "active", 0)
    return redirect("/rounds", code=302)


# ****************************************************************
# * API pages
# ****************************************************************


@app.route("/api/people")
def get_people():
    people = store.load_all_from_db("people")
    if people:
        people_dict = return_json(["person_id", "full_name", "favourite_drink_id", "active"], people)
        return people_dict
    else:
        return {}


@app.route("/api/people-a")
def get_active_people():
    people = store.load_all_active_from_db("people")
    if people:
        people_dict = return_json(["person_id", "full_name", "favourite_drink_id", "active"], people)
        return people_dict
    else:
        return {}


@app.route("/api/drinks")
def get_drinks():
    drinks = store.load_all_from_db("drinks")
    if drinks:
        drinks_dict = return_json(["drink_id", "drink_name", "drink_description", "active"], drinks)
        return drinks_dict
    else:
        return {}


@app.route("/api/drinks-a")
def get_active_drinks():
    drinks = store.load_all_active_from_db("drinks")
    if drinks:
        drinks_dict = return_json(["drink_id", "drink_name", "drink_description", "active"], drinks)
        return drinks_dict
    else:
        return {}


@app.route("/api/rounds")
def get_rounds():
    rounds = store.load_all_from_db("round")
    if rounds:
        rounds_dict = return_json(["round_id", "user_id", "drink_id", "active", "brewer_id"], rounds)
        brewer_and_round_dict = {}
        for i in range(len(rounds_dict)):
            brewer_and_round_dict[rounds_dict[i+1]["round_id"]] = {}
        for i in range(len(rounds_dict)):
            brewer_and_round_dict[rounds_dict[i+1]["round_id"]]["brewer_id"] = rounds_dict[i+1]["brewer_id"]
            brewer_and_round_dict[rounds_dict[i+1]["round_id"]][rounds_dict[i+1]["user_id"]] = rounds_dict[i+1]["drink_id"]
        return brewer_and_round_dict
    else:
        return {}


@app.route("/api/rounds-a")
def get_active_rounds():
    rounds = store.load_all_active_from_db("round")
    if rounds:
        rounds_dict = return_json(["round_id", "user_id", "drink_id", "active", "brewer_id"], rounds)
        brewer_and_round_dict = {}
        for i in range(len(rounds_dict)):
            brewer_and_round_dict[rounds_dict[i+1]["round_id"]] = {}
        for i in range(len(rounds_dict)):
            brewer_and_round_dict[rounds_dict[i+1]["round_id"]]["brewer_id"] = rounds_dict[i+1]["brewer_id"]
            brewer_and_round_dict[rounds_dict[i+1]["round_id"]][rounds_dict[i+1]["user_id"]] = rounds_dict[i+1]["drink_id"]
        return brewer_and_round_dict
    else:
        return {}


# ****************************************************************
# * Main loop
# ****************************************************************


if __name__ == "__main__":
    app.run(host="0.0.0.0")
