from email.message import EmailMessage

import aiosmtplib

from src.core.logger import logging


class EmailService:
    def __init__(self, mail_from: str, mail_to: list[str]):
        self._from = mail_from
        self._to = mail_to

    async def send(self, html: str) -> None:
        msg = EmailMessage()
        msg["Subject"] = "Новая заявка с сайта"
        msg["From"] = self._from
        msg["To"] = ", ".join(self._to)
        msg.set_content(html, subtype="html")

        try:
            await aiosmtplib.send(msg, hostname="localhost", port=25)
        except Exception as err:
            logging.error("Email send error: %s", err)
