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


class PersonHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    
    def do_GET(self):
        self._set_headers()
        path = self.path.split('/')
        path = path[1]
        if path == "people":
            people = store.load_all_from_db("people")
            people_dict = return_json(["person_id", "full_name", "favourite_drink_id", "active"], people)
            jd = json.dumps(people_dict)
            self.wfile.write(jd.encode('utf-8'))
        elif path == "rounds":
            rounds = store.load_all_from_db("round")
            round_dict = return_json(["round_id", "user_id", "drink_id", "active", "brewer_id"], rounds)
            jd = json.dumps(round_dict)
            self.wfile.write(jd.encode('utf-8'))
        elif path == "drinks":
            drinks = store.load_all_from_db("drinks")
            drinks_dict = return_json(["drink_id", "drink_name", "drink_description", "active"], drinks)
            jd = json.dumps(drinks_dict)
            self.wfile.write(jd.encode('utf-8'))
        else:
            pass

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length))
        if (list(data.keys()) == ["full_name", "key"]) and (data["key"] == "123456"):
           store.save_new_person_to_db(data["full_name"])
           self.send_response(201)
        elif (list(data.keys()) == ["drink_name", "drink_description", "key"]) and (data["key"] == "123456"):
           store.save_new_drink_to_db(data["drink_name"], data["drink_description"])
           self.send_response(201)
        # elif (list(data.keys()) == ["drink_name", "drink_description", "key"]) and (data["key"] == "testpass"):
        #    store.save_new_person_to_db(data["first_name"])
        #    self.send_response(201)
        else:
            self.send_response(400)
            self.end_headers()


if __name__ == "__main__":
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, PersonHandler)
    print("Starting server")
    
    httpd.serve_forever()
