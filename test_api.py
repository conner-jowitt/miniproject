import unittest
from unittest.mock import Mock, call
from new_api_with_flask import *
import new_api_with_flask as flask_file
from store import *
import connection
import flask

class Test_Methods(unittest.TestCase):
    def setUp(self):
        self.app = flask_file.app.test_client()

    def test_clean_input_returns_empty_string_when_passed_empty_string(self):
        # Arrange
        input_string = ""
        expected = ""

        # Act
        result = clean_input(input_string)

        # Assert
        self.assertEqual(result, expected)
    
    def test_clean_input_returns_empty_string_when_passed_string_of_special_characters(self):
        # Arrange
        input_string = "!\"£$%^&*()+=[-];'#,./{}:@~<>?\\|"
        expected = ""

        # Act
        result = clean_input(input_string)

        # Assert
        self.assertEqual(result, expected)

    def test_clean_input_returns_same_string_when_passed_string_of_letters_and_numbers(self):
        # Arrange
        input_string = "skfgsorls424asdxccxzznvm8000"
        expected = input_string

        # Act
        result = clean_input(input_string)

        # Assert
        self.assertEqual(result, expected)

    def test_clean_input_returns_string_with_no_special_characters_when_passed_a_mixed_string(self):
        # Arrange
        input_string = "^;'@@@@s1!k2_3f4g|||sorls42*-/+++4asdxccxzz!nvm$8000£"
        expected = "s1k2_3f4gsorls424asdxccxzznvm8000"

        # Act
        result = clean_input(input_string)

        # Assert
        self.assertEqual(result, expected)

    def test_return_json_returns_empty_dict_when_passed_incorrect_number_of_labels(self):
        # Arrange
        passed_columns = [1,2,3]
        passed_rows = [[1, 2],
                       [1, 2],
                       [1, 2]]
        expected = {}

        # Act
        result = return_json(passed_columns, passed_rows)

        # Assert
        self.assertEqual(expected, result)

    def test_return_json_returns_indexed_dictionary_from_input(self):
        # Arrange
        passed_columns = ["first", "second", "third"]
        passed_rows = [["list1 element1", "list1 element2", "list1 element3"],
                       ["list2 element1", "list2 element2", "list2 element3"],
                       ["list3 element1", "list3 element2", "list3 element3"],
                       ["list4 element1", "list4 element2", "list4 element3"]]
        expected = {1:{"first": "list1 element1",
                       "second": "list1 element2",
                       "third": "list1 element3"},
                    2:{"first": "list2 element1",
                       "second": "list2 element2",
                       "third": "list2 element3"},
                    3:{"first": "list3 element1",
                       "second": "list3 element2",
                       "third": "list3 element3"},
                    4:{"first": "list4 element1",
                       "second": "list4 element2",
                       "third": "list4 element3"}}

        # Act
        result = return_json(passed_columns, passed_rows)

        # Assert
        self.assertEqual(expected, result)

    @unittest.mock.patch('store.get_person_name_from_id', side_effect=["joe", "alf", "fred", "alfred"])
    @unittest.mock.patch('store.get_drink_name_from_id', side_effect=["tea", "beer", "water", "tea"])
    def test_get_order_people_and_drinks_returns_list_in_correct_format(self, drink_name_func, person_name_func):
        #Arrange
        order_list = [[1, 1, 1, 1, 1], [1, 2, 2, 1, 1], [1, 3, 3, 1, 1], [1, 4, 1, 1, 1]]
        expected = [["Joe", "tea"], ["Alf", "beer"], ["Fred", "water"], ["Alfred", "tea"]]

        # Act
        result = get_order_people_and_drinks(order_list)

        # Assert
        drink_name_func.assert_has_calls([call(1), call(2), call(3), call(1)])
        person_name_func.assert_has_calls([call(1), call(2), call(3), call(4)])
        self.assertEqual(expected, result)
   
    # Testing website gets

    @unittest.mock.patch('flask.render_template')
    @unittest.mock.patch('store.load_all_from_db', return_value=[[1, "jojo", 1, 1], [2, "alf", 1, 1], [3, "alfred", 2, 1]])
    def test_update_people_get_returning_correct_page(self, load_people, returned_page):
        #Arrange

        # Act
        response = self.app.get("/people")

        # Assert
        load_people.assert_called_with("people")
        returned_page.assert_called_with("people_page.html", person="  none  ", people=["Jojo", "Alf", "Alfred"])
    
    @unittest.mock.patch('flask.render_template')
    @unittest.mock.patch('store.load_all_from_db', return_value=[[1, "tea", "refreshing tea", 1], [2, "coffee", "refreshing coffee", 1], [3, "sewer water", "refreshing sewer water", 1]])
    def test_update_drinks_get_returning_correct_page(self, load_people, returned_page):
        #Arrange

        # Act
        response = self.app.get("/drinks")

        # Assert
        load_people.assert_called_with("drinks")
        returned_page.assert_called_with("drinks_page.html", drinks=[["tea", "refreshing tea"], ["coffee", "refreshing coffee"], ["sewer water", "refreshing sewer water"]])

if __name__ == "__main__":
    unittest.main()
