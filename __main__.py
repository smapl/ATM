ACCESS_BANKNOTES = (10, 50, 100, 200, 500, 1000, 2000, 5000)

class ATM:
    def __init__(self, vault: dict[int, int] | None = None):
        self._vault = {banknote: 0 for banknote in ACCESS_BANKNOTES}
        if vault is not None:
            for banknote in vault:
                if banknote not in ACCESS_BANKNOTES:
                    raise ValueError('Попытка инициализировать банкомат с несуществующими купюрами')
            self._vault |= vault

        self._total_money = 0

    def put_money(self, banknote: int, count: int) -> None:
        if banknote not in ACCESS_BANKNOTES:
            return 'Неизвестная банкнота'

        self._vault[banknote] += count
        self._total_money += count * banknote

    def get_money(self, amount_money: int) -> dict[int, int] | str:
        if amount_money > self._total_money:
            return 'Денег недостаточно'

        reserved_banknotes = {}
        access_vault_banknotes = sorted(self._vault.keys())
        index_max_banknote_value = 1
        process_money = amount_money
        while process_money:
            banknote = access_vault_banknotes[-index_max_banknote_value]
            # Взяли купюру по номиналу большую чем необходимая сумма
            if process_money - banknote < 0:
                index_max_banknote_value += 1
                continue

            # Проверяем достаточно ли купюр одного типа
            if self._vault[banknote] == reserved_banknotes.setdefault(banknote, 0):
                index_max_banknote_value += 1
                if index_max_banknote_value > len(self._vault):
                    return 'Невозможно собрать необходимую сумму с существующими купюрами'

                continue

            # Резервируем необходимые купюры
            reserved_banknote_count = reserved_banknotes.setdefault(banknote, 0)
            reserved_banknotes[banknote] = reserved_banknote_count + 1

            process_money -= banknote

        # Вычитаем из хранилища ранее зарезервированные купюры
        for banknote, count_banknote in reserved_banknotes.items():
            vault_banknote_count = self._vault[banknote]
            self._vault[banknote] = vault_banknote_count - count_banknote

        # правильнее написать приватный метод, который будет актуализировать тотал на основе купюр
        self._total_money -= amount_money

        return {banknote: count for banknote, count in reserved_banknotes.items() if count != 0}


if __name__ == '__main__':
    atm = ATM()
    atm.put_money(banknote=2000, count=1)
    atm.put_money(banknote=1000, count=1)
    atm.put_money(banknote=500, count=1)
    atm.put_money(banknote=100, count=3)
    atm.put_money(banknote=50, count=2)
    atm.put_money(banknote=10, count=5)
    # добавили 3950
    print(atm.get_money(amount_money=1730))
    print()

    print(atm.get_money(amount_money=1))