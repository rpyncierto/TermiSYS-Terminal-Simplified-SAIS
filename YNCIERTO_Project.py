import getpass
from prettytable import PrettyTable

users = {}
userRecords = {}
subjects = {}
WF = []
TTH = []


# displays border lines
def border():
    print("-"*131)


# welcome message
def welcome():
    print("""
----------------------------------------------------------------------------------------------------------------------------------
  __    __       _                                  _               ___         __    ___    __              _
 / / /\ \ \ ___ | |  ___   ___   _ __ ___    ___   | |_   ___      / __\ /\/\  / _\  / __\  / _\ _   _  ___ | |_  ___  _ __ ___
 \ \/  \/ // _ \| | / __| / _ \ | '_ ` _ \  / _ \  | __| / _ \    / /   /    \ \ \  / /     \ \ | | | |/ __|| __|/ _ \| '_ ` _ \ 
  \  /\  /|  __/| || (__ | (_) || | | | | ||  __/  | |_ | (_) |  / /___/ /\/\ \_\ \/ /___   _\ \| |_| |\__ \| |_|  __/| | | | | |
   \/  \/  \___||_| \___| \___/ |_| |_| |_| \___|   \__| \___/   \____/\/    \/\__/\____/   \__/ \__, ||___/ \__|\___||_| |_| |_|
                                                                                                  |___|
""")


# function that displays the menu
def displayMenu():
    welcome()
    print("\t\t\t\t\t\t\t [1] Login", "\t\t\t\t\t\t\t [2] Sign Up",
          "\t\t\t\t\t\t\t [0] Exit", sep="\n",)
    print()
    choice = int(input("Choice: "))
    print()
    border()
    return choice


# function that loads the credentials of the users
def loadCredentials():
    database = open("users.txt", "r")
    users.clear()
    for line in database:
        credentials = line.strip().split(",")
        username = credentials[0]
        password = credentials[-1]
        users[username] = password
    database.close()


# login part of the system
def login():
    attempt = 0
    while attempt < 3:
        print()
        loadCredentials()  # loads the credentials of the users
        username = input("Enter Username: ")
        password = getpass.getpass("Enter Password: ")
        if username not in users or password != users[username]:
            print("Username or Password is incorrect. Please try again!")
        else:
            print("Login successful!")
            print()
            border()
            checkRecords(username)
            return
        attempt += 1
    print()
    border()
    print()
    isValidUsername()
    return username

# displays the menu for enrollment


def enrollMenu(username):
    displaySchedule(username)
    print()
    print("[1] Enroll in a course",
          "[2] Unenroll in a course", "[0] Exit", sep="\n")
    print()
    try:
        choice = int(input("Choice: "))
        print()
        border()
        print()
        if choice == 1:
            classCodeInput(username)
        elif choice == 2:
            unenroll(username)
            saveCredentialsToFile()
            saveSubjectsToFile()
            return checkRecords(username)
        elif choice == 3:
            return displayMenu()
        elif choice == 0:
            print("Thank you for using the system!")
            print()
            border()
            exit()
        else:
            print("Invalid input!")
            print()
            border()
            return enrollMenu(username)
    except ValueError:
        print()
        border()
        print()
        print("Invalid input. Please enter integer only!")
        print()
        border()
        return enrollMenu(username)

# unenroll the course the user wishes to


def unenroll(username):
    for item in userRecords[username]:
        if item[0] == "C":
            return unenrollValidation(username)
    print("You are not yet enrolled in any subject!")
    print()
    border()
    return enrollMenu(username)

# unenroll the course the user wishes to


def unenrollValidation(username):
    classCode = input("Enter class code: ")
    if classCode in userRecords[username]:
        for items in userRecords[username]:
            if items == classCode:
                index = userRecords[username].index(items)
                userRecords[username][index] = str(
                    "unenrolled" + classCode)
                for items in userRecords[username]:
                    if items.isdigit() == True:
                        index = userRecords[username].index(items)
                        units = int(items) - \
                            int(subjects[classCode][0])
                        userRecords[username][index] = str(units)
        subjects[classCode][-1] = str(int(subjects[classCode][-1]) - 1)
        print()
        print("Unenroll successfull!")
        print()
        border()
        print()
        saveCredentialsToFile()
        return enrollMenu(username)
    else:
        print()
        print("Class code not found!")
        print()
        border()
        print()
        return unenroll(username)

