Модуль сбора данных о движениях товаров, остатках и т.д. в формате PRADATA из БД ERP системы и отправкой в API поставщика.

Установка:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install setuptools --upgrade
pip install -r requirements.txt
```
Для запуска необходимо установить значения переменных окружения в .env файле.

Использование:
```powershell
python main.py --date_start "2024-01-01" --date_end "2024-01-10"
# или так:
python main.py --date_start "2024-01-01" --date_end "2024-01-10" --upload
# можно без указания периода:
python main.py --upload
```
