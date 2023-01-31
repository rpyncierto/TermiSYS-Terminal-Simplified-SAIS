from loadData import users;

def usernameExists(username):
    if username in users:
        return True;
    return False;
    
def passwordCheck(username, password):
    if (users[username] == password):
        return True;
    return False;