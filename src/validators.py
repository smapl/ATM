from functools import wraps

from src.const import ACCESS_BANKNOTES


def validate_put_money_input_data(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if kwargs:
            banknote, amount = kwargs['banknote'], kwargs['amount']
        else:
            _, banknote, amount = args

        if not isinstance(banknote, int) or not isinstance(amount, int):
            raise TypeError('Передан неверный тип данных')

        if amount <= 0:
            raise ValueError('Количество переданных банкнот должно быть больше нуля')

        if banknote not in ACCESS_BANKNOTES:
            raise ValueError('Неизвестная банкнота')

        res = func(*args, **kwargs)
        return res

    return inner


def validate_get_money_input_data(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if kwargs:
            amount_money = kwargs['amount_money']
        else:
            _, amount_money = args

        if not isinstance(amount_money, int):
            raise TypeError('Передан неверный тип данных')

        if amount_money <= 0:
            raise ValueError('Количество переданных банкнот должно быть больше нуля')

        res = func(*args, **kwargs)
        return res

    return inner
