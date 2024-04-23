import smtplib
from datetime import timedelta

from email.message import EmailMessage

from src.config import SMTP_EMAIL, SMTP_PASSWORD
from src.users.models import User
from src.auth.jwt import create_access_token


class Email:

    @classmethod
    async def _send(
        cls, email_to: str, subject: str, template: str, subtype: str = "html"
    ) -> None:
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
                email = EmailMessage()
                email["Subject"] = subject
                email["From"] = SMTP_EMAIL
                email["To"] = email_to

                email.set_content(template, subtype=subtype)
                server.send_message(email)

        except Exception as e:
            print(f"Failed to send email: {e}")

    @classmethod
    async def send_verify_email(cls, recipient: User) -> None:
        subject = "Verify email for Reminder"

        verify_token = create_access_token({"sub": recipient.login}, timedelta(days=2))

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

        await cls._send(recipient.email, subject, verify_email_template)

    @classmethod
    async def send_test(cls, recipient: User) -> None:
        subject = "Test"

        test_template = f"""
                    <div>
                        <h3> Hello, sweety</h3>
                        <br>
                        <p>Check mailing with Celery</p>
                    </div>
                """

        await cls._send(recipient.email, subject, test_template)
