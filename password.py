from cryptography.fernet import Fernet


masterpwd = input("What is the master password? ")

def view():
    with open("passwords.txt", "r") as f:
        for line in f.readlines():
            data = (line.rstrip())
            usrn, pwd, email = data.split("|")
            print("Username: ", usern, "Email: ", email, "Password: ", pwd)

def add():
    usern = input("Username:")
    email = input("Email: ")
    pwd = input("Password: ")

    with open("passwords.txt", "a") as f:
        f.write(usern + "|" + email + "|" + pwd + "\n")

while True:
    mode = input("Would you like to add a new password or view existing ones? (add, view, quit)")

    if mode == "quit":
        break

    if mode == "view":
        pass

    elif mode == "add":
        pass

    else:
        print("Invalid input.")
        continue