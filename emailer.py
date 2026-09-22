import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


def send_email(subject, html_body):
    if not config.SMTP_APP_PASSWORD:
        raise RuntimeError(
            "SMTP_APP_PASSWORD is not set. Create a Gmail App Password for "
            f"{config.SENDER_EMAIL} and put it in .env (see .env.example)."
        )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = config.SENDER_EMAIL
    msg["To"] = config.RECIPIENT_EMAIL
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.SENDER_EMAIL, config.SMTP_APP_PASSWORD)
        server.sendmail(config.SENDER_EMAIL, [config.RECIPIENT_EMAIL], msg.as_string())
