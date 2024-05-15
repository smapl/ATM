from collections import Counter

from fixtures.create_atm_with_exist_banknotes import atm as atm_with_banknotes
from fixtures.create_empty_atm import atm

from src.atm import ATM


def test_put_banknote(atm: ATM):
    atm.put_money(banknote=100, amount=1)

    assert atm.total_money == 100
    assert atm.vault == Counter({100: 1})


def test_put_several_different_banknotes(atm: ATM):
    atm.put_money(banknote=100, amount=1)
    atm.put_money(banknote=500, amount=2)
    atm.put_money(banknote=2000, amount=1)
    atm.put_money(banknote=5000, amount=1)

    assert atm.total_money == 8100
    assert atm.vault == Counter({100: 1, 500: 2, 2000: 1, 5000: 1})


def test_unknown_banknote(atm: ATM):
    try:
        atm.put_money(banknote=13, amount=1)
    except ValueError as ex:
        assert ex.args[0] == 'Неизвестная банкнота'


def test_error_type_for_banknote(atm: ATM):
    try:
        atm.put_money(banknote='aaa', amount=1)
    except TypeError as ex:
        assert ex.args[0] == 'Передан неверный тип данных'


def test_banknote_amount_is_negative(atm: ATM):
    try:
        atm.put_money(banknote=10, amount=-1)
    except ValueError as ex:
        assert ex.args[0] == 'Количество переданных банкнот должно быть больше нуля'


def test_banknote_amount_is_null(atm: ATM):
    try:
        atm.put_money(banknote=10, amount=0)
    except ValueError as ex:
        assert ex.args[0] == 'Количество переданных банкнот должно быть больше нуля'


def test_put_to_atm_with_banknotes(atm_with_banknotes: ATM):
    money_before_operation = atm_with_banknotes.total_money
    atm_with_banknotes.put_money(banknote=1000, amount=1)

    assert atm_with_banknotes.total_money == money_before_operation + 1000
    assert atm_with_banknotes.vault == Counter({10: 3, 50: 2, 100: 4, 500: 2, 1000: 3, 2000: 1, 5000: 1})
