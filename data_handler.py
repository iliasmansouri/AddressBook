from datetime import datetime, date
from typing import List
import pandas as pd


class Record:
    def __init__(self, name: str, gender: str, date: str) -> None:
        self.name: str = name
        self.gender: str = gender
        self.parse_date(date)

    def parse_date(self, date_str: str) -> None:
        # TODO better handling of different date formats
        try:
            self.date: date = datetime.strptime(date_str, "%d/%m/%y").date()
        except ValueError:
            raise ValueError(
                "Invalid date format. Date should be in the format 'dd/mm/yy'."
            )

    def __str__(self) -> str:
        return f"[Name: \t{self.name}, \nGender: {self.gender}, \nDate: \t{self.date}]"

    def to_dict(self):
        return {"Name": self.name, "Gender": self.gender, "Date": self.date}


class AddressBook:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.records: List[Record] = []
        self.df: pd.DataFrame = pd.DataFrame(columns=["Name", "Gender", "Date"])
        self.__load_records()

    def __load_records(self) -> None:
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    record_data = line.strip().split(",")
                    name = record_data[0].strip()
                    gender = record_data[1].strip()
                    date = record_data[2].strip()
                    record = Record(name, gender, date)
                    self.records.append(record)
                    self.df = pd.concat(
                        [self.df, pd.DataFrame([record.to_dict()])], ignore_index=True
                    )
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")

    def get_records(self) -> List[Record]:
        return self.records

    def get_record_by_name(self, name: str) -> List[Record]:
        matching_records = [
            record for record in self.records if record.name.lower() == name.lower()
        ]
        return matching_records

    def get_records_by_gender(self, gender: str) -> List[Record]:
        matching_records = [
            record for record in self.records if record.gender.lower() == gender.lower()
        ]
        return matching_records

    def get_records_by_year(self, year: str) -> List[Record]:
        matching_records = [
            record for record in self.records if record.date.year == int(year)
        ]
        return matching_records

    def add_record(self, name: str, gender: str, date: str) -> None:
        if any(record.name.lower() == name.lower() for record in self.records):
            raise ValueError(f"Record with name '{name}' already exists.")

        record = Record(name, gender, date)
        self.records.append(record)
        self.df = pd.concat(
            [self.df, pd.DataFrame([record.to_dict()])], ignore_index=True
        )

    def save_records(self, filename: str = "records.txt") -> None:
        with open(filename, "w") as file:
            for record in self.records:
                file.write(f"{record.name}, {record.gender}, {record.date}\n")

    def get_df(self) -> pd.DataFrame:
        return self.df

    def delete_record(self, name: str) -> None:
        # Delete record from the list of records
        self.records = [
            record for record in self.records if record.name.lower() != name.lower()
        ]

        # Delete record from the DataFrame
        self.df = self.df[self.df["Name"].str.lower() != name.lower()]


# Example Usage:
if __name__ == "__main__":
    # Example of how to use the AddressBook class
    address_book = AddressBook("./assets/data.txt")

    # Display loaded records
    print("Loaded Records:")
    for record in address_book.get_records():
        print(record)
    # Add a new record
    address_book.add_record("John Doe", "Male", "15/05/90")
    # Save records to the file
    address_book.save_records()

    # Display updated records
    print("\nUpdated Records:")
    for record in address_book.get_records():
        print(record)

    # Get records by name
    print("\nRecords for John Doe:")
    john_doe_records = address_book.get_record_by_name("John Doe")
    for record in john_doe_records:
        print(record)
    # Get records by gender
    female_records = address_book.get_records_by_gender("Female")
    print("\nFemale Records:")
    for record in female_records:
        print(record)

    # Get records by year
    year = "1990"
    year_records = address_book.get_records_by_year(year)
    print(f"\nRecords from the year {year}:")
    for record in year_records:
        print(record)
