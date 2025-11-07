from collections import UserDict
import re


class Field:
    """
    Base class for record fields in the address book.
    Stores a single value and provides string representation.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Represents a contact's name.
    The name field is required and cannot be empty.
    """

    def __init__(self, value):
        if not value:
            raise ValueError("Name can't be empty")
        super().__init__(value)


class Phone(Field):
    """
    Represents a contact's phone number.
    Validates that the phone number consists of exactly 10 digits.
    """

    def __init__(self, phone):
        if not re.fullmatch(r'\d{10}', phone):
            raise ValueError("The phone should contain 10 digits")
        super().__init__(phone)


class Record:
    """
    Stores information about a contact,
    including their name and a list of phone numbers.
    Provides methods to add, remove, edit, and find phone numbers.
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        try:
            new_phone = Phone(phone)
            self.phones.append(new_phone)
        except ValueError as e:
            print(f"Couldn't find the phone: {e}")

    def remove_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)
                return True
        print("Phone not found")
        return False

    def edit_phone(self, old_phone, new_phone):
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                try:
                    validated_phone = Phone(new_phone)
                    phone_obj.value = validated_phone.value
                    return True
                except ValueError as e:
                    print(f"Couldn't find the phone: {e}")
                    return False
        print("Phone not found")
        return False

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        print("Phone not found")
        return None

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

    def __repr__(self):
        return self.__str__()


class AddressBook(UserDict):
    """
    Manages a collection of contact records.
    Provides methods to add, find, and delete records by contact name.
    """

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print("Record not found")

    def __str__(self):
        return '\n'.join(str(contact) for contact in self.data.values())


if __name__ == "__main__":
    # Create a new address book
    book = AddressBook()

    # Create a record for John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Add John's record to the address book
    book.add_record(john_record)

    # Create and add a new record for Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Print book.data
    print("Book.data: ", book.data)

    # Print all records in the book
    print("\nAll records in the book:")
    for name, record in book.data.items():
        print(record)

    # Find and edit John's phone number
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print("\nAfter editing John's phone number:")
    print(john)
    # Output: Contact name: John, phones: 1112223333; 5555555555

    # Search for a specific phone number in John's record
    found_phone = john.find_phone("5555555555")
    print(
        f"\nSearching for phone number in John: {
        found_phone.value if found_phone else 'Not found'}")
    # Output: 5555555555

    # Delete Jane's record
    book.delete("Jane")
    print("\nAfter deleting Jane:")
    for name, record in book.data.items():
        print(record)
