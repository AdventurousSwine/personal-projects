from cryptography.fernet import Fernet
import json
import base64
import hashlib
import getpass
import random
import string

# File paths
filename_json = "passwords.json"
filename_master_password = "master_password.txt"

# Function to generate the key using the master password
def generate_key(master_password):
    # Derive the key using PBKDF2 with a high iteration count
    key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), b'salt', 100000)
    return key

# Function to generate a random password with a variable length
def generate_password(min_length=8, max_length=16, chars=string.ascii_letters + string.digits + string.punctuation):
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(chars) for _ in range(length))


# Function to encrypt data
def encrypt_data(data, key):
    # Encode the key using base64 before passing it to Fernet
    cipher_suite = Fernet(base64.urlsafe_b64encode(key))
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

# Function to decrypt data
def decrypt_data(encrypted_data, key):
    # Encode the key using base64 before passing it to Fernet
    cipher_suite = Fernet(base64.urlsafe_b64encode(key))
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

# Function to save the hashed master password to a file
def save_master_password(master_password):
    hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
    with open(filename_master_password, "w") as f:
        f.write(hashed_password)

# Function to load the hashed master password from a file
def load_master_password():
    try:
        with open(filename_master_password, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# Function to check if master password is set and if it's correct
def check_master_password():
    while True:
        master_password = getpass.getpass("Enter your master password: ")
        hashed_master_password = load_master_password()
        if hashed_master_password:
            if hashlib.sha256(master_password.encode()).hexdigest() == hashed_master_password:
                return True
            else:
                print("Incorrect master password. Please try again.")
        else:
            print("No master password set.")
            return False

# Function to view passwords
def view(key):
    try:
        with open(filename_json, "r") as f:
            passwords = json.load(f)
            for website, details in passwords.items():
                print("Website:", website)
                
                # Decode the base64-encoded email and password
                encoded_username = details["username"]
                encoded_email = details["email"]
                encoded_password = details["password"]
                
                
                # Decrypt the email and password
                decrypted_username = decrypt_data(base64.urlsafe_b64decode(encoded_username), key)
                decrypted_email = decrypt_data(base64.urlsafe_b64decode(encoded_email), key)
                decrypted_password = decrypt_data(base64.urlsafe_b64decode(encoded_password), key)
               
                
                print("Username:", decrypted_username)
                print("Email:", decrypted_email)
                print("Password:", decrypted_password)
                print()
    except FileNotFoundError:
        print("No passwords stored yet.")

# Function to add a new password
def add(key):
    while True:
        # Ask for website
        website = input("Website: ")
        if website.strip():  # Check if website is not empty or whitespace
            break
        else:
            print("Error: Website cannot be empty. Please try again.")

    # Ask for username
    while True:
        username_required = input("Do you want to provide a username? (yes/no): ").lower()
        if username_required in ('yes', 'no', 'y', 'n'):
            break
        else:
            print("Error: Please enter 'yes' or 'no'.")

    if username_required in ('yes', 'y'):
        while True:
            username = input("Username: ")
            if username.strip():  # Check if username is not empty or whitespace
                break
            else:
                print("Error: Username cannot be empty. Please try again.")
    else:
        username = ""

    # Ask for email
    while True:
        email_required = input("Do you want to provide an email? (yes/no): ").lower()
        if email_required in ('yes', 'no', 'y', 'n'):
            break
        else:
            print("Error: Please enter 'yes' or 'no'.")

    if email_required in ('yes', 'y'):
        while True:
            email = input("Email: ")
            if email.strip():  # Check if email is not empty or whitespace
                break
            else:
                print("Error: Email cannot be empty. Please try again.")
    else:
        email = ""
        
    # Ask for password
    while True:
        password_choice = input("Do you want to generate a password? (yes/no): ").lower()
        if password_choice == ('yes'):
            password = generate_password()
            print("Password has been generated.")
        else:
            password = getpass.getpass("Password: ")
        if not password:
            print("Error: Password cannot be empty. Please try again.")
            continue
        else:
            break

    # Encrypt the email and password
    encrypted_email = encrypt_data(email, key)
    encrypted_password = encrypt_data(password, key)
    encrypted_username = encrypt_data(username, key)

    # Convert the encrypted email and password to base64-encoded strings
    encoded_email = base64.urlsafe_b64encode(encrypted_email).decode()
    encoded_password = base64.urlsafe_b64encode(encrypted_password).decode()
    encoded_username = base64.urlsafe_b64encode(encrypted_username).decode()

    try:
        # Try to open the existing passwords.json file
        with open(filename_json, "r") as f:
            passwords = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, create a new dictionary for passwords
        passwords = {}

    # Add the new username, email, and password to the dictionary
    passwords[website] = {"username": encoded_username, "email": encoded_email, "password": encoded_password}

    # Write the updated dictionary to the passwords.json file
    with open(filename_json, "w") as f:
        json.dump(passwords, f, indent=4)

    print("Password added successfully.")

# Main function
def main():
    # Check if master password is already set
    master_password = load_master_password()
    if not master_password:
        # If not set, prompt user to set a new master password
        master_password = getpass.getpass("Set your master password: ")
        save_master_password(master_password)

    # Generate the key using the master password
    key = generate_key(master_password)

    # Check if the entered master password is correct
    if not check_master_password():
        print("Incorrect master password. Exiting.")
        return

    while True:
        mode = input("Would you like to add a new password, view existing ones, or quit? (add/view/quit): ").lower()

        if mode == "quit":
            break

        elif mode == "view":
            view(key)

        elif mode == "add":
            add(key)

        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()
