# =======================================================================>
# pass-steal By khr1st - 2023
#
# This script works by first making a GET request to the Gaia Online 
# login page to obtain a CSRF token. It then logs in using the 
# provided account credentials and the obtained CSRF token. If the 
# login is successful, it extracts the user ID and account token from 
# the response headers and prints them to the console.
# =======================================================================>

import requests

# Replace these variables with your own credentials
username = 'your_username'
password = 'your_password'

# URL for the Gaia Online login page
login_url = 'https://www.gaiaonline.com/auth/login/'

# Set up the request session
session = requests.Session()

# Make a GET request to the login page to get the CSRF token
login_page = session.get(login_url)
csrf_token = session.cookies.get('csrf_token')

# Log in to Gaia Online using the credentials
login_data = {'username': username,
              'password': password,
              'csrf_token': csrf_token}
response = session.post(login_url, data=login_data)

# Check if the login was successful
if 'You have entered an invalid username or password.' in response.text:
    print('Login failed')
else:
    print('Login successful')

# Get the user ID and account token from the response headers
user_id = session.cookies.get('user_id')
account_token = session.cookies.get('gaia_account_token')

# Print the user ID and account token
print(f'User ID: {user_id}')
print(f'Account token: {account_token}')
