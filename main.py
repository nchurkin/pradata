import os
import shutil
from datetime import timedelta
from pathlib import Path

from loguru import logger

from config import settings, sql_path
from database import DbClient
from models.queries import Sku, TTOption, TA, Delivery, Stock, Receive, Cancellation
from utils import parse_args, get_and_save, upload_file


def export_data(path, date_start, date_end):
    logger.info(f'Сохранение по пути {path}')
    logger.info(f'Период выполнения: date_start: {date_start}, date_end: {date_end}')
    logger.info(f'Срок отчёта в днях: {settings.report_days_count}')

    report_dates = [date_start + timedelta(days=x) for x in range((date_end - date_start).days + 1)]

    with DbClient(settings.database_url) as db:
        db.invoke_file(sql_path / 'prepare/01-sku-by-supplier.sql')
        db.invoke_file(sql_path / 'prepare/02-org-segments.sql')
        db.invoke_file(sql_path / 'prepare/03-our-orgs.sql')
        db.invoke_file(sql_path / 'prepare/04-org-by-period.sql', date_start=date_start, date_end=date_end)
        db.invoke_file(sql_path / 'prepare/04-org-by-period.sql', date_start=date_start, date_end=date_end)
        db.invoke_file(sql_path / 'prepare/05-docs-by-period.sql', date_start=date_start, date_end=date_end)
        db.invoke_file(sql_path / 'prepare/06-org-w-tt-by-period.sql')

        get_and_save(db, sql_path / 'get/01-sku.sql', path / 'sku.csv', Sku)
        get_and_save(db, sql_path / 'get/02-ttoptions.sql', path / 'ttoptions.csv', TTOption)
        get_and_save(db, sql_path / 'get/03-ta.sql', path / 'ta.csv', TA)
        get_and_save(db, sql_path / 'get/04-delivery.sql', path / 'delivery.csv', Delivery)

        for date in report_dates:
            get_and_save(db, sql_path / 'get/05-stocks.sql', path / 'stocks.csv', Stock, date=date)
            get_and_save(db, sql_path / 'get/06-receive.sql', path / 'receive.csv', Receive, date=date)
            get_and_save(db, sql_path / 'get/07-cancellations.sql', path / 'cancellations.csv', Cancellation, date=date)


if __name__ == '__main__':
    args = parse_args()

    report_date = args.date_end + timedelta(days=1)
    out_path = Path(__file__).parent.resolve() / 'out' / report_date.strftime('%Y-%m-%d')
    logger.add(out_path / 'export.log', format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}', level='DEBUG')
    shutil.rmtree(out_path, ignore_errors=True)
    os.makedirs(out_path, exist_ok=True)

    export_data(path=out_path, date_start=args.date_start, date_end=args.date_end)

    if args.upload:
        files = out_path.glob('*.csv')
        for file in files:
            upload_file(file)
        pass