# save records of the enrollment of the user in a file


def saveCredentialsToFile():
    fileWriter = open("usersrecords.txt", "w")
    for k in userRecords:
        record = ""
        for i in range(len(userRecords[k])):
            if i < len(userRecords[k]) - 1:
                record += str(userRecords[k][i]) + ","
            else:
                record += str(userRecords[k][i])
        fileWriter.write(k + "," + record + "\n")
    fileWriter.close()

# checks if username is in the record of those who have already enrolled a course


def checkRecords(username):
    userRecords = loadUserRecords()
    if username in userRecords:
        return enrollMenu(username)
    else:
        isEnrolling(username)

# displays the schedule of the user


def displaySchedule(username):
    schedule = userRecords[username].copy()
    newWF = []
    newTTH = []
    for item in schedule:
        if item.isdigit() == False:
            if item[0] == "C":
                if subjects[item][-3] == "WF":
                    newWF.append(item + " " + subjects[item][-5])
                else:
                    newTTH.append(item + " " + subjects[item][-5])
            else:
                subject = str(item[10:len(item)])
                if subjects[subject][-3] == "WF":
                    newWF.append(" ")
                else:
                    newTTH.append(" ")
    if len(newWF) < 4:
        for i in range(4-len(newWF)):
            newWF.append(" ")
    if len(newTTH) < 4:
        for i in range(4-len(newTTH)):
            newTTH.append(" ")
    for item in schedule:
        if item.isdigit() == True:
            units = item
    print()
    print("Enrolled Units: ", units)
    print()
    table = PrettyTable()
    table.title = "Weekly Schedule"
    table.add_column("Time", ["08-09", "09-10", "10-11", "11-12"])
    table.add_column("Monday", [" ", " ", " ", " ", ])
    table.add_column("Tuesday", newTTH)
    table.add_column("Wednesday", newWF)
    table.add_column("Thursday", newTTH)
    table.add_column("Friday", newWF)
    table.add_column("Saturday", [" ", " ", " ", " ", ])
    table.add_column("Sunday", [" ", " ", " ", " ", ])
    print(table)
    WF = newWF
    TTH = newTTH


# displays the menu for suername valudation
def isValidUsername():
    print("You have reached the maximum attempts. Do you want to check if your username exists?")
    print()
    print("[1] Yes", "[2] No", sep="\n")
    print()
    while True:
        try:
            choice = int(input("Choice: "))
            if choice == 1:
                print()
                border()
                print()
                checkUsername()
                return
            elif choice == 2:
                return
            else:
                print()
                border()
                print()
                print("Invalid input!")
                print()
                border()
                print()
                return isValidUsername()
        except ValueError:
            print()
            border()
            print()
            print("Invalid input. Please enter integer only!")
            print()
            border()
            print()
            return isValidUsername()

# checks if the username of the user is already in the system


def checkUsername():
    username = input("Enter Username: ")
    print()
    if username not in users:
        print("Username does not exist. Please sign up to register! ")
        return
    else:
        print("Username exist!")
        print()
        isValidPassword(username)
        return

# displays the menu for password validation


def isValidPassword(username):
    print("Forgot Password?")
    print()
    print("[1] Yes", "[2] No", sep="\n")
    print()
    while True:
        try:
            option = int(input("Choice: "))
            if option == 1:
                print()
                border()
                print()
                passwordCheck(username)
                return
            elif option == 2:
                return
            else:
                print()
                border()
                print()
                print("Invalid input")
                print()
                border()
                print()
                return isValidPassword(username)
        except ValueError:
            print()
            border()
            print()
            print("Invalid input. Please enter integer only!")
            print()
            border()
            print()
            return isValidPassword(username)

# checks if the new password inputted by the user is valid, in case he/she forgot his/her password


