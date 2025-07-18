import json
import time
from pathlib import Path
import httpx
from src.core.logger import logging

TOKEN_PATH = (
    Path(__file__).resolve().parent.parent.parent / "token.json"
)  # был TOKEN.txt


class AmoCRMService:
    def __init__(
        self,
        subdomain: str,
        client_id: str,
        client_secret: str,
        code: str,
        redirect: str,
    ):
        self.subdomain = subdomain
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.redirect = redirect
        self._access_token: str = ""

    # ────────────────────────────────────────────── публичные ──────────────────
    async def create_lead(self, phone: str, region: str) -> int | None:
        await self._ensure_token()
        url = self._api("leads/complex")
        payload = [
            {
                "name": 'Заявка с "списать-долг-законно.рф"',
                "pipeline_id": 7_529_150,
                "status_id": 62_403_622,
                "tags_to_add": [{"name": "решение"}],
                "_embedded": {
                    "contacts": [
                        {
                            "name": "CLIENT",
                            "custom_fields_values": [
                                {
                                    "field_code": "PHONE",
                                    "values": [{"value": phone, "enum_code": "WORK"}],
                                },
                                {
                                    "field_id": 366_891,
                                    "values": [{"value": region}],
                                },
                            ],
                        }
                    ]
                },
            }
        ]
        data = await self._post(url, payload)
        return data["_embedded"]["leads"][0]["id"]

    async def add_note(self, lead_id: int, text: str) -> None:
        await self._ensure_token()
        url = self._api(f"leads/{lead_id}/notes")
        await self._post(url, [{"note_type": "common", "params": {"text": text}}])

    # ────────────────────────────────────────────── служебные ──────────────────
    def _api(self, path: str) -> str:
        return f"https://{self.subdomain}.amocrm.ru/api/v4/{path}"

    async def _post(self, url: str, payload: list | dict):
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient() as c:
            r = await c.post(url, headers=headers, json=payload, timeout=15.0)
        r.raise_for_status()
        return r.json()

    # ---------- работа с OAuth ----------

    async def _ensure_token(self) -> None:
        """Проверяем, что access_token жив; иначе обновляем/берём первый раз"""
        if self._token_valid():
            return

        if TOKEN_PATH.exists():
            refresh = json.loads(TOKEN_PATH.read_text())["refresh_token"]
            oauth_payload = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": refresh,
                "redirect_uri": self.redirect,
            }
        else:
            oauth_payload = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "authorization_code",
                "code": self.code,
                "redirect_uri": self.redirect,
            }

        url = f"https://{self.subdomain}.amocrm.ru/oauth2/access_token"
        async with httpx.AsyncClient() as c:
            r = await c.post(url, json=oauth_payload, timeout=15.0)
        r.raise_for_status()
        token = r.json()

        # сохраняем красиво
        token_json = {
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "expires_at": time.time() + token["expires_in"],
        }
        TOKEN_PATH.write_text(json.dumps(token_json, ensure_ascii=False, indent=2))
        logging.info("amoCRM token saved → %s", TOKEN_PATH)

        self._access_token = token_json["access_token"]

    def _token_valid(self) -> bool:
        """True, если в файле есть живой access_token"""
        if not TOKEN_PATH.exists():
            return False
        try:
            data = json.loads(TOKEN_PATH.read_text())
            if data["expires_at"] > time.time() + 60:  # запас 60 с
                self._access_token = data["access_token"]
                return True
        except (ValueError, KeyError):
            logging.warning("Bad token.json format — re-auth")
        return False
