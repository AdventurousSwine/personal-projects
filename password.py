from cryptography.fernet import Fernet
import json
import secrets
import string
import random
import pickle

filename = "passwords.txt"
passdict = {}
random.seed(secrets.token_bytes())


class Master:

    def __init__(self, mp: str):
        self.mstr = mp


def initial():

    mp = input("Please create your new master password: ")
    return mode()


def subsequent():

    input("Would you like to update your master password? y/n")
    if input == "y":
        input("Create your new password:")
    else:
        return old()


def old():

    input("What is the master password? ")
    if input != Master:
        print("The password is incorrect. Please try again. ")
        return
    else:
        return mode()



alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for i in range(8, 18))
work = random.randint(4, 8)


def gen():
    scret = str(secrets.token_hex(work))
    print(f"{scret} has {len(scret)} characters.")


def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    write_key()


def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key

#key = load_key() + mstr.encode()
#fer = Fernet(key)


def view():

    with open("passwords.txt", "r") as f:
        for line in f.readlines():
            data = (line.rstrip())
            usrn, pwd, email = data.split("|")
            print("Username: ", usrn, "Email: ", email, "Password: ", fer.decrypt(pwd.encode()))


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


def mode():

    input("Would you like to add a new account or view existing ones? (add, view, quit)")
    if mode == "quit":
        quit()
    if mode == "view":
        view()
    if mode == "add":
        add()
    else:
        print("Invalid input.")
        mode()