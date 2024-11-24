from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if self.is_valid(value):
            super().__init__(value)
        else:
            raise ValueError("Name must be a non-empty string.")

    @staticmethod
    def is_valid(value):
        return isinstance(value, str) and len(value.strip()) > 0


class Phone(Field):
    def __init__(self, value):
        if self.is_valid(value):
            super().__init__(value)
        else:
            raise ValueError("Phone number must be 10 digits.")

    @staticmethod
    def is_valid(value):
        return isinstance(value, str) and value.isdigit() and len(value) == 10


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if isinstance(phone, Phone):
            self.phones.append(phone)
        else:
            raise ValueError("Invalid phone type.")

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_birthday(self, birthday):
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        else:
            raise ValueError("Invalid birthday type.")

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.today().date()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        phones = ", ".join([str(phone) for phone in self.phones])
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"{self.name.value}: Phones: [{phones}], Birthday: {birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        if isinstance(record, Record):
            self.data[record.name.value] = record
        else:
            raise ValueError("Invalid record type.")

    def find_record(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)
                if 0 <= (next_birthday - today).days <= days:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


# Функції для роботи з AddressBook
def add_contact(book, args):
    name = args[0]
    phone = args[1] if len(args) > 1 else None
    birthday = args[2] if len(args) > 2 else None
    record = Record(name)
    try:
        if phone:
            record.add_phone(Phone(phone))
        if birthday:
            record.add_birthday(Birthday(birthday))
        book.add_record(record)
        return f"Contact {name} added."
    except ValueError as e:
        return f"Error: {e}"


def change_contact(book, args):
    name, old_phone, new_phone = args
    record = book.find_record(name)
    if not record:
        return f"Contact {name} not found."
    record.edit_phone(old_phone, Phone(new_phone))
    return f"Contact {name} updated."


def show_phone(book, args):
    name = args[0]
    record = book.find_record(name)
    if not record:
        return f"Contact {name} not found."
    phones = ", ".join([str(phone) for phone in record.phones])
    return f"{name}: {phones}"


def show_all(book):
    return str(book)


def upcoming_birthdays(book, days=7):
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(str(record) for record in upcoming)


# Основна програма
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        if user_input == "exit":
            print("Good bye!")
            break
        elif user_input == "hello":
            print("How can I help you?")
        elif user_input.startswith("add"):
            args = user_input.split()[1:]
            print(add_contact(book, args))
        elif user_input.startswith("change"):
            args = user_input.split()[1:]
            print(change_contact(book, args))
        elif user_input.startswith("phone"):
            args = user_input.split()[1:]
            print(show_phone(book, args))
        elif user_input == "show all":
            print(show_all(book))
        elif user_input.startswith("birthdays"):
            days = int(user_input.split()[1]) if len(user_input.split()) > 1 else 7
            print(upcoming_birthdays(book, days))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
