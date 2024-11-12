import json
import os
from getpass import getpass
from cryptography.fernet import Fernet
import pyperclip
from tabulate import tabulate
from colorama import init, Fore, Style
import bcrypt

# Initialize colorama
init(autoreset=True)

# File to store passwords
PASSWORD_FILE = 'passwords.json'
KEY_FILE = 'key.key'
MASTER_KEY_FILE = 'master.key'

def generate_key():
    """Generate a new encryption key and save it to a file."""
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    """Load the encryption key from a file."""
    return open(KEY_FILE, 'rb').read()

def encrypt_password(password, key):
    """Encrypt a password using the provided key."""
    f = Fernet(key)
    return f.encrypt(password.encode())

def decrypt_password(encrypted_password, key):
    """Decrypt a password using the provided key."""
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()

def hash_password(password):
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    """Verify a password against a hashed password."""
    return bcrypt.checkpw(password.encode(), hashed.encode())

def save_password(website, domain, password):
    """Save a password for a website."""
    key = load_key()
    encrypted_password = encrypt_password(password, key)
    hashed_password = hash_password(password)
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            passwords = json.load(file)
    else:
        passwords = {}
    passwords[website] = {'domain': domain, 'encrypted_password': encrypted_password.decode(), 'hashed_password': hashed_password}
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(passwords, file)

def get_password(website):
    """Retrieve a password for a website."""
    key = load_key()
    with open(PASSWORD_FILE, 'r') as file:
        passwords = json.load(file)
    encrypted_password = passwords.get(website, {}).get('encrypted_password')
    if encrypted_password:
        return decrypt_password(encrypted_password.encode(), key)
    else:
        return None

def delete_password(website):
    """Delete a saved password for a website."""
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            passwords = json.load(file)
        if website in passwords:
            del passwords[website]
            with open(PASSWORD_FILE, 'w') as file:
                json.dump(passwords, file)
            print(Fore.GREEN + f"Password for {website} deleted successfully.")
        else:
            print(Fore.RED + f"No password found for {website}.")
    else:
        print(Fore.RED + "No passwords found.")

def delete_files():
    """Delete the password and key files."""
    try:
        if os.path.exists(PASSWORD_FILE):
            os.remove(PASSWORD_FILE)
            print(Fore.GREEN + f"{PASSWORD_FILE} deleted successfully.")
        if os.path.exists(KEY_FILE):
            os.remove(KEY_FILE)
            print(Fore.GREEN + f"{KEY_FILE} deleted successfully.")
    except Exception as e:
        print(Fore.RED + f"Error deleting files: {e}")

def migrate_passwords():
    """Migrate old password entries to the new format."""
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            passwords = json.load(file)
        updated_passwords = {}
        for website, details in passwords.items():
            if isinstance(details, str):
                # Convert old string entries to the new dictionary format
                updated_passwords[website] = {
                    'domain': website,
                    'encrypted_password': details,
                    'hashed_password': hash_password(decrypt_password(details.encode(), load_key()))
                }
            else:
                updated_passwords[website] = details
        with open(PASSWORD_FILE, 'w') as file:
            json.dump(updated_passwords, file)

def display_passwords():
    """Display all saved passwords in a table."""
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as file:
            passwords = json.load(file)
        table = []
        for website, details in passwords.items():
            if isinstance(details, dict):
                domain = details['domain']
                hashed_password = details['hashed_password']
                table.append([Fore.CYAN + website + Style.RESET_ALL, Fore.YELLOW + domain + Style.RESET_ALL, Fore.GREEN + hashed_password + Style.RESET_ALL])
            else:
                print(Fore.RED + f"Error: Expected a dictionary for {website}, but got {type(details)}")
        print(tabulate(table, headers=[Fore.BLUE + "Website" + Style.RESET_ALL, Fore.BLUE + "Domain" + Style.RESET_ALL, Fore.BLUE + "Hashed Password" + Style.RESET_ALL]))
    else:
        print(Fore.RED + "No passwords found.")

def verify_master_key():
    """Verify the master key before performing sensitive operations."""
    with open(MASTER_KEY_FILE, 'r') as file:
        stored_hashed_master_key = file.read()
    while True:
        master_key = getpass("Enter the master key: ")
        if verify_password(master_key, stored_hashed_master_key):
            return True
        else:
            print(Fore.RED + "Invalid master key! Please try again.")

def main():
    if not os.path.exists(KEY_FILE):
        generate_key()

    if not os.path.exists(MASTER_KEY_FILE):
        master_key = getpass("Set a master key: ")
        hashed_master_key = hash_password(master_key)
        with open(MASTER_KEY_FILE, 'w') as file:
            file.write(hashed_master_key)
        print(Fore.GREEN + "Master key set successfully!")

    migrate_passwords()  # Migrate old password entries to the new format

    while True:
        print("1. Save a new password")
        print("2. Retrieve a password")
        print("3. Display all passwords")
        print("4. Delete a saved password")
        print("5. Delete all saved passwords")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            website = input("Enter the website: ")
            domain = input("Enter the domain: ")
            password = getpass("Enter the password: ")
            save_password(website, domain, password)
            print(Fore.GREEN + "Password saved successfully!")
        elif choice == '2':
            if verify_master_key():
                website = input("Enter the website: ")
                password = get_password(website)
                if password:
                    pyperclip.copy(password)
                    print(Fore.GREEN + "Password copied to clipboard!")
                else:
                    print(Fore.RED + "No password found for this website.")
        elif choice == '3':
            display_passwords()
        elif choice == '4':
            if verify_master_key():
                website = input("Enter the website to delete: ")
                delete_password(website)
        elif choice == '5':
            if verify_master_key():
                delete_files()
        elif choice == '6':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
