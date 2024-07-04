import datetime

from pydantic import BaseModel, Field, computed_field, ConfigDict

from config import settings
from utils import preload_producer_sku

producer_sku = preload_producer_sku()


class Query(BaseModel):
    model_config = ConfigDict(populate_by_name=True, coerce_numbers_to_str=True)

    @computed_field(alias='id дистрибьютора')
    @property
    def company_id(self) -> int:
        return settings.company_id


class Sku(Query):
    """Товары (продукты)"""
    id: str = Field(max_length=128, alias='Код продукта дистрибьютора')
    name: str = Field(max_length=128, alias='Название продукта')
    barcode: str = Field(max_length=128, alias='Штрихкод')

    @computed_field(alias='Код продукта производителя')
    @property
    def producer_id(self) -> str:
        return producer_sku.get(self.id, '')

    @computed_field(alias='id единицы измерения продукта')
    @property
    def unit_id(self) -> int:
        return settings.unit_id


class TTOption(Query):
    """Торговые точки"""
    client_code: str = Field(max_length=128, alias='Код клиента ERP')
    client_name: str = Field(max_length=256, alias='Название клиента')
    client_addr: str = Field(max_length=256, alias='Адрес клиента')
    tt_name: str = Field(max_length=128, alias='Название ТТ')
    tt_addr: str = Field(max_length=256, alias='Адрес ТТ')
    inn: str = Field(max_length=256, alias='Код ИНН')
    segment: str = Field(max_length=256, alias='Сегмент')


class TA(Query):
    """ТА - торговые агенты"""
    ta_code: str = Field(max_length=64, alias='Код ТА')
    ta_name: str = Field(max_length=128, alias='Имя ТА')


class Delivery(Query):
    """Оборот продукции"""
    client_code: str = Field(max_length=128, alias='Код клиента ERP')
    date: datetime.date = Field(alias='Дата')
    sku_id: str = Field(max_length=128, alias='Код продукта дистрибьютора')
    qty: float = Field(alias='Количество')
    total: float = Field(alias='Сумма отгрузки')
    total_gross: float = Field(alias='Сумма отгрузки с НДС')
    ta_code: str = Field(max_length=64, alias='Код ТА')
    doc_num: str = Field(max_length=128, alias='Номер расходной накладной')


class Stock(Query):
    """Остатки продукции"""
    date: datetime.date = Field(alias='Дата')
    sku_id: str = Field(max_length=128, alias='Код продукта дистрибьютора')
    qty: float = Field(alias='Количество', default=0)


class Receive(Query):
    """Приходы дистрибьютора"""
    date: datetime.date = Field(alias='Дата')
    sku_id: str = Field(max_length=128, alias='Код продукта дистрибьютора')
    qty: float = Field(alias='Количество')
    doc_num: str = Field(max_length=128, alias='Номер накладной')


class Cancellation(Receive):
    """Другие операции"""
    pass
