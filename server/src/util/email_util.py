import smtplib
from datetime import timedelta

from email.message import EmailMessage

from src.config import SMTP_EMAIL, SMTP_PASSWORD
from src.users.models import User
from src.auth.jwt import create_access_token


class Email:

    @classmethod
    def send_verify_email(cls, recipient: User) -> EmailMessage:
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
                email = EmailMessage()
                email["Subject"] = "Verify email for Reminder"
                email["From"] = SMTP_EMAIL
                email["To"] = recipient.email

                verify_token = create_access_token(
                    {"sub": recipient.login}, timedelta(days=2)
                )

                verify_email_template = f"""
                            <div>
                                <h3> Hello, sweety</h3>
                                <br>
                                <p>Click on the button</p>
                                <a href="http://localhost:8000/api/auth/verification/{verify_token}">
                                    Verify email
                                </a>
                            </div>
                        """

                email.set_content(verify_email_template, subtype="html")
                server.send_message(email)
        except Exception as e:
            print(f"Failed to send email: {e}")

    @classmethod
    def send_test(cls, recipient: User) -> None:
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
                email = EmailMessage()
                email["Subject"] = "AAAAAAAAAA"
                email["From"] = SMTP_EMAIL
                email["To"] = recipient.email

                verify_email_template = f"""
                            <div>
                                <h3> Hello, sweety</h3>
                                <br>
                                <p>Check mailing with Celery</p>
                            </div>
                        """

                email.set_content(verify_email_template, subtype="html")
                server.send_message(email)
        except Exception as e:
            print(f"Failed to send email: {e}")
