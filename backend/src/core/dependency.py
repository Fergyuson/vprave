from functools import lru_cache
from fastapi import Depends
from logging import Logger

from src.core.config import settings
from src.core.logger import logging as app_logger
from src.services.bitrix import BitrixService
from src.services.email import EmailService
from src.services.geo import GeoService
from src.services.amo import AmoCRMService


@lru_cache  # singleton
def get_settings():
    return settings


def get_logger() -> Logger:
    return app_logger


@lru_cache
def get_bitrix(settings=Depends(get_settings)) -> BitrixService:
    return BitrixService(settings.bitrix.webhook,
                         settings.bitrix.source_id_web,
                         settings.bitrix.source_id_yandex)


@lru_cache
def get_email(settings=Depends(get_settings)) -> EmailService:
    return EmailService(settings.email.mail_from, settings.email.mail_to)


@lru_cache
def get_geo_service() -> GeoService:
    return GeoService()


@lru_cache
def get_amocrm(settings=Depends(get_settings)) -> AmoCRMService | None:
    if not settings.amocrm.subdomain:
        return None  # интеграция выключена
    return AmoCRMService(
        settings.amocrm.subdomain,
        settings.amocrm.client_id,
        settings.amocrm.client_secret,
        settings.amocrm.code,
        settings.amocrm.redirect_uri,
    )
