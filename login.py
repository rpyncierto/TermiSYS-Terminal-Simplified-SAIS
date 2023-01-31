from loadData import users;
import getpass;
from display import clearScreen, welcomeMessage;

def usernameExists(username):
    if username in users:
        return True;
    return False;
    
def passwordCheck(username, password):
    if (users[username] == password):
        return True;
    return False;
    
def resetPassword(database, username):
    newPassword = getpass.getpass("Enter new password: ")
    confirmPassword = getpass.getpass("Confirm new password: ")
    print();
    if len(newPassword) < 8:
        clearScreen();
        welcomeMessage();
        print(">> Password must be at least 8 characters. Please try again!\n")
        return resetPassword(database, username);
    elif newPassword == confirmPassword:
        users[username] = newPassword
        database.write(username + "," + newPassword)
        print(">> Password changed successfully!")
    else:
        clearScreen();
        welcomeMessage();
        print(">> Password did not match. Please try again!\n")
        return resetPassword(database, username);
    