import re

import httpx

from src.core.logger import logging

_PHONE_RE = re.compile(r"\D")


def _digits(phone: str) -> str:
    return _PHONE_RE.sub("", phone)


class BitrixService:
    def __init__(self, webhook: str, src_web: int, src_yandex: int):
        self._url = webhook.rstrip("/")
        self._src_web = src_web
        self._src_yd = src_yandex

    async def _post(self, method: str, payload: dict):
        async with httpx.AsyncClient(verify=False) as c:
            r = await c.post(f"{self._url}/{method}.json",
                             json=payload, timeout=12.0)
            r.raise_for_status()
            return r.json()

    # ---------- публичные методы ----------
    async def is_duplicate(self, phone: str) -> bool:
        data = await self._post(
            "crm.duplicate.findbycomm",
            {"filter": {"PHONE": _digits(phone)}},
        )
        return bool(data.get("result", {}).get("LEAD"))

    async def add_lead(self, *, phone: str, quiz_text: str,
                       utm: dict, region: str):
        fields = {
            "TITLE": "Заявка с сайта списать-долг-законно.рф",
            "PHONE": [{"VALUE": _digits(phone), "VALUE_TYPE": "WORK"}],
            "COMMENTS": quiz_text,
            "SOURCE_ID": self._src_yd
            if utm.get("utm_source") == "yandex_webted"
            else self._src_web,
            "UF_CRM_REGION": region,  # кастомное поле, если нужно
            **{k.upper(): v for k, v in utm.items() if v},
        }
        await self._post("crm.lead.add", {"fields": fields})
        logging.info("Bitrix lead created for %s", phone)
