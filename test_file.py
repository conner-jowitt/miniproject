import unittest
from brIW import *

class Test_Methods(unittest.TestCase):
    def test_concat_favs(self):
        #Arrange
        entered_values = {"this strin": "g was concat", "This string wa": "s also concat"}

        expected_outputs = ["this strin: g was concat", "This string wa: s also concat"]

        #Act
        returned_values = concat_favs(entered_values)

        #Assert
        self.assertEqual(returned_values, expected_outputs)
    def test_integer_validation_integer_entry(self):
        #Arrange
        entered_value = 1

        expected_result = 1

        #Act
        returned_value = integer_validation(entered_value)

        #Assert
        self.assertEqual(returned_value, expected_result)
    
    def test_integer_validation_integer_string_entry(self):
        #Arrange
        entered_value = "1"

        expected_result = 1

        #Act
        returned_value = integer_validation(entered_value)

        #Assert
        self.assertEqual(returned_value, expected_result)

    def test_integer_validation_blank_entry(self):
        #Arrange
        entered_value = ""

        expected_result = ""

        #Act
        returned_value = integer_validation(entered_value)

        #Assert
        self.assertEqual(returned_value, expected_result)

    def test_integer_validation_randon_string_entry(self):
        #Arrange
        entered_value = "1akfjha!"

        expected_result = "False"

        #Act
        returned_value = integer_validation(entered_value)

        #Assert
        self.assertEqual(returned_value, expected_result)

if __name__ == "__main__":
    unittest.main()
