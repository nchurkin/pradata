from pathlib import Path
from sqlalchemy import create_engine, text
from loguru import logger


class DbClient:
    def __init__(self, database_url):
        self.engine = create_engine(database_url, echo=False)
        self.connection = None

    def __enter__(self):
        self.connection = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection is not None:
            self.connection.close()

    def invoke_query(self, query_text, **kwargs):
        try:
            with self.engine.begin() as connection:
                t = text(query_text)
                result = connection.execute(t, kwargs)
                if result.cursor is not None:
                    all_rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
                    return all_rows
        except Exception as e:
            print('Ошибка выполнения SQL запроса:', e)

    def invoke_file(self, file_path, **kwargs):
        try:
            logger.info(f'Выполнение запроса: {file_path} {kwargs}')
            query_text = Path(file_path).read_text(encoding='utf-8')
            result = self.invoke_query(query_text, **kwargs)
            logger.info(f'Получено строк: {len(result or '')}')
            return result
        except Exception as e:
            print('Ошибка выполнения SQL файла:', e)

    def invoke_commands(self, commands):
        try:
            with self.engine.begin() as connection:
                for command, *kwargs in commands:
                    connection.execute(text(command), kwargs)
        except Exception as e:
            print('Ошибка выполнения команд SQL:', e)
