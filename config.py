from pathlib import Path

from models.settings import Settings

settings = Settings()

sql_path = Path(__file__).parent.resolve() / 'sql'
