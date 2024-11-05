from smtplib import SMTP
import secrets
from keyring import get_password as get_secret_value


def send_code(email: str) -> str:
    smtp_server = "smtp.mail.ru"
    port = 587
    server = SMTP(smtp_server, port)
    server.starttls()

    email = get_secret_value("sender", "email")
    password = get_secret_value("sender", email)
    
    server.login(email, password)

    authorization_code = secrets.token_hex(40)

    server.sendmail("sasha.flexer@mail.ru", email, authorization_code)
    return authorization_code
