import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
mail_content = """Good Afternoon,

The following image is  of an unauthorized vehicle in the parking garage.
    
Respecfully,
    Design Team 08"""

def sendEmail():
    #The mail addresses and password
    sender_address = 'smartparkinguofa@gmail.com'
    sender_pass = 'JoshAaron2021'
    receiver_address = 'joshuanewman16@gmail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Unauthorized Vehicle Entered Parking Garage'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')