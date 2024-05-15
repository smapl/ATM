from collections import Counter

from src.const import ACCESS_BANKNOTES
from src.validators import validate_get_money_input_data, validate_put_money_input_data


class ATM:
    __slots__ = ('_vault', '_total_money', '_reserved_banknotes')

    _vault: Counter[int, int]
    _total_money: int
    _reserved_banknotes: Counter[int, int]

    def __init__(self, vault: dict[int, int] | None = None):
        self._vault = Counter({banknote: 0 for banknote in ACCESS_BANKNOTES})

        if vault is not None:
            for banknote, amount in vault.items():
                if not isinstance(banknote, int) or not isinstance(amount, int):
                    raise TypeError('Передан неверный тип данных')

                if amount <= 0:
                    raise ValueError('Количество переданных банкнот должно быть больше нуля')

                if banknote not in ACCESS_BANKNOTES:
                    raise ValueError('Попытка инициализировать банкомат с неизвестными купюрами')

            self._vault |= vault

        self._total_money = self.__calculate_money_by_vault(self._vault)
        self._reserved_banknotes = Counter()

    @property
    def vault(self):
        return self._vault

    @property
    def total_money(self):
        return self._total_money

    @validate_put_money_input_data
    def put_money(self, banknote: int, amount: int) -> None:
        self._vault[banknote] += amount
        self._total_money += amount * banknote

    @validate_get_money_input_data
    def get_money(self, amount_money: int) -> dict[int, int] | str:
        if amount_money > self._total_money:
            return 'Денег недостаточно'

        access_vault_banknotes = sorted(self._vault.keys())
        index_max_banknote_value = 1
        process_money = amount_money
        while process_money:
            if index_max_banknote_value > len(self._vault):
                return 'Невозможно собрать необходимую сумму с существующими купюрами'

            banknote = access_vault_banknotes[-index_max_banknote_value]

            # Взяли купюру по номиналу большую чем необходимая сумма
            if process_money - banknote < 0:
                index_max_banknote_value += 1
                continue

            # Проверяем достаточно ли купюр данного номинала
            if self._vault[banknote] == self._reserved_banknotes[banknote]:
                index_max_banknote_value += 1
                continue

            # Резервируем необходимые купюры
            self._reserved_banknotes[banknote] += 1

            process_money -= banknote

        output_banknotes = {banknote: amount for banknote, amount in self._reserved_banknotes.items() if amount != 0}
        self.__update_vault_state()

        return output_banknotes

    def __calculate_money_by_vault(self, vault: dict[int, int]) -> int:
        return sum((banknote * amount for banknote, amount in vault.items()))

    def __update_vault_state(self):
        # Вычитаем из хранилища ранее зарезервированные купюры
        self._vault -= self._reserved_banknotes
        self._reserved_banknotes.clear()

        # На основе актуальных данных в хранилище купюр высчитываем новую сумму всех доступных денег
        self._total_money = self.__calculate_money_by_vault(self._vault)
