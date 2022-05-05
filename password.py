from cryptography.fernet import Fernet
import json
import secrets
import string
import random


filename = "passwords.txt"
passdict = {}
random.seed(secrets.token_bytes())
masterpwd = input("What is the master password? ")

alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for i in range(8, 18))

work = random.randint(4, 8)

def gen():
    scret = str(secrets.token_hex(work))
    print(f"{scret} has {len(scret)}")

#def write_key():
    #key = Fernet.generate_key()
    #with open("key.key", "wb") as key_file:
        #key_file.write(key)

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
    confirm_input = input("Would you like to generate a password? y/n")
    if confirm_input == "y":
        gen()
        usern = input("Username: ")
        email = input("Email: ")
    else:
        usern = input("Username: ")
        email = input("Email: ")
        pwd = input("Password: ")

    with open("passwords.txt", "a") as f:
        f.write(usern + "|" + email + "|" + str(fer.encrypt(gen())) + "\n")

    with open("passwords.txt") as fh:
        for line in fh:
            command, description = line.strip().split(None, 1)
            passdict[command] = description.strip()
    out_file = open("passwords.json", "a")
    json.dump(passdict, out_file, indent=4, sort_keys=False)
    out_file.close()

while True:
    mode = input("Would you like to add a new account or view existing ones? (add, view, quit)")

    if mode == "quit":
        break

    if mode == "view":
        view()

    elif mode == "add":
        add()

    else:
        print("Invalid input.")
        continue