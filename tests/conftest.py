from datetime import date, timedelta
from pathlib import Path

import pytest

from database import DbClient
from config import settings


def pytest_addoption(parser):
    parser.addoption("--date_start", '--start', action="store", type=date.fromisoformat,
                     default=date.today() - timedelta(days=settings.report_days_count))
    parser.addoption("--date_end", '--end', action="store", type=date.fromisoformat,
                     default=date.today() - timedelta(days=1))


@pytest.fixture(scope="session", autouse=True)
def date_start(request):
    return request.config.getoption("--date_start")


@pytest.fixture(scope="session", autouse=True)
def date_end(request):
    return request.config.getoption("--date_end")


@pytest.fixture(scope="session", autouse=True)
def database():
    assert settings.mode == 'TEST'
    db_url = "sqlite:///:memory:"
    with DbClient(db_url) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
def out_path(date_end):
    report_date = date_end + timedelta(days=1)
    return Path(__file__).parent.parent.resolve() / 'out' / report_date.strftime('%Y-%m-%d')