def passwordCheck(username):
    newpassword = getpass.getpass("Enter new password: ")
    confirmation = getpass.getpass("Confirm new password: ")
    if len(newpassword) < 8:
        print("Password must be at least 8 characters. Please try again!")
        print()
        passwordCheck(username)
    elif newpassword == confirmation:
        database = open("users.txt", "w")
        users[username] = newpassword
        database.write(username + "," + newpassword)
        database.close()
        print("Password changed successfully!")
        return
    else:
        print("Password did not match. Please try again!")
        print()
        passwordCheck(username)

# load the enrolled subjects of the user


def loadUserRecords():
    database = open("usersrecords.txt", "r")
    userRecords.clear()
    for line in database:
        records = line.strip().split(",")
        username = records[0]
        enrolledSubjects = records[1:len(records)]
        userRecords[username] = enrolledSubjects
    database.close()
    return userRecords

# displays a menu for enrollment


def isEnrolling(username):
    print()
    print(
        "You are not yet enrolled in any subject. Do you want to enroll now?")
    print()
    print("[1] Yes", "[2] No", sep="\n")
    print()
    try:
        choice = int(input("Choice: "))
        if choice == 1:
            print()
            border()
            print()
            classCodeInput(username)
        elif choice == 2:
            return
        else:
            print()
            border()
            print()
            print("Invalid input!")
            print()
            border()
            return isEnrolling(username)
    except ValueError:
        print()
        border()
        print()
        print("Invalid input. Please enter integer only!")
        print()
        border()
        return isEnrolling(username)

# fuction that lets the user register if they still do not have an account in the system


def register():
    print()
    loadCredentials()
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")
    confirm = getpass.getpass("Confirm Password: ")
    if username in users:
        print("Username already exists. Please try again!")
        register()
    elif len(password) < 8:
        print("Password must be at least 8 characters. Please try again!")
        register()
    elif password != confirm:
        print("Password did not match. Please try again!")
        register()
    else:
        database = open("users.txt", "a")
        database.write(username + "," + password + "\n")
        database.close()
        print("Registration successful!")

# laod all subjects in the system


def loadSubjects():
    database = open("subjects.txt", "r")
    for line in database:
        description = line.strip().split(",")
        classCode = description[0]
        classInformation = description[1:len(description)]
        subjects[classCode] = classInformation
    database.close()

# class code validation


def classCodeInput(username):
    classCode = input("Enter class code: ")
    print()
    if classCode in subjects:
        print(getClass(subjects[classCode]))
        checkEnroll(username, classCode)
    else:
        print("Class code not found!")
        print()
        border()
        print()
        return classCodeInput(username)

# displays the menu whether the user wishes to enroll or not of a specific course


def checkEnroll(username, classCode):
    print()
    print("Do you want to enroll in this course?")
    print()
    print("[1] Yes", "[2] No", sep="\n")
    print()
    try:
        choice = int(input("Choice: "))
        print()
        border()
        print()
        if choice == 1:
            loadCredentials()
            if int(subjects[classCode][-1]) <= int(subjects[classCode][-2]):
                if username in userRecords:
                    for items in userRecords[username]:
                        if items.isdigit() == True:
                            if int(items) < 15:
                                for items in userRecords[username]:
                                    if items == classCode:
                                        print(
                                            "Enrollment Failed. Course already exist!")
                                        print()
                                        border()
                                        return enrollMenu(username)
                                WFcount = 0
                                TTHcount = 0
                                for items in userRecords[username]:
                                    if items.isdigit() == False:
                                        if items[0] == "C":
                                            if subjects[items][-3] == "WF":
                                                WFcount += 1
                                            else:
                                                TTHcount += 1
                                if subjects[classCode][-3] == "WF":
                                    if WFcount >= 4:
                                        print(
                                            "Enrollment Failed. Class schedules overlap!")
                                        print()
                                        border()
                                        return enrollMenu(username)
                                    else:
                                        enrollCourse(username, classCode)
                                        return enrollMenu(username)
                                else:
                                    if TTHcount >= 4:
                                        print(
                                            "Enrollment Failed. Class schedules overlap!")
                                        print()
                                        border()
                                        return enrollMenu(username)
                                    else:
                                        enrollCourse(username, classCode)
                                        return enrollMenu(username)
                            else:
                                print(
                                    "Enrollment Failed. Maximum units already taken!")
                                print()
                                border()
                                return enrollMenu(username)
                # if it is the first time the user is enrolling in a course, it will automatically enrolled given that the capacity of the course in which he/she wishes to enroll is not yer maximized.
                userRecords[username] = [classCode, subjects[classCode][0]]
                print("Enrollment Successful!")
                subjects[classCode][-1] = str(int(subjects[classCode][-1]) + 1)
                saveSubjectsToFile()
                saveCredentialsToFile()
                print()
                border()
                return enrollMenu(username)
            else:
                print("Enrollment Failed. Class already reached maximum capacity!")
                print()
                border()
                return checkRecords(username)
        elif choice == 2:
            return checkRecords(username)
        else:
            print("Invalid input!")
            print()
            print(getClass(subjects[classCode]))
            return checkEnroll(username, classCode)
    except ValueError:
        print()
        border()
        print()
        print("Invalid input. Please enter integer only!")
        print()
        print(getClass(subjects[classCode]))
        return checkEnroll(username, classCode)


