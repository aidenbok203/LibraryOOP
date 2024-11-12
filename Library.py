from datetime import datetime
from dataclasses import dataclass
import sqlite3

@dataclass
class Book:
    id: int
    title: str
    author: str
    availability: bool = True

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Available: {self.availability}"

class Library:
    def __init__(self):
        self.list = []
        self.createDB()
        self.loadFromFile()

    def createDB(self):
        conn = sqlite3.connect("PY/LibraryOOP/library.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        availability BOOLEAN NOT NULL )
                        """)
        conn.commit()
        conn.close()

    def verifyExistence(self, id) -> bool:
        for book in self.list:
            if book.id == id:
                return True
        return False

    def addBook(self, id, title, author) -> None:
        if not self.verifyExistence(id):
            new_book = Book(id, title, author)
            self.list.append(new_book)
            self.saveToFile()
        else:
            print("Book ID {id} already exists!")

    def checkout(self, id) -> None:
        for book in self.list:
            if book.id == id:
                if book.availability:
                    book.availability = False
                    print(f"{book.title} by {book.author} has been checked out!")
                    self.saveToFile()
                    self.log(currentUser, id, "borrowed")
                    self.writeOwnership(id, currentUser)
                    return
                else:
                    print(f"{book.title} by {book.author} is not available!")
                    return
        print(f"Book ID {id} does not exist!")

    def returnBook(self, id) -> None:
        for book in self.list:
            if book.id == id:
                if not book.availability:
                    if self.removeOwnership(id, currentUser):
                        book.availability = True
                        print(f"{book.title} by {book.author} has been returned!")
                        self.saveToFile()
                        self.log(currentUser, id, "returned")
                        return
                    else:
                        print(f"You do not own book ID {id}!")
                        return
                else:
                    print(f"{book.title} by {book.author} has already been returned!")
                    return
        print(f"Book ID {id} does not exist!")

    def checkOwnership(self, id, user) -> bool:
        with open("PY/LibraryOOP/ownership.txt", "r") as owners:
            for owner in owners:
                owner_user, owner_id = owner.strip().split()
                if owner_user == user and owner_id == str(id):
                    return True
        return False

    def writeOwnership(self, id, user) -> None:
        with open("PY/LibraryOOP/ownership.txt", "a") as owners:
            owners.write(f"{user} {id}\n")

    def removeOwnership(self, id, user) -> bool:
        found = False
        if self.checkOwnership(id, user):
            with open("PY/LibraryOOP/ownership.txt", "r") as owners:
                lines = owners.readlines()
            with open("PY/LibraryOOP/ownership.txt", "w") as owners:
                for line in lines:
                    owner_user, owner_id = line.strip().split()
                    if not (owner_user == user and owner_id == str(id)):
                        owners.write(line)
                    else:
                        found = True
        return found

    def showBooks(self) -> None:
        for book in self.list:
            print(book)

    def saveToFile(self) -> None:
        conn = sqlite3.connect("PY/LibraryOOP/library.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books")
        for book in self.list:
            cursor.execute("INSERT INTO books (id, title, author, availability) VALUES (?, ?, ?, ?)",
                            (book.id, book.title, book.author, book.availability)
            )
        conn.commit()
        conn.close()

    def loadFromFile(self):
        conn = sqlite3.connect("PY/LibraryOOP/library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, availability FROM books")
        rows = cursor.fetchall()
        for row in rows:
            self.list.append(Book(id=row[0], title=row[1], author=row[2], availability=row[3]))
        conn.close()

    def log(self, user, id, action) -> None:
        with open("PY/LibraryOOP/log.txt", "a") as log:
            log.write(f"{datetime.now()}, ID: {id}, {action} by {user}\n")

    def deleteBook(self) -> None:
        req = int(input("Enter book ID to delete: "))
        found = False
        for book in self.list:
            if book.id == req:
                found = True
                self.list.remove(book)
                print(f"Book ID {req} deleted!")
                continue
        if not found:
            print(f"Book ID {req} not found!")
        else:
            self.saveToFile()

    def modifyBook(self, reqId, field: int, changeTo) -> None:
        found = False
        for book in self.list:
            if book.id == reqId:
                found = True
                match field:
                    case 1:
                        book.title = changeTo
                        self.saveToFile()
                    case 2:
                        book.author = changeTo
                        self.saveToFile
                    case _:
                        print("Invalid input!")
        if found:
            print(f"Book ID {reqId} has been modified!")
        else:
            print(f"Book ID {reqId} does not exist!")

def auth() -> bool:
    userList = []
    codeList = []
    x = 0
    userInput, codeInput = input("Enter username: "), input("Enter password: ")
    with open("PY/LibraryOOP/credentials.txt", "r") as users:
        tempList = users.readlines()
    for i in range(int(len(tempList) / 2)) :
        userList.append(tempList[x])
        x += 1
        codeList.append(tempList[x])
        x += 1
    userList = [i.strip() for i in userList]
    codeList = [i.strip() for i in codeList]
    for i in range(len(userList)):
        if userInput == userList[i] and codeInput == codeList[i]:
            print("Logged in!")
            global currentUser
            currentUser = userInput
            return True
    print("Invalid username or password.")
    return False

def createAccount() -> bool:
    print("Creating a new account...")
    userNew, codeNew = input("Enter username: "), input("Enter password: ")
    with open("PY/LibraryOOP/credentials.txt", "a") as users:
        users.writelines(userNew + "\n" + codeNew + "\n")
    match input("Account created! Would you like to login (Y/N)"):
        case "Y" | "y":
            global currentUser
            currentUser = userNew
            return True
        case "N" | "n":
            return False
        case _:
            print("Invalid input!")

def logon() -> None:
    try:
        match int(input("1. Sign in, 2. Sign up\n")):
            case 1:
                return auth()
            case 2:
                return createAccount()
            case _:
                print("Invalid input!")
    except ValueError:
        print("Invalid input!")
        logon()

def menu(library) -> None:
    if logon():
        while True:
            try:
                userIn = int(input("1. Add new book \n2. Display all books \n3. Checkout a book \n4. Return a book \n5. Modify a book \n6. Delete a book \n7. Exit system \n"))
                match userIn:
                    case 1:
                        library.addBook(int(input("Enter book ID: ")), str(input("Enter title: ")), str(input("Enter author: ")))
                        print("Book added to library!")
                    case 2:
                        library.showBooks()
                    case 3:
                        library.checkout(int(input("Enter book ID: ")))
                    case 4:
                        library.returnBook(int(input("Enter book ID: ")))
                    case 5:
                        library.modifyBook(int(input("Book ID to change: ")), int(input("1. Title, 2. Author: ")), input("What would you like to change it to? "))
                    case 6:
                        library.deleteBook()
                    case 7:
                        print("Closing library.")
                        break
                    case _:
                        print("Invalid selection!")
            except ValueError:
                print("Invalid input!")

def main():
    library = Library()
    menu(library)

if __name__ == "__main__":
    main()
