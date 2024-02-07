from data_handler import AddressBook
from datetime import datetime


class Browser:
    def __init__(self, address_book):
        self.address_book = address_book

    def count_records(self, gender):
        records = self.address_book.get_records_by_gender(gender)
        return len(records)

    def get_oldest_record(self):
        oldest_record = None
        for record in self.address_book.get_records():
            if oldest_record is None or record.date < oldest_record.date:
                oldest_record = record
        return oldest_record

    def get_age_difference(self, name1, name2):
        records = self.address_book.get_record_by_name(
            name1
        ) + self.address_book.get_record_by_name(name2)
        if len(records) < 2:
            return "Both names not found in the address book."

        record1, record2 = records[0], records[1]
        date_format = "%d/%m/%y"
        date1 = record1.date
        date2 = record2.date
        age_difference = abs((date2 - date1).days)
        return (
            f"The age difference between {name1} and {name2} is {age_difference} days."
        )


if __name__ == "__main__":
    address_book = AddressBook("data.txt")
    address_book.load_records()

    browser = Browser(address_book)

    # Count male records
    num_males = browser.count_records("male")
    print(f"Number of males in the address book: {num_males}")

    # Count female records
    num_females = browser.count_records("female")
    print(f"Number of females in the address book: {num_females}")

    # Get the oldest record
    oldest_record = browser.get_oldest_record()
    if oldest_record:
        print(
            f"The oldest record is: {oldest_record.name}, {oldest_record.gender}, {oldest_record.date}"
        )
    else:
        print("No records found in the address book.")

    age_difference = browser.get_age_difference("Bill McKnight", "Paul Robinson")
    print(age_difference)
