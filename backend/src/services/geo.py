import httpx
from src.core.logger import logging

_SYPGEO_URL = "http://api.sypexgeo.net/json/{}"


class GeoService:
    async def get_region(self, ip: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(_SYPGEO_URL.format(ip), timeout=3.0)
                data = r.json()
            return (
                    data.get("region", {}).get("name_ru")
                    or data.get("city", {}).get("name_ru")
                    or "Не определён"
            )
        except Exception as err:
            logging.warning("Geo lookup failed: %s", err)
            return "Не определён"
