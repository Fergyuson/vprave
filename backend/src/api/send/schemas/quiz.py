from pydantic import BaseModel, Field


class QuizForm(BaseModel):
    # ────────────────── основные поля ──────────────────
    phone: str = Field(..., alias="phone")                           # Номер_телефона
    debt_types: list[str] = Field(..., alias="Какие_у_Вас_долги?")    # Какие_у_Вас_долги?
    has_overdue: str = Field(..., alias="Есть_ли_просрочки_по_выплатам?")  # Есть_ли_просрочки_по_выплатам?
    debt_amount: str = Field(..., alias="Какая_сумма_задолженности?")      # Какая_сумма_задолженности?

    # ────────────────── UTM-метки ──────────────────
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None

    class Config:
        validate_by_name = True