# enrolls the user in the specific course
def enrollCourse(username, classCode):
    for item in userRecords[username]:
        if item.isdigit() == False:
            if item[0] == "u":
                subject = str(item[10:len(item)])
                if subjects[subject][-3] == "WF" and subjects[classCode][-3] == "WF":
                    index = userRecords[username].index(item)
                    userRecords[username][index] = classCode
                    return saveEnrolledSubjects(username, classCode)
                elif subjects[subject][-3] == "TTH" and subjects[classCode][-3] == "TTH":
                    index = userRecords[username].index(item)
                    userRecords[username][index] = classCode
                    return saveEnrolledSubjects(username, classCode)
                else:
                    userRecords[username].append(classCode)
                    return saveEnrolledSubjects(username, classCode)
    userRecords[username].append(classCode)
    return saveEnrolledSubjects(username, classCode)

# updates the units taken by the user each time he/she enrolls a course. This also updates the enrolled students in the course when the user enrolled.


def saveEnrolledSubjects(username, classCode):
    for items in userRecords[username]:
        if items.isdigit() == True:
            units = int(items) + \
                int(subjects[classCode][0])
    userRecords[username][1] = str(units)
    subjects[classCode][-1] = str(int(subjects[classCode][-1]) + 1)
    saveCredentialsToFile()
    print("Enrollment Successful!")
    saveSubjectsToFile()
    print()
    border()
    return enrollMenu(username)

# displays the class description of the course the user wishes to enroll


def getClass(code):
    table = PrettyTable()
    table._max_width = {"Class Description": 50}
    table.field_names = ["Units", "Class Description", "Instructor",
                         "Section", "Hrs/Class", "Days/Week", "Capacity", "Enrolled"]
    table.add_row(code)
    return table

# save subjects enrolled by the user in the system


def saveSubjectsToFile():
    fileWriter = open("subjects.txt", "w")
    for k in subjects:
        record = ""
        for i in range(len(subjects[k])):
            if i < len(subjects[k]) - 1:
                record += str(subjects[k][i]) + ","
            else:
                record += str(subjects[k][i])
        fileWriter.write(k + "," + record + "\n")
    fileWriter.close()


# main part of the program
records = open("usersrecords.txt", "a")
records.close()
database = open("users.txt", "a")
database.close()
loadUserRecords()
loadSubjects()
loadCredentials()
while True:
    try:
        choice = displayMenu()
        if choice == 1:
            login()
        elif choice == 2:
            register()
        elif choice == 0:
            print()
            print("Thank you for using the system!")
            print()
            border()
            exit()
        else:
            print()
            print("Invalid input. Please try again!")
    except ValueError:
        print()
        border()
        print()
        print("Invalid input. Please enter integer only!")
