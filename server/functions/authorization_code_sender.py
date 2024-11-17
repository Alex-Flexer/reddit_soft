from smtplib import SMTP
from secrets import token_hex
from email.message import EmailMessage


def send_code(email: str) -> str:
    smtp_server = "smtp.mail.ru"
    port = 587
    server = SMTP(smtp_server, port)
    server.starttls()

    sender_email = "sasha.flexer@mail.ru"
    password = "f9fjMdtUvBk0Qtx616jK"

    server.login(sender_email, password)

    authorization_code = token_hex(40)

    message = EmailMessage()
    message["Subject"] = "Confim Code"
    message["From"] = sender_email
    message["To"] = email

    message.set_content("""You are welcomed by Reddit Syndicate, """)

    server.sendmail(sender_email, email, message.as_string())
    return authorization_code


if __name__ == "__main__":
    send_code("sasha.flexer@gmail.com")