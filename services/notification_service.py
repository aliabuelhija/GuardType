import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def send_email(receiver_email, subject, template_name, context):
    sender_email = "guardtypealert@gmail.com"
    password = "tixb bakf fbmx hcgb"

    # Load HTML template from file
    env = Environment(loader=FileSystemLoader(searchpath=r'C:\Users\ali12\PycharmProjects\guardtype_server\templates'))
    template = env.get_template(template_name)
    html = template.render(context)

    # Create MIME object
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the HTML message
    message.attach(MIMEText(html, "html"))

    # Connect to the server and send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")

def notify_first_active(receiver_email, username):
    context = {"username": username}
    send_email(receiver_email, "Welcome to GuardType!", 'first_activation.html', context)

def notify_change(receiver_email, username, old_keyboard, new_keyboard):
    context = {"username": username, "old_keyboard": old_keyboard, "new_keyboard": new_keyboard}
    send_email(receiver_email, "Keyboard Change Alert", 'keyboard_change.html', context)

def notify_offensive_word(receiver_email, username, detected_content):
    context = {"username": username, "detected_content": detected_content}
    send_email(receiver_email, "Content Alert Notification", 'offensive_word.html', context)
