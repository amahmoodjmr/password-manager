## Secured Password Manager

A lightweight and secure password manager designed to help users store, manage, and retrieve their passwords safely. Passwords are **hashed before storage** and only accessible through a **master key authentication system**.

## Features

*  **Master Key Authentication** – required for both registration and deletion of any password.
*  **Secure Password Storage** – all user passwords are hashed before saving.
*  **Website & Domain Mapping** – stores website names and their domains alongside the hashed passwords.
*  **Password Retrieval** – upon request, displays all stored passwords in their hashed format along with their associated websites/domains.
*  **Secure Deletion** – only authorized with the master key.

## How It Works

1. **Set Master Key** – Users register with a master key, which will be required for all operations.
2. **Add Passwords** – Store new website credentials (name, domain, and password). The password is **hashed** before storage.
3. **View Passwords** – Display all saved credentials (website + domain + hashed password).
4. **Delete Passwords** – Remove a stored password securely by authenticating with the master key.


## Tech Stack

* **Language:** Python 
* **Hashing Algorithm:** SHA-256 
* **Storage:** Local file / database 


## Getting Started

### Prerequisites

* Install Python 3.x
* Install dependencies (if any)

```bash
pip install -r requirements.txt
```

### Run the Project

```bash
python password_manager.py
```



## Example Usage

* **Register Master Key**
* **Add Passwords**

  * Input: Website → `Facebook`, Domain → `facebook.com`, Password → `mypassword123`
  * Stored: `Facebook | facebook.com | <hashed_password>`
* **View Saved Passwords**

  ```
   Website        Domain          Password
   Facebook |  facebook.com |  5f4dcc3b5aa765d61d8327deb882cf99
   Gmail    |  gmail.com    |  098f6bcd4621d373cade4e832627b4f6
  ```


## Security Notes

* Passwords are **never stored in plaintext**.
* The **master key** should be kept safe, as it is required for all operations.
* Hashing ensures that even if the storage is compromised, raw passwords are not revealed.


## Author by: 

Developed by **Abubakar Sadeeq (Tremor)**
