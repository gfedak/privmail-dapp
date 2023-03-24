import smtplib
import json
import gnupg

# Open the JSON configuration file for reading
with open('settings.json', 'r') as f:
    settings = json.load(f)

#configure the SMTP server
smtp_server = settings['smtp_server']
smtp_port = settings['smtp_port']
sender_email = settings['email']
smtp_passwd = settings['smtp_passwd']

receiver_email = "reply-to@gmail.com"

print( smtp_server, smtp_port, sender_email, smtp_passwd)

#Prepare the message with the GPG pub key of the recipient
gpg = gnupg.GPG()
key_data = settings['gpg_pubkey']
import_result = gpg.import_keys(key_data)

body = 'YOUR MESSAGE HERE'
encrypted_data = gpg.encrypt(body, import_result.fingerprints[0])

message = f"""\
From: {sender_email}
To: {receiver_email}
Subject: Toto titi
""" +str(encrypted_data)

# Open a connection with the SMTP server
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(sender_email, smtp_passwd)

# Send email
server.sendmail(sender_email, receiver_email, message)

server.quit()
