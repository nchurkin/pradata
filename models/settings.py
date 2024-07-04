from typing import Annotated

from pydantic import UrlConstraints
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    database_url: str
    report_days_count: int = 45
    company_id: int
    unit_id: int
    mode: str
    spot2d_login: str
    spot2d_password: str
    spot2d_url: Annotated[Url, UrlConstraints(allowed_schemes=["http", "https"])]
