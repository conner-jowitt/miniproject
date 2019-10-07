from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from connection import create_db_connection
import store


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


def html_results(list_to_print):
    html_list = "        <ul>\n"
    for item in list_to_print:
        html_list += f"            <li>{item}</li>\n"
    html_list += "        </ul>\n"
    return html_list


def list_from_dict(dict_to_list, key_for_list):
    list_to_return = []
    for i in range(len(dict_to_list)):
        list_to_return.append(dict_to_list[i+1][key_for_list])
    return list_to_return


class PersonHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        self._set_headers()
        path = self.path.split('/')
        path = path[1]
        html_page_top = """<!doctype html>
<html>
    <body>
        """
        html_page_bottom = """    </body>
</html>
        """
        list_items = ""
        if path == "":
            list_items = "Please go to <a href=./rounds>/rounds</a> for rounds, <a href=./people>/people</a>"
            list_items += " for people info, or <a href=./drinks>/drinks</a> for drinks information."
            webpage = html_page_top + "<h1>Menu</h1>"  + list_items + html_page_bottom
            self.wfile.write(webpage.encode('utf-8'))
        elif path == "people":            
            people = store.load_all_from_db("people")
            people_dict = return_json(["person_id", "full_name", "favourite_drink_id", "active"], people)
            list_items = html_results(list_from_dict(people_dict, "full_name"))
            webpage = html_page_top + "<h1>people</h1>"  + list_items + html_page_bottom
            self.wfile.write(webpage.encode('utf-8'))
        elif path == "drinks":
            drinks = store.load_all_from_db("drinks")
            drinks_dict = return_json(["drink_id", "drink_name", "drink_description", "active"], drinks)
            list_items = html_results(list_from_dict(drinks_dict, "drink_name"))
            webpage = html_page_top + "<h1>drinks</h1>\n"  + list_items + html_page_bottom
            self.wfile.write(webpage.encode('utf-8'))
        elif path == "rounds":
            rounds = store.load_all_from_db("round")
            rounds_dict = return_json(["round_id", "user_id", "drink_id", "active", "brewer_id"], rounds)
            brewer_round_list = []
            for row in rounds:
                brewer_round_list.append(str(row[0]) + " - " + str(row[4]))
            brewer_round_list = list(set(brewer_round_list))
            list_items = html_results(brewer_round_list)
            webpage = html_page_top + "<h1>rounds</h1>"  + list_items + html_page_bottom
            self.wfile.write(webpage.encode('utf-8'))
        else:
            pass


if __name__ == "__main__":
    server_address = ('0.0.0.0', 8081)
    httpd = HTTPServer(server_address, PersonHandler)
    print("Starting server")
    
    httpd.serve_forever()
