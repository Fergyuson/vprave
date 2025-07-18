from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]   # …/backend

class LogConfig(BaseModel):
    level: str             = Field(default="INFO")
    dir:   Path            = Field(default=Path("logs"))
    filename:  str         = Field(default="app.log")
    fmt:   str             = Field(default="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    rotation_when: str     = Field(default="midnight")
    rotation_interval: int = Field(default=1)
    retention_days: int    = Field(default=7)


class ServerConfig(BaseModel):
    host:  str             = Field(default="0.0.0.0")
    port:  int             = Field(default=8000)
    debug: bool            = Field(default=False)
    reload: bool           = Field(default=False)


class AmoCRMConfig(BaseModel):
    subdomain: str             = Field(default="webted")
    client_id: str             = Field(default="872d0b9f...")
    client_secret: str         = Field(default="tFxbo0...")
    code: str                  = Field(default="def50200...")
    redirect_uri: str          = Field(default="https://webted.amocrm.ru/")

class Settings(BaseSettings):
    app_name:     str          = Field(default="MyFastAPIApp")
    log:          LogConfig    = Field(default_factory=LogConfig)
    server:       ServerConfig = Field(default_factory=ServerConfig)
    amocrm: AmoCRMConfig       = Field(default_factory=AmoCRMConfig)
    database_url: str          = Field(default="sqlite:///./test.db")

    model_config = SettingsConfigDict(
        env_file               =  BASE_DIR / ".env",
        env_file_encoding      = "utf-8",
        env_prefix             = "BACKEND__",
        env_nested_delimiter   = "__",
        extra                  = "ignore",
    )


settings = Settings()