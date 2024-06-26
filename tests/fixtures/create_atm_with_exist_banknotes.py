import pytest

from src.atm import ATM


@pytest.fixture()
def atm():
    vault = {10: 3, 50: 2, 100: 4, 500: 2, 1000: 2, 2000: 1, 5000: 1}
    # total value = 10530
    return ATM(vault=vault)
