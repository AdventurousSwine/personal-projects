from cryptography.fernet import Fernet
import json

filename = "passwords.txt"
passdict = {}


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

    with open("passwords.txt") as fh:
        for line in fh:
            command, description = line.strip().split(None, 1)
            passdict[command] = description.strip()
    out_file = open("passwords.json", "a")
    json.dump(passdict, out_file, indent=4, sort_keys=False)
    out_file.close()

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