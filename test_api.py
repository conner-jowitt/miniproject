import unittest
from unittest.mock import Mock
from new_api_with_flask import *
from store import *

class Test_Methods(unittest.TestCase):
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
        input_string = "!\"£$%^&*()+=[];'#,./{}:@~<>?\\|"
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
        expected = "s1k2_3f4gsorls42-4asdxccxzznvm8000"

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

if __name__ == "__main__":
    unittest.main()
