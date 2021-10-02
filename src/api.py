# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='app.auguri@gmail.com',
    to_emails='alexanderaboutanos@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)

# print("Hello real world!")

# cron = CronTab('username')

# /Users/alexanderaboutanos/Desktop/Coding/Springboard/Auguri/app.py
# /Users/alexanderaboutanos/Desktop/Coding/SpringBoard/Auguri/venv/bin/python
