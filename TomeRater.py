class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("Email updated to " + self.email)

    def __repr__(self):
        return "User {name}, email: {email}, books read: {books_read}".format(name=self.name, email=self.email, books_read=len(self.books))

    def __eq__(self, other_user):
        if (self.email == other_user.email) and (self.name == other_user.name):
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        sum = 0
        length = 0
        for i in self.books.values():
            if i:
                sum += i
                length += 1
        return sum/length

    def __hash__(self):
        return hash((self.name, self.email))

class Book(object):
    def __init__(self, title, isbn, price):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        self.price = price

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("ISBN has been updated to " + str(self.isbn))

    def get_price(self):
        return self.price

    def set_price(self, new_price):
        self.price = new_price
        print("Price has been updated to $" + str(new_price))

    def add_rating(self, rating):
        if 0 <= rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def __eq__(self, other_book):
        if (self.title == other_book.title) and (self.isbn == other_book.isbn):
            return True
        else:
            return False

    def get_average_rating(self):
        sum = 0
        for i in self.ratings:
            sum += i
        return sum/len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "{title}, costs ${price}".format(title=self.title, price=self.price)

class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}, costs ${price}".format(title=self.title, author=self.author, price=self.price)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}, costs ${price}".format(title=self.title, level=self.level, subject=self.subject, price=self.price)

class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn, price):
        return Book(title, isbn, price)

    def create_novel(self, title, author, isbn, price):
        return Fiction(title, author, isbn, price)

    def create_non_fiction(self, title, subject, level, isbn, price):
        return Non_Fiction(title, subject, level, isbn, price)

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users.keys():
            self.users[email].read_book(book, rating)
            if rating:
                book.add_rating(rating)
            if book in self.books.keys():
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print("No user with email {email}!".format(email=email))

    def add_user(self, name, email, user_books=None):
        if email in self.users.keys():
            print("User with email {email} already exists.".format(email))
        else:
            if ("@" in email) and ((".com" in email) or (".edu" in email) or (".org" in email)):
                user = User(name, email)
                self.users[email] = user
                if user_books:
                    for book in user_books:
                        self.add_book_to_user(book, email)
            else:
                print("Invalid email address.")

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def get_most_read_book(self):
        most_times = 0
        most_read_book = None
        for book, times_read in self.books.items():
            if times_read > most_times:
                most_times = times_read
                most_read_book = book
        return most_read_book

    def highest_rated_book(self):
        highest_rating = 0
        highest_rated_book = None
        for book in self.books.keys():
            if book.get_average_rating() > highest_rating:
                highest_rating = book.get_average_rating()
                highest_rated_book = book
        return highest_rated_book

    def most_positive_user(self):
        most_positive_rating = 0
        most_positive_user = None
        for user in self.users.values():
            if user.get_average_rating() > most_positive_rating:
                most_positive_rating = user.get_average_rating()
                most_positive_user = user
        return most_positive_user

    def get_worth_of_user(self, user_email):
        sum = 0
        for book in self.users[user_email].books.keys():
            sum += book.price
        return sum

    def get_n_most_expensive_books(self, n):
        d = {}
        for book in self.books.keys():
            d[book] = book.price
        for book in sorted(d, key=d.get, reverse=True)[:n]:
            print(book)

    def get_n_most_read_books(self, n):
        for book in sorted(self.books, key=self.books.get, reverse=True)[:n]:
            print(book)

    def get_n_most_prolific_readers(self, n):
        d = {}
        for user in self.users.values():
            d[user] = len(user.books)
        for user in sorted(d, key=d.get, reverse=True)[:n]:
            print(user)

    def __eq__(self):
        if (self.users == other.users) and (self.books == other.books):
            return True
        else:
            return False

    def __repr__(self):
        u = ""
        b = ""
        for user in self.users.values():
            u += str(user) + "\n"
        for book in self.books.keys():
            b += str(book) + "\n"
        return "\nUsers:\n" + u + "Books:\n" + b
