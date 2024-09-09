import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email, credentials):

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = credentials["email"]
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'html'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(credentials["email"], credentials["password"])

        # Send the email
        server.sendmail(credentials["email"], to_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

def notify(new_adverts, recipients, credentials):
    details = ""
    for advert in new_adverts:
        details += f"<li><a href=\"{advert.url}\">{advert.url}</a>"
        if advert.description:
            details += f"<p>{advert.description}</p>"
        details += "</li>"
    html = f"""\
        <html>
        <body> 
            <p>New adverts:</p>
            <ul>
            {details}
            </ul>
        </body>
        </html>
        """
    send_to = ", ".join(recipients)
    send_email("New Housing Adverts!", html, send_to, credentials)
    