import argparse
import csv
import os
from datetime import date, timedelta
from pathlib import Path

from loguru import logger
from pydantic import TypeAdapter
import requests

from config import settings


def read_csv_to_dict(filename):
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        result = []
        for row in reader:
            result.append(row)
    return result


def validate(rows, model):
    adapter = TypeAdapter(list[model])
    validated_rows = adapter.validate_python(rows)
    return validated_rows


def get_model_data_from_csv(filepath, model):
    items_dict = read_csv_to_dict(filepath)
    items = validate(items_dict, model)
    return items


def write_model_data(model, model_lines, filename):
    """Дописывает в файл csv экземпляры модели, если файл существует"""
    fieldnames = list(model.model_json_schema(mode='serialization')['properties'].keys())
    mode = 'a' if os.path.exists(filename) else 'w'

    with open(filename, mode=mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_ALL)
        if mode == 'w':
            writer.writeheader()

        for line in model_lines:
            writer.writerow(line.model_dump(by_alias=True))


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--date_start', type=date.fromisoformat,
                        default=date.today() - timedelta(days=settings.report_days_count),
                        help='Дата начала в формате YYYY-MM-DD')
    parser.add_argument('--date_end', type=date.fromisoformat,
                        default=date.today() - timedelta(days=1),
                        help='Дата окончания в формате YYYY-MM-DD')
    parser.add_argument('--upload', type=bool, help='Выгружать данные на сервер?', default=False,
                        action=argparse.BooleanOptionalAction)
    parsed = parser.parse_args(args=args)
    if parsed.date_start > parsed.date_end:
        raise ValueError('date_start > date_end')
    return parsed


@logger.catch
def get_and_save(db, query_path, out_path, model, **kwargs):
    lines = db.invoke_file(query_path, **kwargs)
    validated_lines = validate(lines, model)
    write_model_data(model, validated_lines, out_path)


def preload_producer_sku():
    preload_path = Path(__file__).parent.resolve() / 'preload_data/sku.csv'

    with open(preload_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        producer_sku = {
            row['Код СКЮ дистрибьютора']: row['Код продукта производителя']
            for row in reader if row['Код СКЮ дистрибьютора'] != ''
        }

    return producer_sku


@logger.catch
def upload_file(file):
    data = {
        "__login": settings.spot2d_login,
        "__password": settings.spot2d_password,
    }
    files = {'ufile': (file.name, open(file, 'rb'), 'text/plain')}
    r = requests.post(url=settings.spot2d_url, files=files, data=data)
    r.raise_for_status()
    logger.debug(r.status_code)
    logger.debug(r.text)
