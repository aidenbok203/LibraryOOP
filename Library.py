from datetime import datetime

class Book:
    def __init__(self, id, title, author, availability = True):
        self.id = id
        self.title = title
        self.author = author
        self.availability = availability

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Available: {self.availability}"

class Library:
    def __init__(self):
        self.list = []
        self.loadFromFile()

    def addBook(self, id, title, author):
        new_book = Book(id, title, author)
        self.list.append(new_book)
        self.saveToFile()

    def checkout(self, id):
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

    def returnBook(self, id):
        for book in self.list:
            if book.id == id:
                if not book.availability:
                    book.availability = True
                    print(f"{book.title} by {book.author} has been returned!")
                    self.saveToFile()
                    self.log(currentUser, id, "returned")
                    self.removeOwnership(id, currentUser)
                    return
                else:
                    print(f"{book.title} by {book.author} has already been returned!")
                    return
        print(f"Book ID {id} does not exist!")

    def checkOwnership(self, id, user):
        with open("PY/LibraryOOP/ownership.txt", "r") as owners:
            for owner in owners:
                owner_user, owner_id = owner.strip().split()
                if owner_user == user and owner_id == str(id):
                    return True
        return False

    def writeOwnership(self, id, user):
        with open("PY/LibraryOOP/ownership.txt", "a") as owners:
            owners.write(f"{user} {id}\n")

    def removeOwnership(self, id, user):
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

    def showBooks(self):
        for book in self.list:
            print(book)

    def saveToFile(self):
        with open("PY/LibraryOOP/Bookshelf.txt", "w") as f:
            for book in self.list:
                f.write(f"{book.id},{book.title},{book.author},{book.availability}\n")

    def loadFromFile(self):
        self.list = []
        try:
            with open("PY/LibraryOOP/Bookshelf.txt", "r") as f:
                for line in f:
                    id, title, author, availability = line.strip().split(",")
                    self.list.append(Book(int(id), title, author, availability == "True"))
        except:
            print("File not found!")

    def log(self, user, id, action):
        with open("PY/LibraryOOP/log.txt", "a") as log:
            log.write(f"{datetime.now()}, ID: {id}, {action} by {user}\n")

    def deleteBook(self):
        req = int(input("Enter book ID to delete: "))
        found = False
        with open("PY/LibraryOOP/Bookshelf.txt", "r") as f:
            lines = f.readlines()
        with open("PY/LibraryOOP/Bookshelf.txt", "w") as f:
            for line in lines:
                id, title, author, availability = line.strip().split(",", 3)
                if int(id) == req:
                    found = True
                    print(f"Book ID {req} deleted!")
                    continue
                f.write(line)
        if not found:
            print(f"Book ID {req} not found!")
        else:
            self.loadFromFile()

def auth():
    userList = []
    codeList = []
    x = 0
    userInput, codeInput = input("Enter username: "), input("Enter password: ")
    with open("PY/LibraryOOP/credentials.txt", "r") as users:
        tempList = users.readlines()
    for i in range(int(len(tempList) / 2)):
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

def createAccount():
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

def logon():
    match int(input("1. Sign in, 2. Sign up\n")):
        case 1:
            return auth()
        case 2:
            return createAccount()
        case _:
            print("Invalid input!")

def menu(library):
    if logon():
        while True:
            try:
                userIn = int(input("1. Add new book \n2. Display all books \n3. Checkout a book \n4. Return a book \n5. Delete a book \n6. Exit system \n"))
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
                        library.deleteBook()
                    case 6:
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
