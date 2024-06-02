import tkinter as tk
from tkinter import messagebox, simpledialog  
from cryptography.fernet import Fernet
import json
import base64
import hashlib
import getpass
import random
import string

filename_json = "passwords.json"
filename_master_password = "master_password.txt"

def generate_key(master_password):
    key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), b'salt', 100000)
    return key

def generate_password(min_length=8, max_length=16, chars=string.ascii_letters + string.digits + string.punctuation):
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(chars) for _ in range(length))

def encrypt_data(data, key):
    cipher_suite = Fernet(base64.urlsafe_b64encode(key))
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(base64.urlsafe_b64encode(key))
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

def save_master_password(master_password):
    hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
    with open(filename_master_password, "w") as f:
        f.write(hashed_password)

def load_master_password():
    try:
        with open(filename_master_password, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    
def check_master_password():
    while True:
        master_password = simpledialog.askstring("Master Password", "Enter your master password:", show='*')
        hashed_master_password = load_master_password()
        if hashed_master_password:
            if hashlib.sha256(master_password.encode()).hexdigest() == hashed_master_password:
                return master_password
            else:
                messagebox.showerror("Error", "Incorrect master password. Please try again.")
        else:
            messagebox.showinfo("Error", "No master password set.")
            return None

def view(key):
    try:
        with open(filename_json, "r") as f:
            passwords = json.load(f)
            if not passwords:
                messagebox.showinfo("Error", "No passwords stored yet.")
                return
            
            all_passwords = ""
            for website, details in passwords.items():
                decrypted_username = decrypt_data(base64.urlsafe_b64decode(details["username"]), key)
                decrypted_email = decrypt_data(base64.urlsafe_b64decode(details["email"]), key)
                decrypted_password = decrypt_data(base64.urlsafe_b64decode(details["password"]), key)
                all_passwords += (f"Website: {website}\nUsername: {decrypted_username}\nEmail: {decrypted_email}\nPassword: {decrypted_password}\n\n")

            messagebox.showinfo("Password Manager", all_passwords)

    except FileNotFoundError:
        messagebox.showinfo("Error", "No passwords stored yet.") 

def add(key):
    while True:
        website = simpledialog.askstring("Password Manager", "Website:")  
        if website.strip():
            break
        else:
            messagebox.showerror("Error", "Website cannot be empty. Please try again.") 

    username_required = messagebox.askyesno("Input", "Do you want to provide a username?")  
    if username_required:
        while True:
            username = simpledialog.askstring("Password Manager", "Username:") 
            if username.strip():
                break
            else:
                messagebox.showerror("Error", "Username cannot be empty. Please try again.")  
    else:
        username = ""

    email_required = messagebox.askyesno("Password Manager", "Do you want to provide an email?")  
    if email_required:
        while True:
            email = simpledialog.askstring("Password Manager", "Email:")  
            if email.strip():
                break
            else:
                messagebox.showerror("Error", "Email cannot be empty. Please try again.")  
    else:
        email = ""

    while True:
        password_choice = messagebox.askyesno("Password Manager", "Do you want to generate a password?") 
        if password_choice:
            password = generate_password()
            messagebox.showinfo("Password Manager", f"Password: {password}") 
        else:
            password = simpledialog.askstring("Password Manager", "Password:", show='*') 
        if not password:
            messagebox.showerror("Error", "Password cannot be empty. Please try again.")  
        else:
            break

    encrypted_username = encrypt_data(username, key)
    encrypted_email = encrypt_data(email, key)
    encrypted_password = encrypt_data(password, key)

    encoded_username = base64.urlsafe_b64encode(encrypted_username).decode()
    encoded_email = base64.urlsafe_b64encode(encrypted_email).decode()
    encoded_password = base64.urlsafe_b64encode(encrypted_password).decode()

    try:
        with open(filename_json, "r") as f:
            passwords = json.load(f)
    except FileNotFoundError:
        passwords = {}

    passwords[website] = {"username": encoded_username, "email": encoded_email, "password": encoded_password}

    with open(filename_json, "w") as f:
        json.dump(passwords, f, indent=4)

    messagebox.showinfo("Password Manager", "Password added successfully.") 

def custom_ask_string(title, prompt, quit_text):
    root = tk.Tk()
    root.withdraw()  

    dialog = tk.Toplevel(root)
    dialog.title(title)

    tk.Label(dialog, text=prompt).pack()
    entry = tk.Entry(dialog)
    entry.pack(padx=10, pady=5)
    entry.focus_set()
    
    def on_ok():
        dialog.user_input = entry.get()
        dialog.destroy()

    ok_button = tk.Button(dialog, text="OK", command=on_ok, default=tk.ACTIVE)
    ok_button.pack(side=tk.LEFT, padx=10, pady=10)

    quit_button = tk.Button(dialog, text=quit_text, command=root.destroy)
    quit_button.pack(side=tk.RIGHT, padx=10, pady=10)

    dialog.bind('<Return>', lambda event=None: ok_button.invoke())
    dialog.wait_window()
    return dialog.user_input if hasattr(dialog, 'user_input') else None

def main():
    root = tk.Tk()
    root.withdraw()

    master_password = load_master_password()
    if not master_password:
        master_password = simpledialog.askstring("Password Manager", "Set your master password:", show='*')  
        save_master_password(master_password)

    key = generate_key(master_password)

    if not check_master_password():
        messagebox.showerror("Error", "Incorrect master password. Exiting.")
        return

    while True:
        mode = custom_ask_string("Password Manager", "Would you like to add a new password, view existing ones, or quit? (add/view/quit):", "Quit").lower() 

        if mode == "quit":
            break
        elif mode == "view":
            view(key)
        elif mode == "add":
            add(key)
        else:
            messagebox.showerror("Error", "Invalid input. Please try again.")

if __name__ == "__main__":    
    main()
