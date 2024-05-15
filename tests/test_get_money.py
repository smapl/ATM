from fixtures.create_atm_with_exist_banknotes import atm


def test_get_money(atm):
    money_before_operation = atm.total_money
    vault_before_operation = atm.vault

    result = atm.get_money(1000)

    assert atm.total_money == money_before_operation - 1000

    vault_before_operation[1000] -= 1
    assert atm.vault == vault_before_operation

    assert result == {1000: 1}


def test_get_money_with_negative_amount(atm):
    try:
        atm.get_money(amount=-1)
    except ValueError as ex:
        assert ex.args[0] == 'Количество переданных банкнот должно быть больше нуля'


def test_get_money_with_null_amount(atm):
    try:
        atm.get_money(amount=0)
    except ValueError as ex:
        assert ex.args[0] == 'Количество переданных банкнот должно быть больше нуля'


def test_get_money_with_error_type(atm):
    try:
        atm.get_money(amount='aaa')
    except TypeError as ex:
        assert ex.args[0] == 'Передан неверный тип данных'
