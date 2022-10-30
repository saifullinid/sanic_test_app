import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email, output_msg, msg_title):
    msg = MIMEMultipart()
    msg['From'] = 'saifullin.id.for.logging@gmail.com'
    msg['To'] = email
    msg['Subject'] = msg_title
    message = output_msg
    msg.attach(MIMEText(message))
    try:
        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver.set_debuglevel(True)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login('saifullin.id.for.logging@gmail.com', 'odrundtqchdjxzse')
        mailserver.sendmail('saifullin.id.for.logging@gmail.com', email, msg.as_string())
        mailserver.quit()
    except smtplib.SMTPException as e:
        print(f'<ERROR>: {e}')
