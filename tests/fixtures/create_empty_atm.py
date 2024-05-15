import pytest

from src.atm import ATM


@pytest.fixture()
def atm():
    return ATM()
