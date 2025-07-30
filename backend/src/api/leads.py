from fastapi import APIRouter, HTTPException, Request
import os, ssl, json
import httpx
import aiosmtplib
import urllib.parse
from email.message import EmailMessage
from ..core.config import settings
from .schemas import LeadIn, LeadOut

router = APIRouter(tags=["leads"])

def get_b24_url() -> str:
    url = settings.bitrix24.webhook_url
    if not url:
        raise RuntimeError("Переменная BITRIX_WEBHOOK_URL не установлена")
    return url

@router.post("", summary="Создать лид в Bitrix24 и отправить письмо-дубликат", response_model=LeadOut)
async def create_lead(lead: LeadIn, request: Request):
    b24_url = get_b24_url()
    import logging
    logging.getLogger(__name__).info("➡️  Bitrix URL: %s", b24_url)

    # 1) Bitrix24
    b24_payload = {
        "fields": {
            "TITLE": f"{settings.project.name}: заявка от {lead.name}",
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
    subject = f"[{settings.project.name}] Новая заявка (лид #{lead_id})"
    lines = [
        f"Проект: {settings.project.name}",
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
    msg["From"] = settings.mail.from_address
    msg["To"] = settings.mail.to_address
    if settings.mail.bcc_addresses:
        msg["Bcc"] = ", ".join(settings.mail.bcc_addresses)
    msg.set_content("\n".join(lines))

    ctx = ssl.create_default_context()
    email_sent = False
    try:
        if settings.smtp.use_implicit_tls:           # SMTPS 465
            await aiosmtplib.send(
                msg,
                hostname=settings.smtp.host,
                port=settings.smtp.port or 465,
                username=settings.smtp.username or None,
                password=settings.smtp.password or None,
                use_tls=True,
                tls_context=ctx,
                timeout=10,
            )
        else:                                       # Submission 587 + STARTTLS
            await aiosmtplib.send(
                msg,
                hostname=settings.smtp.host,
                port=settings.smtp.port or 587,
                username=settings.smtp.username or None,
                password=settings.smtp.password or None,
                start_tls=True,
                tls_context=ctx,
                timeout=10,
            )
        email_sent = True

    except Exception as e:
        import logging
        logging.error("SMTP error: %s", e, exc_info=True)

    return LeadOut(lead_id=lead_id, email_sent=email_sent)
