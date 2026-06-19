import smtplib
import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


class EmailSender:
    """
    Reusable utility to send emails with optional attachments.

    Credentials are loaded from environment variables to avoid hardcoding secrets:
        EMAIL_HOST     - SMTP host (e.g. smtp.gmail.com)
        EMAIL_PORT     - SMTP port (e.g. 587)
        EMAIL_USER     - Sender email address
        EMAIL_PASSWORD - Sender email password / app password

    Example usage:
        sender = EmailSender()
        sender.send(
            to="qa@company.com",
            subject="Test Report",
            body="See attached report.",
            attachments=["reports/report.docx"]
        )
    """

    DEFAULT_HOST = "smtp.gmail.com"
    DEFAULT_PORT = 587

    def __init__(
        self,
        host: str = None,
        port: int = None,
        user: str = None,
        password: str = None,
    ):
        self.host = host or os.getenv("EMAIL_HOST", self.DEFAULT_HOST)
        self.port = int(port or os.getenv("EMAIL_PORT", self.DEFAULT_PORT))
        self.user = user or os.getenv("EMAIL_USER")
        self.password = password or os.getenv("EMAIL_PASSWORD")

        if not self.user or not self.password:
            raise EnvironmentError(
                "Email credentials are missing. "
                "Set EMAIL_USER and EMAIL_PASSWORD as environment variables."
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def send(
        self,
        to: Union[str, list[str]],
        subject: str,
        body: str,
        attachments: list[Union[str, Path]] = None,
        cc: Union[str, list[str]] = None,
        bcc: Union[str, list[str]] = None,
        html: bool = False,
    ) -> bool:
        """
        Send an email with optional file attachments.

        Args:
            to          : Recipient(s) — string or list of strings.
            subject     : Email subject line.
            body        : Email body (plain text or HTML).
            attachments : List of file paths to attach (optional).
            cc          : CC recipient(s) (optional).
            bcc         : BCC recipient(s) (optional).
            html        : Set True if body contains HTML markup.

        Returns:
            True if sent successfully, False otherwise.
        """
        recipients = self._normalize_addresses(to)
        cc_list = self._normalize_addresses(cc)
        bcc_list = self._normalize_addresses(bcc)

        msg = self._build_message(
            to=recipients,
            subject=subject,
            body=body,
            attachments=attachments or [],
            cc=cc_list,
            html=html,
        )

        all_recipients = recipients + cc_list + bcc_list

        try:
            with smtplib.SMTP(self.host, self.port, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.user, all_recipients, msg.as_string())

            logger.info(
                "Email sent successfully | to=%s | subject='%s' | attachments=%d",
                all_recipients,
                subject,
                len(attachments or []),
            )
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed. Check EMAIL_USER / EMAIL_PASSWORD.")
        except smtplib.SMTPException as e:
            logger.error("SMTP error while sending email: %s", e)
        except OSError as e:
            logger.error("Network/connection error: %s", e)

        return False

    def send_report(
        self,
        to: Union[str, list[str]],
        test_name: str,
        status: str,
        report_path: Union[str, Path] = None,
        extra_body: str = "",
    ) -> bool:
        """
        Convenience method specifically for sending test reports.
        Builds a pre-formatted subject & body for QA use cases.

        Args:
            to          : Recipient(s).
            test_name   : Name of the test / test suite.
            status      : Result string, e.g. 'PASS', 'FAIL'.
            report_path : Path to the report file to attach (optional).
            extra_body  : Additional text appended to the email body.

        Returns:
            True if sent successfully, False otherwise.
        """
        subject = f"[TEST REPORT] {test_name} — {status.upper()}"
        body = (
            f"Test Name : {test_name}\n"
            f"Status    : {status.upper()}\n"
        )
        if extra_body:
            body += f"\n{extra_body}"

        body += "\n\n-- Sent automatically by QA Automation Framework --"

        attachments = [report_path] if report_path else []

        return self.send(to=to, subject=subject, body=body, attachments=attachments)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_message(
        self,
        to: list[str],
        subject: str,
        body: str,
        attachments: list,
        cc: list[str],
        html: bool,
    ) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = self.user
        msg["To"] = ", ".join(to)
        msg["Subject"] = subject
        if cc:
            msg["Cc"] = ", ".join(cc)

        mime_type = "html" if html else "plain"
        msg.attach(MIMEText(body, mime_type))

        for file_path in attachments:
            self._attach_file(msg, Path(file_path))

        return msg

    @staticmethod
    def _attach_file(msg: MIMEMultipart, file_path: Path) -> None:
        if not file_path.exists():
            logger.warning("Attachment not found, skipping: %s", file_path)
            return

        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment",
            filename=file_path.name,
        )
        msg.attach(part)
        logger.debug("Attached file: %s (%.1f KB)", file_path.name, file_path.stat().st_size / 1024)

    @staticmethod
    def _normalize_addresses(addresses: Union[str, list, None]) -> list[str]:
        if not addresses:
            return []
        if isinstance(addresses, str):
            return [addr.strip() for addr in addresses.split(",") if addr.strip()]
        return [addr.strip() for addr in addresses if addr.strip()]