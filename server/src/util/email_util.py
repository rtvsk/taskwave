import smtplib
import logging
from datetime import timedelta

from email.message import EmailMessage

from src.config import settings
from src.users.models import User
from src.auth.jwt import JwtToken

logging.basicConfig(
    level=logging.DEBUG,
    filename="email_log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


class Email:

    __EMAIL = settings.smtp.EMAIL
    __PASSWORD = settings.smtp.PASSWORD.get_secret_value()

    @classmethod
    async def _send(
        cls, email_to: str, subject: str, template: str, subtype: str = "html"
    ) -> None:
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                logger.info(f"Preparing mail from {cls.__EMAIL}...")
                server.login(cls.__EMAIL, cls.__PASSWORD)
                email = EmailMessage()
                email["Subject"] = subject
                email["From"] = cls.__EMAIL
                email["To"] = email_to

                email.set_content(template, subtype=subtype)
                server.send_message(email)
                logger.info(f"Mail send")

        except Exception as e:
            logger.debug(f"Failed to send email: {e}")

    @classmethod
    async def send_verify_email(cls, recipient: User) -> None:
        subject = "Verify email for Reminder"

        verify_token = JwtToken.create_access_token(
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

    @classmethod
    async def send_test_reminder_letter(cls, recipient: User, name) -> None:
        subject = "Test"

        test_template = f"""
                    <div>
                        <h3> Hello, sweety. Don't forget</h3>
                        <br>
                        <p>The deadline for completing the task {name} is in three days</p>
                    </div>
                """

        await cls._send(recipient.email, subject, test_template)
