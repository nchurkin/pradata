import pytest

from models.queries import Sku, Delivery, Stock, Receive, Cancellation
from utils import get_model_data_from_csv


@pytest.fixture(scope='module')
def data(out_path):
    return dict(
        sku=get_model_data_from_csv(out_path / 'sku.csv', Sku),
        delivery=get_model_data_from_csv(out_path / 'delivery.csv', Delivery),
        stocks=get_model_data_from_csv(out_path / 'stocks.csv', Stock),
        receive=get_model_data_from_csv(out_path / 'receive.csv', Receive),
        cancellations=get_model_data_from_csv(out_path / 'cancellations.csv', Cancellation),
    )


def test_sku_id_in_facts_files(data):
    all_sku_id = {item.id for item in data['sku']}
    sku_id_in_delivery = {item.sku_id for item in data['delivery']}
    sku_id_in_stocks = {item.sku_id for item in data['stocks']}
    sku_id_in_receive = {item.sku_id for item in data['receive']}
    sku_id_cancellation_data = {item.sku_id for item in data['cancellations']}

    for sku_id in sku_id_in_delivery:
        assert sku_id in all_sku_id

    for sku_id in sku_id_in_stocks:
        assert sku_id in all_sku_id

    for sku_id in sku_id_in_receive:
        assert sku_id in all_sku_id

    for sku_id in sku_id_cancellation_data:
        assert sku_id in all_sku_id


def test_sum_check(data, date_start, date_end):
    for sku in data['sku']:
        incoming = [x.qty for x in data['stocks'] if x.sku_id == sku.id and x.date == date_start]
        incoming_sum = sum(incoming)

        delivery = [x.qty for x in data['delivery'] if x.sku_id == sku.id and x.qty != 0 and x.date > date_start]
        delivery_sum = sum(delivery)

        receive = [x.qty for x in data['receive'] if x.sku_id == sku.id and x.qty != 0 and x.date > date_start]
        receive_sum = sum(receive)

        cancellations = [x.qty for x in data['cancellations'] if
                         x.sku_id == sku.id and x.qty != 0 and x.date > date_start]
        cancellations_sum = sum(cancellations)

        outgoing = [x.qty for x in data['stocks'] if x.sku_id == sku.id and x.date == date_end]
        outgoing_sum = sum(outgoing)

        assert incoming_sum - delivery_sum + receive_sum + cancellations_sum == outgoing_sum, f'{sku=}'
