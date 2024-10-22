import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv

# Function to send email with attachment using SMTP
def send_email_smtp(recipient_email, recipient_name, subject, sender_email, sender_password, message_template, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = msg['From'] = f'Mahak Jain'
   
    msg['To'] = recipient_email
    msg['Subject'] = subject  # Set the batch custom subject

    # Replace {name} in the message template with the actual recipient's name
    personalized_message = message_template.replace("{name}", recipient_name)
    msg.attach(MIMEText(personalized_message, 'html'))  # Use HTML for formatting

    # Attach the resume (or any file)
    attachment = open(attachment_path, 'rb')

    # Create the MIMEBase object
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={attachment_path.split("/")[-1]}')

    # Attach the file to the email
    msg.attach(part)

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Update with the correct SMTP server
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print(f'Email sent to {recipient_email}')
    except Exception as e:
        print(f'Failed to send email to {recipient_email}: {e}')

# Function to load contacts from CSV
def load_contacts(filename):
    contacts = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            contacts.append({
                'email': row['email'],
                'name': row['name']
            })
    return contacts

# Function to read the message template from a file
def read_message_template(filename):
    with open(filename, 'r') as file:
        return file.read()

# Function to read the subject from a file
def read_subject(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

if __name__ == "__main__":
    # Your Gmail credentials
    sender_email = 'jainmahak1310@gmail.com'
    sender_password = 'rvqw xlhn tcih ygig'

    # Path to your resume (or any file you want to attach)
    attachment_path = 'Mahak_Jain_Resume.pdf'

    # Load contacts from the CSV file
    contacts = load_contacts('contacts.csv')

    # Read the message template from the text file
    message_template = read_message_template('message_template.txt')

    # Read the subject for this batch from a text file
    subject = read_subject('subject.txt')

    # Send email with attachment to each contact in the batch
    for contact in contacts:
        send_email_smtp(contact['email'], contact['name'], subject, sender_email, sender_password, message_template, attachment_path)
