import smtplib
from getpass import getpass

user = input('User:\n')
password = getpass('Password:\n')
recipients = input('Recipients (separate with spaces):\n').split()
message = """Subject: Testing Testing
Hello from Python.

Sincerely,
This script"""

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.starttls()
    server.login(user, password)
    server.sendmail(user, recipients, message)
finally:
    server.quit()
