from smtplib import SMTP
from secrets import token_hex
from keyring import get_password as get_secret_value


def send_code(email: str) -> str:
    smtp_server = "smtp.mail.ru"
    port = 587
    server = SMTP(smtp_server, port)
    server.starttls()

    sender_email = get_secret_value("sender", "email")
    password = get_secret_value("sender", sender_email)

    server.login(sender_email, password)

    authorization_code = token_hex(40)

    server.sendmail(sender_email, email, authorization_code)
    return authorization_code
