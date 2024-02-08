from .data_handler import Record, AddressBook
from datetime import datetime
from typing import Union, Optional


class Browser:
    def __init__(self, address_book: AddressBook) -> None:
        self.address_book: AddressBook = address_book

    def count_records(self, gender: str) -> int:
        records = self.address_book.get_records_by_gender(gender)
        return len(records)

    def get_oldest_record(self) -> Optional[Record]:
        oldest_record: Optional[Record] = None
        for record in self.address_book.get_records():
            if oldest_record is None or record.date < oldest_record.date:
                oldest_record = record
        return oldest_record

    def get_youngest_record(self) -> Optional[Record]:
        youngest_record: Optional[Record] = None
        for record in self.address_book.get_records():
            if youngest_record is None or record.date > youngest_record.date:
                youngest_record = record
        return youngest_record

    def get_age_difference(self, name1: str, name2: str) -> str:
        records = self.address_book.get_record_by_name(
            name1
        ) + self.address_book.get_record_by_name(name2)
        if len(records) < 2:
            return "Both names not found in the address book."

        record1, record2 = records[0], records[1]
        date1 = record1.date
        date2 = record2.date
        age_difference = abs((date2 - date1).days)
        return (
            f"The age difference between {name1} and {name2} is {age_difference} days."
        )


if __name__ == "__main__":
    address_book: AddressBook = AddressBook("assets/data.txt")

    browser: Browser = Browser(address_book)

    # Count male records
    num_males: int = browser.count_records("male")
    print(f"Number of males in the address book: {num_males}")

    # Count female records
    num_females: int = browser.count_records("female")
    print(f"Number of females in the address book: {num_females}")

    # Get the oldest record
    oldest_record: Optional[Record] = browser.get_oldest_record()
    if oldest_record:
        print(
            f"The oldest record is: {oldest_record.name}, {oldest_record.gender}, {oldest_record.date}"
        )
    else:
        print("No records found in the address book.")

    age_difference: str = browser.get_age_difference("Bill McKnight", "Paul Robinson")
    print(age_difference)

    # Get the most recent record
    youngest_record: Optional[Record] = browser.get_youngest_record()
    if youngest_record:
        print(
            f"The youngest record is: {youngest_record.name}, {youngest_record.gender}, {youngest_record.date}"
        )
    else:
        print("No records found in the address book.")
