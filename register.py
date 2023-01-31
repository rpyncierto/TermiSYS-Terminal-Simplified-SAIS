import getpass;
from loadData import users;
from login import validPassword;
from display import clearScreen, welcomeMessage;


def register(database):
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")
    confirm = getpass.getpass("Confirm Password: ")
    if username in users:
        clearScreen();
        welcomeMessage();
        print(">> Username already exists. Please try again!\n")
        return register(database);
    elif(validPassword(password, confirm)):
        database.write(username + "," + password + "\n")
        print("\n>> Registration successful!")
    else:
        return register(database);