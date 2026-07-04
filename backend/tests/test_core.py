from app.core.settings import settings
from app.core.constants import APP_NAME


def test_settings():
    assert settings.APP_NAME == "RED AI"


def test_constants():
    assert APP_NAME == "RED AI"