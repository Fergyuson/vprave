from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr, field_validator
import os, ssl, json
import httpx
import aiosmtplib
import urllib.parse
from email.message import EmailMessage

router = APIRouter(prefix="/leads", tags=["leads"])

def get_b24_url() -> str:
    url = os.getenv("BITRIX_WEBHOOK_URL")
    if not url:
        raise RuntimeError("Переменная BITRIX_WEBHOOK_URL не установлена")
    return url

PROJECT_NAME       = os.getenv("PROJECT_NAME", "DevService — лендинг заявок")

SMTP_HOST     = os.getenv("SMTP_HOST", "smtp.mailgun.org")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_IMPLICIT = os.getenv("SMTP_USE_IMPLICIT_TLS", "false").lower() == "true"  # true→465, false→587 STARTTLS

MAIL_FROM = os.getenv("MAIL_FROM", "leads@e-devservice.ru")
MAIL_TO   = os.getenv("MAIL_TO",   "leads-control@e-devservice.ru")
MAIL_BCC  = [e.strip() for e in os.getenv("MAIL_BCC", "cto@e-devservice.ru,owner@e-devservice.ru").split(",") if e.strip()]

class LeadIn(BaseModel):
    name: str
    phone: str
    email: EmailStr | None = None
    comment: str | None = None
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    utm_term: str | None = None
    utm_content: str | None = None

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        digits = "".join(ch for ch in v if ch.isdigit())
        if digits.startswith("8"):
            digits = "7" + digits[1:]
        if len(digits) < 10:
            raise ValueError("Некорректный номер телефона")
        return digits

@router.post("", summary="Создать лид в Bitrix24 и отправить письмо-дубликат")
async def create_lead(lead: LeadIn, request: Request):
    b24_url = get_b24_url()
    import logging
    logging.getLogger(__name__).info("➡️  Bitrix URL: %s", b24_url)

    # 1) Bitrix24
    b24_payload = {
        "fields": {
            "TITLE": f"{PROJECT_NAME}: заявка от {lead.name}",
            "NAME": lead.name,
            "PHONE": [{"VALUE": lead.phone, "VALUE_TYPE": "WORK"}],
            "EMAIL": [{"VALUE": str(lead.email or ""), "VALUE_TYPE": "WORK"}],
            "COMMENTS": lead.comment or "",
            "SOURCE_ID": "WEB",
            "UTM_SOURCE": lead.utm_source or "",
            "UTM_MEDIUM": lead.utm_medium or "",
            "UTM_CAMPAIGN": lead.utm_campaign or "",
            "UTM_TERM": lead.utm_term or "",
            "UTM_CONTENT": lead.utm_content or "",
        }
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(b24_url, json=b24_payload)
        if resp.status_code != 200:
            raise HTTPException(502, f"Bitrix HTTP {resp.status_code}: {resp.text}")
        data = resp.json()
        if "error" in data:
            raise HTTPException(502, f"Bitrix error: {data.get('error_description') or data['error']}")
        lead_id = data.get("result")

    # 2) Письмо
    subject = f"[{PROJECT_NAME}] Новая заявка (лид #{lead_id})"
    lines = [
        f"Проект: {PROJECT_NAME}",
        f"Лид #{lead_id}",
        f"Имя: {lead.name}",
        f"Телефон: +{lead.phone}",
        f"Email: {lead.email or '—'}",
        f"Комментарий: {lead.comment or '—'}",
        "",
        "UTM:",
        f"  source:   {lead.utm_source or '—'}",
        f"  medium:   {lead.utm_medium or '—'}",
        f"  campaign: {lead.utm_campaign or '—'}",
        f"  term:     {lead.utm_term or '—'}",
        f"  content:  {lead.utm_content or '—'}",
        "",
        f"IP: {request.client.host}",
    ]
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = MAIL_FROM
    msg["To"] = MAIL_TO
    if MAIL_BCC:
        msg["Bcc"] = ", ".join(MAIL_BCC)
    msg.set_content("\n".join(lines))

    ctx = ssl.create_default_context()
    email_sent = False
    try:
        if SMTP_IMPLICIT:                       # SMTPS 465
            await aiosmtplib.send(
                msg,
                hostname=SMTP_HOST,
                port=SMTP_PORT or 465,
                username=SMTP_USERNAME or None,
                password=SMTP_PASSWORD or None,
                use_tls=True,
                tls_context=ctx,
                timeout=10,
            )
        else:                                   # Submission 587 + STARTTLS
            await aiosmtplib.send(
                msg,
                hostname=SMTP_HOST,
                port=SMTP_PORT or 587,
                username=SMTP_USERNAME or None,
                password=SMTP_PASSWORD or None,
                start_tls=True,
                tls_context=ctx,
                timeout=10,
            )
        email_sent = True

    except Exception as e:
        import logging
        logging.error("SMTP error: %s", e, exc_info=True)

    # ← все отступы вернулись на уровень функции
    return {"lead_id": lead_id, "email_sent": email_sent}
