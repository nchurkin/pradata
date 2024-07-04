from models.queries import Sku


def test_sku_producer_id():
    sku = Sku(
        id='1970324837004321',
        name='Тарталетки круг 7 (коричневая), 50*25 мм (1000/20 000 штук)',
        barcode='0000'
    )

    assert sku.producer_id == '7 (кор)0000'
    assert sku.unit_id == 1


def test_sku_producer_unknown_id():
    sku = Sku(
        id='123',
        name='456',
        barcode='0000'
    )

    assert sku.producer_id == ''
    assert sku.unit_id == 1
