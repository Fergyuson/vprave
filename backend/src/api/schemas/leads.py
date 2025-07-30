from pydantic import BaseModel, EmailStr, field_validator


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


class LeadOut(BaseModel):
    lead_id: int
    email_sent: bool 