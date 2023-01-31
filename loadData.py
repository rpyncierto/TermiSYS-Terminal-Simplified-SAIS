users = {}
userRecords = {}
subjects = {}
WF = []
TTH = []

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

def loadSubjects():
    database = open("subjects.txt", "r")
    for line in database:
        description = line.strip().split(",")
        classCode = description[0]
        classInformation = description[1:len(description)]
        subjects[classCode] = classInformation
    database.close()
    
def loadCredentials():
    database = open("users.txt", "r")
    users.clear()
    for line in database:
        credentials = line.strip().split(",")
        username = credentials[0]
        password = credentials[-1]
        users[username] = password
    database.close()  