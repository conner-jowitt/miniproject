import unittest
from unittest.mock import Mock, call
import store
import connection

class Test_Methods(unittest.TestCase):
    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_is_active_in_db_returns_true_when_active_values_in_db(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, 2, 1, 4, 1],
                                             [1, 1, 1, 4, 1],
                                             [1, 4, 1, 4, 1]]
        table = "round"
        column_to_check = "round_id"
        looking_for_value = 1
        expected = True
        
        # Act
        result = store.is_active_in_db(table, column_to_check, looking_for_value)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_called_with("SELECT * FROM round WHERE round_id='1' AND active=1;")
        self.assertEqual(expected, result)

    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_is_active_in_db_returns_false_when_no_active_values_in_db(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        table = "round"
        column_to_check = "round_id"
        looking_for_value = 1
        expected = False
        
        # Act
        result = store.is_active_in_db(table, column_to_check, looking_for_value)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_called_with("SELECT * FROM round WHERE round_id='1' AND active=1;")
        self.assertEqual(expected, result)

    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_is_in_db_returns_true_when_active_values_in_db(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, 2, 1, 4, 1],
                                             [1, 1, 1, 4, 1],
                                             [1, 4, 1, 4, 1]]
        table = "round"
        column_to_check = "round_id"
        looking_for_value = 1
        expected = True
        
        # Act
        result = store.is_in_db(table, column_to_check, looking_for_value)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_called_with("SELECT * FROM round WHERE round_id='1';")
        self.assertEqual(expected, result)

    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_is_in_db_returns_false_when_no_active_values_in_db(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        table = "round"
        column_to_check = "round_id"
        looking_for_value = 1
        expected = False
        
        # Act
        result = store.is_in_db(table, column_to_check, looking_for_value)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_called_with("SELECT * FROM round WHERE round_id='1';")
        self.assertEqual(expected, result)

    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_get_drink_name_from_id_returns_name_when_passed_valid_id(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, "tea", "a refreshing cup of tea", 1]]
        drink_id = 1
        expected = "tea"
        
        # Act
        result = store.get_drink_name_from_id(drink_id)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_has_calls([call("SELECT * FROM drinks WHERE drink_id='1' AND active=1;"), call("SELECT * FROM drinks WHERE active=1 AND drink_id='1';")])
        self.assertEqual(expected, result)

    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_get_drink_name_from_id_returns_false_when_passed_invalid_id(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        drink_id = 1
        expected = False
        
        # Act
        result = store.get_drink_name_from_id(drink_id)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_has_calls([call("SELECT * FROM drinks WHERE drink_id='1' AND active=1;")])
        self.assertEqual(expected, result)
    
    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_get_drink_id_from_name_returns_name_when_passed_valid_name(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, "tea", "a refreshing cup of tea", 1]]
        drink_name = "tea"
        expected = 1
        
        # Act
        result = store.get_drink_id_from_name(drink_name)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_has_calls([call("SELECT * FROM drinks WHERE drink_name='tea' AND active=1;"), call("SELECT * FROM drinks WHERE active=1 AND drink_name='tea';")])
        self.assertEqual(expected, result)

    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_get_drink_id_from_name_returns_false_when_passed_invalid_name(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        drink_name = "tea"
        expected = False
        
        # Act
        result = store.get_drink_id_from_name(drink_name)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_has_calls([call("SELECT * FROM drinks WHERE drink_name='tea' AND active=1;")])
        self.assertEqual(expected, result)

    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_get_person_name_from_id_returns_name_when_passed_valid_id(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, "john", 1, 1]]
        person_id = 1
        expected = "john"
        
        # Act
        result = store.get_person_name_from_id(person_id)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_has_calls([call("SELECT * FROM people WHERE person_id='1' AND active=1;"), call("SELECT * FROM people WHERE active=1 AND person_id='1';")])
        self.assertEqual(expected, result)

    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_get_person_name_from_id_returns_false_when_passed_invalid_id(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        person_id = 1
        expected = False
        
        # Act
        result = store.get_person_name_from_id(person_id)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_has_calls([call("SELECT * FROM people WHERE person_id='1' AND active=1;")])
        self.assertEqual(expected, result)
    
    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_get_person_id_from_name_returns_id_when_passed_valid_name(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1, "john", 1, 1]]
        person_name = "john"
        expected = 1
        
        # Act
        result = store.get_person_id_from_name(person_name)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_has_calls([call("SELECT * FROM people WHERE full_name='john' AND active=1;"), call("SELECT * FROM people WHERE active=1 AND full_name='john';")])
        self.assertEqual(expected, result)

    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_get_person_id_from_name_returns_false_when_passed_invalid_name(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        person_name = "john"
        expected = False
        
        # Act
        result = store.get_person_id_from_name(person_name)

        #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_has_calls([call("SELECT * FROM people WHERE full_name='john' AND active=1;")])
        self.assertEqual(expected, result)

    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_load_some_rows_active_columns_from_db_called_correctly_and_returns(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [[1,2,3],[4,5,6],[7,8,9]]
        columns_to_return = ["column1", "column2", "column3"]
        table = "people"
        column_to_match = "thisone"
        looking_for_value = 1
        sql_command = "SELECT column1, column2, column3 FROM people WHERE active=1 AND thisone='1';"
        expected = [[1,2,3],[4,5,6],[7,8,9]]


        #Act
        result = store.load_some_rows_active_columns_from_db(columns_to_return, table, column_to_match, looking_for_value)

         #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_has_calls([call(sql_command)])
        self.assertEqual(expected, result)

    @unittest.mock.patch('connection.create_db_connection', return_value=unittest.mock)
    def test_update_db_row_value_called_correctly_and_returns(self, create_db_connection):
        # Arrage
        mock_connection = Mock()
        create_db_connection.return_value = mock_connection
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        table = "people"
        row_id_to_change = "thisone"
        row_value = 1
        column = "here"
        looking_for_value = "changeme"
        sql_command = "UPDATE people SET here='changeme' WHERE thisone='1';"
        expected = True


        #Act
        result = store.update_db_row_value(table, row_id_to_change, row_value, column, looking_for_value)

         #Assert
        create_db_connection.assert_called_with()
        mock_connection.cursor.assert_called_with()
        mock_cursor.execute.assert_has_calls([call(sql_command)])
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
