import pytest

from app.calc import *


@pytest.fixture  # the pytest.fixture decorator is called before the test run
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account_balance():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 3, 10),
    (10, 5, 15)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_multiply():
    assert multiply(2, 5) == 10


def test_divide():
    assert divive(8, 2) == 4


def test_subtract():
    assert subtract(15, 6) == 9


def test_bank_account_init_balance(bank_account_balance):
    assert bank_account_balance.balance == 50


def test_default_acccount_balance(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdrawal(bank_account_balance):
    bank_account_balance.withdraw(25)
    assert bank_account_balance.balance == 25


def test_deposit(bank_account_balance):
    bank_account_balance.deposit(50)
    assert bank_account_balance.balance == 100


def test_interest(bank_account_balance):
    bank_account_balance.interest()
    assert round(bank_account_balance.balance, 6) == 55


# def test_bank_transaction(zero_bank_account):
#     zero_bank_account.deposit(500)
#     zero_bank_account.withdraw(300)
#     assert zero_bank_account.balance == 200
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (300, 100, 200),
    (500, 450, 50),
    (800, 200, 600)
])
# You can user the parametrize and fixture decorators to test cases like the test below
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


# How to raise an exception with pytest
def test_insufficient_balance(bank_account_balance):
    with pytest.raises(InsufficientFund):
        bank_account_balance.withdraw(100)
