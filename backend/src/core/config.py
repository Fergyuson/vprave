from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]   # …/project_root
print(BASE_DIR)
print(BASE_DIR / ".env")
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


class Bitrix24Config(BaseModel):
    webhook_url: str           = Field(default="")


class SMTPConfig(BaseModel):
    host: str                  = Field(default="smtp.mailgun.org")
    port: int                  = Field(default=587)
    username: str              = Field(default="")
    password: str              = Field(default="")
    use_implicit_tls: bool     = Field(default=False)


class MailConfig(BaseModel):
    from_address: str          = Field(default="leads@e-devservice.ru")
    to_address: str            = Field(default="leads-control@e-devservice.ru")
    bcc_addresses: list[str]   = Field(default_factory=lambda: ["cto@e-devservice.ru", "owner@e-devservice.ru"])


class ProjectConfig(BaseModel):
    name: str                  = Field(default="DevService — лендинг заявок")


class Settings(BaseSettings):
    log:          LogConfig    = Field(default_factory=LogConfig)
    server:       ServerConfig = Field(default_factory=ServerConfig)
    amocrm: AmoCRMConfig       = Field(default_factory=AmoCRMConfig)
    bitrix24: Bitrix24Config   = Field(default_factory=Bitrix24Config)
    smtp: SMTPConfig           = Field(default_factory=SMTPConfig)
    mail: MailConfig           = Field(default_factory=MailConfig)
    project: ProjectConfig     = Field(default_factory=ProjectConfig)
    database_url: str          = Field(default="sqlite:///./test.db")

    model_config = SettingsConfigDict(
        env_file               =  BASE_DIR / ".env",
        env_file_encoding      = "utf-8",
        env_prefix             = "BACKEND__",
        env_nested_delimiter   = "__",
        extra                  = "ignore",
    )


settings = Settings()
print(settings.model_dump())
