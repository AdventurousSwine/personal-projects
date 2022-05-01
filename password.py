from cryptography.fernet import Fernet
import json
import random
import string


filename = "passwords.txt"
passdict = {}

masterpwd = input("What is the master password? ")

length = random in range(8, 18)

num = string.digits
letters = string.ascii_letters
gen = random.sample(num + letters, length)

def generate():
    gen
    print(gen)

#def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

#write_key()

def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key

key = load_key() + masterpwd.encode()
fer = Fernet(key)

def view():
    with open("passwords.txt", "r") as f:
        for line in f.readlines():
            data = (line.rstrip())
            usrn, pwd, email = data.split("|")
            print("Username: ", usern, "Email: ", email, "Password: ", fer.decrypt(pwd.encode()))

def add():
    usern = input("Username:")
    email = input("Email: ")
    pwd = input("Password: ")

    with open("passwords.txt", "a") as f:
        f.write(usern + "|" + email + "|" + fer.encrypt(pwd.encode()).decode() + "\n")

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
        view()

    elif mode == "add":
        add()

    else:
        print("Invalid input.")
        continue