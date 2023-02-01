from loadData import subjects;

def classCodeInput():
    classCode = input("Enter class code: ")
    print()
    if classCode in subjects:
        print("Subject Found!")
    else:
        print(">> Class code not found. Please try again!")
        return classCodeInput()