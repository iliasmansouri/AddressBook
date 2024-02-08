import unittest
from datetime import datetime
from data_handler import Record, AddressBook
import os


class TestRecord(unittest.TestCase):
    def test_parse_valid_date(self):
        # Test parsing a valid date
        record = Record("John Doe", "Male", "01/01/90")
        self.assertEqual(record.date, datetime.strptime("01/01/90", "%d/%m/%y").date())

    def test_parse_invalid_date(self):
        # Test parsing an invalid date
        with self.assertRaises(ValueError):
            Record("Jane Doe", "Female", "2022-01-01")

    def test_to_dict(self):
        # Test converting record to dictionary
        record = Record("Alice Smith", "Female", "25/12/85")
        expected_dict = {
            "Name": "Alice Smith",
            "Gender": "Female",
            "Date": datetime.strptime("25/12/85", "%d/%m/%y").date(),
        }
        self.assertEqual(record.to_dict(), expected_dict)


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        # Create an instance of AddressBook for testing
        self.address_book = AddressBook("test_records.txt")
        self.address_book.add_record("John Doe", "Male", "01/01/90")
        self.address_book.add_record("Jane Doe", "Female", "05/05/95")
        self.address_book.add_record("Alice Smith", "Female", "25/12/85")

    def test_load_records(self):
        # Test loading records
        self.assertEqual(len(self.address_book.records), 3)

    def test_get_record_by_name(self):
        # Test getting record by name
        records = self.address_book.get_record_by_name("John Doe")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].name, "John Doe")

    def test_get_records_by_gender(self):
        # Test getting records by gender
        records = self.address_book.get_records_by_gender("Female")
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].gender, "Female")

    def test_get_records_by_year(self):
        # Test getting records by year
        records = self.address_book.get_records_by_year("1995")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].date.year, 1995)

    def test_add_record(self):
        # Test adding a record
        self.address_book.add_record("Bob Smith", "Male", "15/03/80")
        self.assertEqual(len(self.address_book.records), 4)
        self.assertEqual(self.address_book.records[-1].name, "Bob Smith")

    def test_delete_record(self):
        # Test deleting a record
        self.address_book.delete_record("Jane Doe")
        self.assertEqual(len(self.address_book.records), 2)
        self.assertNotIn(
            "Jane Doe", [record.name for record in self.address_book.records]
        )

    def test_save_records(self):
        # Test saving records
        self.address_book.save_records("test_saved_records.txt")
        with open("test_saved_records.txt", "r") as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 3)

    def tearDown(self):
        # Clean up after tests
        self.address_book = None
        # Clean up saved records file if it exists
        try:
            os.remove("test_saved_records.txt")
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    unittest.main()
