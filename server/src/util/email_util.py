import smtplib
import logging
from datetime import timedelta

from email.message import EmailMessage

from src.config import settings
from src.users.models import User
from src.auth.jwt import JwtToken

logger = logging.getLogger(__name__)


class Email:
    """
    Service class for sending emails.
    """

    def __init__(self, email: str, password: str, host: str, port: int):
        """
        Initialize the Email service with the necessary credentials and server details.

        :param email: sender's email address.
        :param password: sender's email password.
        :param host: SMTP server host.
        :param port: SMTP server port.
        """
        self.email = email
        self.password = password
        self.host = host
        self.port = port

    async def _send(
        self, email_to: str, subject: str, template: str, subtype: str = "html"
    ):
        """
        Send an email using the SMTP server.

        :param email_to: recipient's email address.
        :param subject: subject of the email.
        :param template: HTML content of the email.
        :param subtype: subtype of the email content. Default is "html"
        :raises Exception: if sending email failed.
        """
        try:
            with smtplib.SMTP_SSL(self.host, self.port) as server:
                logger.debug(f"Preparing mail from...")
                server.login(self.email, self.password)
                email = EmailMessage()
                email["Subject"] = subject
                email["From"] = self.email
                email["To"] = email_to

                email.set_content(template, subtype=subtype)
                server.send_message(email)
                logger.debug(f"Mail send")

        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    async def send_verify_email(self, recipient: User):
        """
        Send a verification email to a user.
        """
        subject = "Verify email for Reminder"

        verify_token = JwtToken.create_access_token(
            {"sub": recipient.login}, timedelta(days=2)
        )

        verify_email_template = f"""
                    <div>
                        <h3> Hello, sweety</h3>
                        <br>
                        <p>Click on the button</p>
                        <a href="{settings.client.ORIGIN}/api/auth/verification/{verify_token}">
                            Verify email
                        </a>
                    </div>
                """

        await self._send(recipient.email, subject, verify_email_template)

    async def send_reminder_letter(self, recipient: User, name) -> None:
        """
        Send a reminder email to a user.

        :param recipient: user to send the reminder email to.
        :param name: name of the task to remind the user about.
        """
        subject = "Test"

        test_template = f"""
                    <div>
                        <h3> Hello, sweety. Don't forget</h3>
                        <br>
                        <p>The deadline for completing the task {name} is in three days</p>
                    </div>
                """

        await self._send(recipient.email, subject, test_template)


email = Email(
    settings.smtp.EMAIL,
    settings.smtp.PASSWORD.get_secret_value(),
    settings.smtp.HOST,
    settings.smtp.PORT,
)
