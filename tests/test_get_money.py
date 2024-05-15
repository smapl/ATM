from fixtures.create_atm_with_exist_banknotes import atm


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


def test_get_money(atm):
    money_before_operation = atm.total_money
    vault_before_operation = atm.vault

    result = atm.get_money(1000)

    assert atm.total_money == money_before_operation - 1000

    vault_before_operation[1000] -= 1
    assert atm.vault == vault_before_operation

    assert result == {1000: 1}


def test_get_compare_money(atm):
    money_before_operation = atm.total_money
    vault_before_operation = atm.vault

    amount_get_money = 9780

    result = atm.get_money(amount_get_money)

    assert atm.total_money == money_before_operation - amount_get_money

    vault_before_operation[5000] -= 1
    vault_before_operation[2000] -= 1
    vault_before_operation[1000] -= 2
    vault_before_operation[500] -= 1
    vault_before_operation[100] -= 2
    vault_before_operation[50] -= 1
    vault_before_operation[10] -= 3

    assert atm.vault == vault_before_operation
    assert result == {10: 3, 50: 1, 100: 2, 500: 1, 1000: 2, 2000: 1, 5000: 1}


def test_get_money_more_total(atm):
    amount_get_money = 100_000
    result = atm.get_money(amount=amount_get_money)
    assert result == 'Денег недостаточно'

def test_get_money_less_min_banknote(atm):
    amount_get_money = 1
    result = atm.get_money(amount=amount_get_money)
    assert result == 'Невозможно собрать необходимую сумму с существующими купюрами'

def test_get_with_incomparable_banknotes(atm):
    amount_get_money = 190
    result = atm.get_money(amount=amount_get_money)
    assert result == 'Невозможно собрать необходимую сумму с существующими купюрами'