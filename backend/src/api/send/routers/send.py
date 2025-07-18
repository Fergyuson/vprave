from logging import Logger

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from starlette import status

from ..schemas.quiz import QuizForm
from src.core.dependency import (
    get_bitrix,
    get_email,
    get_geo_service,
    get_logger, get_amocrm,
)
from src.services.amo import AmoCRMService
from src.services.bitrix import BitrixService
from src.services.email import EmailService
from src.services.geo import GeoService

router = APIRouter(prefix="/send", tags=["send"])


@router.post("/", response_class=JSONResponse)
async def send_lead(
        form: QuizForm,
        request: Request,
        bitrix: BitrixService = Depends(get_bitrix),
        mailer: EmailService = Depends(get_email),
        geo: GeoService = Depends(get_geo_service),
        amocrm: AmoCRMService | None = Depends(get_amocrm),
        logger: Logger = Depends(get_logger),
):
    # 1. Регион по IP
    region = await geo.get_region(request.client.host)

    # 2. Читаемый текст заявки
    quiz_text = (
        f"Какие долги: {', '.join(form.debt_types)}\n"
        f"Просрочки: {form.has_overdue}\n"
        f"Сумма: {form.debt_amount}\n"
        f"Регион: {region}"
    )

    # 3. Письмо
    html = (
            f"<b>Телефон:</b> {form.phone}<br><br>"
            + quiz_text.replace("\n", "<br>")
    )
    # await mailer.send(html)

    # 4. Дубли в Bitrix24
    # if await bitrix.is_duplicate(form.phone):
    #     logger.info("Duplicate lead %s", form.phone)
    #     return JSONResponse({"response": "duble"})

    # 5. Новый лид
    # await bitrix.add_lead(
    #     phone=form.phone,
    #     quiz_text=quiz_text,
    #     utm=form.model_dump(
    #         include={
    #             "utm_source",
    #             "utm_medium",
    #             "utm_campaign",
    #             "utm_content",
    #             "utm_term",
    #         }
    #     ),
    #     region=region,
    # )
    # 6. amoCRM
    # if amocrm:
    #     lead_id = await amocrm.create_lead(form.phone, region)
    #     await amocrm.add_note(lead_id, quiz_text)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "quiz_text": quiz_text,
            "html": html,
            "response": "ok"
        }
    )
