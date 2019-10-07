import unittest
from unittest.mock import Mock
from rounds import *

class Test_Methods(unittest.TestCase):
    def test_concat_dict_key_values_to_string_returns_concatenated_strings_for_simple_dicts(self):
        # Arrange
        entered_values = {"this strin": "g was concat", "This string wa": "s also concat"}

        expected_outputs = ["this strin: g was concat", "This string wa: s also concat"]

        # Act
        returned_values = concat_dict_key_values_to_string(entered_values)

        # Assert
        self.assertEqual(returned_values, expected_outputs)
    def test_integer_validation_integer_entry(self):
        # Arrange
        entered_value = 1

        expected_result = 1

        # Act
        returned_value = integer_validation(entered_value)

        # Assert
        self.assertEqual(returned_value, expected_result)
    
    def test_integer_validation_integer_string_entry(self):
        # Arrange
        entered_value = "1"

        expected_result = 1

        # Act
        returned_value = integer_validation(entered_value)

        # Assert
        self.assertEqual(returned_value, expected_result)

    def test_integer_validation_blank_entry(self):
        # Arrange
        entered_value = ""

        expected_result = ""

        # Act
        returned_value = integer_validation(entered_value)

        # Assert
        self.assertEqual(returned_value, expected_result)

    def test_integer_validation_randon_string_entry(self):
        # Arrange
        entered_value = "1akfjha!"

        expected_result = "False"

        # Act
        returned_value = integer_validation(entered_value)

        # Assert
        self.assertEqual(returned_value, expected_result)

    @unittest.mock.patch('os.system')
    @unittest.mock.patch('builtins.print')
    @unittest.mock.patch('brIW.print_table', side_effect=[""])
    @unittest.mock.patch('brIW.enter_integer', side_effect=[""])
    def test_remove_item_returns_list_when_passed_blank_string(self, enter_int, print_tab, builtins_print, os_system):
        # Arrange
        list_to_pass = [0, 1, 2, 3, 4, 5]
        object_type="test"
        expected = [0, 1, 2, 3, 4, 5]

        # Act
        result = remove_item(list_to_pass, object_type)

        # Assert
        self.assertEqual(expected, result)

    @unittest.mock.patch('os.system')
    @unittest.mock.patch('builtins.print')
    @unittest.mock.patch('brIW.print_table')
    @unittest.mock.patch('brIW.enter_integer', side_effect=[5, ""])
    def test_remove_item_returns_list_with_item_removed(self, enter_int, print_tab, builtins_print, os_system):
        # Arrange
        list_to_pass = [0, 1, 2, 3, 4, 5]
        object_type="test"
        expected = [0, 1, 2, 3, 4]

        # Act
        result = remove_item(list_to_pass, object_type)

        # Assert
        self.assertEqual(expected, result)

    @unittest.mock.patch('os.system')
    @unittest.mock.patch('builtins.print')
    @unittest.mock.patch('brIW.print_table')
    @unittest.mock.patch('brIW.enter_integer', side_effect=[5, 1, ""])
    def test_remove_item_returns_list_with_2_items_removed(self, enter_int, print_tab, builtins_print, os_system):
        # Arrange
        list_to_pass = [0, 1, 2, 3, 4, 5]
        object_type="test"
        expected = [0, 2, 3, 4]

        # Act
        result = remove_item(list_to_pass, object_type)

        # Assert
        self.assertEqual(expected, result)

    @unittest.mock.patch('os.system')
    @unittest.mock.patch('builtins.print')
    @unittest.mock.patch('brIW.print_table')
    @unittest.mock.patch('brIW.enter_integer', side_effect=[5, 1, 0, ""])
    def test_remove_item_returns_list_with_3_items_removed(self, enter_int, print_tab, builtins_print, os_system):
        # Arrange
        list_to_pass = [0, 1, 2, 3, 4, 5]
        object_type="test"
        expected = [2, 3, 4]

        # Act
        result = remove_item(list_to_pass, object_type)

        # Assert
        self.assertEqual(expected, result)

    @unittest.mock.patch('os.system')
    @unittest.mock.patch('builtins.print')
    @unittest.mock.patch('brIW.print_table')
    @unittest.mock.patch('brIW.enter_integer', side_effect=[5, 5, ""])
    def test_remove_item_returns_list_with_item_removed_when_passed_wrong_input(self, enter_int, print_tab, builtins_print, os_system):
        # Arrange
        list_to_pass = [0, 1, 2, 3, 4, 5]
        object_type="test"
        expected = [0, 1, 2, 3, 4]

        # Act
        result = remove_item(list_to_pass, object_type)

        # Assert
        self.assertEqual(expected, result)

    @unittest.mock.patch('os.system')
    @unittest.mock.patch('builtins.print')
    @unittest.mock.patch('brIW.print_table')
    @unittest.mock.patch('brIW.enter_integer', side_effect=[5])
    def test_choose_item_returns_value_when_within_list_len_range(self,  enter_int, print_tab, builtins_print, os_system):
        # Arrange
        list_to_pass = [0, 1, 2, 3, 4, 5]
        object_type = "test"
        expected = 5

        # Act
        result = choose_item(list_to_pass, object_type)

        # Assert
        self.assertEqual(expected, result)

    @unittest.mock.patch('os.system')
    @unittest.mock.patch('builtins.print')
    @unittest.mock.patch('brIW.print_table')
    @unittest.mock.patch('brIW.enter_integer', side_effect=[9, 4])
    def test_choose_item_asks_for_another_item_when_out_of_list_len_range(self,  enter_int, print_tab, builtins_print, os_system):
        # Arrange
        list_to_pass = [0, 1, 2, 3, 4, 5]
        object_type = "test"
        expected = 4

        # Act
        result = choose_item(list_to_pass, object_type)

        # Assert
        self.assertEqual(expected, result)

    @unittest.mock.patch('os.system')
    @unittest.mock.patch('builtins.print')
    @unittest.mock.patch('brIW.print_table')
    @unittest.mock.patch('brIW.enter_integer', side_effect=[""])
    def test_choose_item_returns_blank_string(self,  enter_int, print_tab, builtins_print, os_system):
        # Arrange
        list_to_pass = [0, 1, 2, 3, 4, 5]
        object_type = "test"
        expected = ""

        # Act
        result = choose_item(list_to_pass, object_type)

        # Assert
        self.assertEqual(expected, result)

    @unittest.mock.patch('store.run_db_set_command', side_effect=[True])
    def test_add_person_to_round_no_errors_returns_true(self, run_db_set_comm):
        #Arrange
        new_round = Mock(Round)
        new_round.get_round_id.return_value = 2
        new_round.get_brew_maker.return_value = "me"

        person = "me"
        drink = "test"
        expected = True

        #Act
        result = add_person_to_round(new_round, person, drink)

        #Assert
        self.assertEqual(expected, result)

    @unittest.mock.patch('store.run_db_set_command', side_effect=[False])
    def test_add_person_to_round_with_errors_returns_false(self, run_db_set_comm):
        # Arrange
        new_round = Mock(Round)
        new_round.get_round_id.return_value = 2
        new_round.get_brew_maker.return_value = "me"

        person = "me"
        drink = "test"
        expected = False

        # Act
        result = add_person_to_round(new_round, person, drink)

        # Assert
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
