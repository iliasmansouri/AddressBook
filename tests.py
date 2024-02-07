import unittest
from datetime import datetime
from data_handler import Record, AddressBook


class TestRecord(unittest.TestCase):
    def test_parse_valid_date(self):
        record = Record("John Doe", "Male", "15/05/90")
        self.assertEqual(record.date, datetime(1990, 5, 15).date())

    def test_parse_invalid_date(self):
        with self.assertRaises(ValueError):
            Record("John Doe", "Male", "1990-05-15")


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        # Create a sample file with records
        self.filename = "test_records.txt"
        with open(self.filename, "w") as file:
            file.write("John Doe, Male, 15/05/90\n")
            file.write("Jane Doe, Female, 20/03/92\n")

    def test_load_records(self):
        address_book = AddressBook(self.filename)
        address_book.load_records()
        self.assertEqual(len(address_book.get_records()), 2)

    def test_get_record_by_name(self):
        address_book = AddressBook(self.filename)
        address_book.load_records()
        john_records = address_book.get_record_by_name("John Doe")
        jane_records = address_book.get_record_by_name("Jane Doe")
        self.assertEqual(len(john_records), 1)
        self.assertEqual(len(jane_records), 1)
        self.assertEqual(john_records[0].name, "John Doe")
        self.assertEqual(jane_records[0].name, "Jane Doe")

    def test_get_records_by_gender(self):
        address_book = AddressBook(self.filename)
        address_book.load_records()
        male_records = address_book.get_records_by_gender("Male")
        female_records = address_book.get_records_by_gender("Female")
        self.assertEqual(len(male_records), 1)
        self.assertEqual(len(female_records), 1)
        self.assertEqual(male_records[0].gender, "Male")
        self.assertEqual(female_records[0].gender, "Female")

    def test_get_records_by_year(self):
        address_book = AddressBook(self.filename)
        address_book.load_records()
        year_records = address_book.get_records_by_year("1990")
        self.assertEqual(len(year_records), 1)
        self.assertEqual(year_records[0].date.year, 1990)

    def tearDown(self):
        # Clean up the test file
        import os

        os.remove(self.filename)


if __name__ == "__main__":
    unittest.main()
