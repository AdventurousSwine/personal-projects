from cryptography.fernet import Fernet
import json
import secrets
import string
import random

filename = "passwords.txt"
passdict = {}
random.seed(secrets.token_bytes())


class Master:

    def __init__(self, mp: str):
        self.mstr = mp
        self.alphabet = string.ascii_letters + string.digits
        self.password = ''.join(secrets.choice(self.alphabet) for i in range(8, 18))
        self.work = random.randint(4, 8)


    def initial(self):

        key = Fernet.generate_key()

        with open("mp.key", 'wb') as mp:
            mp.write(key)

        with open('key.key', 'rb') as mp:
            key = mp.read()
        print(key)
        mp = input("Please create your new master password: ")
        return self.mode()


    def subsequent(self):

        input("Would you like to update your master password? y/n")
        if input == "y":
            input("Create your new password:")
        else:
            return self.old()


    def old(self):

        input("What is the master password? ")
        if input != Master:
            print("The password is incorrect. Please try again. ")
            return
        else:
            return self.mode()


    def gen(self):
        scret = str(secrets.token_hex(self.work))
        print(f"{scret} has {len(scret)} characters.")


    def write_key(self):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        self.write_key()


    def load_key(self):
        file = open("key.key", "rb")
        key = file.read()
        file.close()
        return key


    '''key = load_key() + mstr.encode()
    fer = Fernet(key)'''


    def view(self):

        with open("passwords.txt", "r") as f:
            for line in f.readlines():
                data = (line.rstrip())
                usrn, pwd, email = data.split("|")
                print("Username: ", usrn, "Email: ", email, "Password: ", fer.decrypt(pwd.encode()))


    def add(self):

        confirm_input = input("Would you like to generate a password? y/n")
        if confirm_input == "y":
            self.gen()
            usern = input("Username: ")
            email = input("Email: ")
        else:
            usern = input("Username: ")
            email = input("Email: ")
            pwd = input("Password: ")

        with open("passwords.txt", "a") as f:
            f.write(usern + "|" + email + "|" + str(fer.encrypt(self.gen())) + "\n")

        with open("passwords.txt") as fh:
            for line in fh:
                command, description = line.strip().split(None, 1)
                passdict[command] = description.strip()
        out_file = open("passwords.json", "a")
        json.dump(passdict, out_file, indent=4, sort_keys=False)
        out_file.close()


    def mode(self):

        input("Would you like to add a new account or view existing ones? (add, view, quit)")
        if self.mode == "quit":
            quit()
        if self.mode == "view":
            self.view()
        if self.mode == "add":
            self.add()
        else:
            print("Invalid input.")
            self.mode()