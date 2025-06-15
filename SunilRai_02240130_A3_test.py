import unittest
from SunilRai_02240130_A3 import Bank, Account, InputError, TransferError  # Use your actual filename

class TestBankApp(unittest.TestCase):
    def setUp(self):
        # Set up two accounts before each test
        self.bank = Bank()
        self.bank.create_account("A1", "Alice")
        self.bank.create_account("B1", "Bob")

    def test_deposit(self):
        """Test a regular deposit."""
        self.bank.accounts["A1"].deposit(100)
        self.assertEqual(self.bank.accounts["A1"].balance, 100)

    def test_deposit_negative(self):
        """Depositing a negative amount should fail."""
        with self.assertRaises(InputError):
            self.bank.accounts["A1"].deposit(-50)

    def test_withdraw(self):
        """Withdraw should work if there's enough money."""
        self.bank.accounts["A1"].deposit(200)
        self.bank.accounts["A1"].withdraw(50)
        self.assertEqual(self.bank.accounts["A1"].balance, 150)

    def test_withdraw_too_much(self):
        """Should not let you withdraw more than you have."""
        self.bank.accounts["A1"].deposit(30)
        with self.assertRaises(TransferError):
            self.bank.accounts["A1"].withdraw(100)

    def test_withdraw_negative(self):
        """Negative withdrawals are not allowed."""
        with self.assertRaises(InputError):
            self.bank.accounts["A1"].withdraw(-10)

    def test_transfer(self):
        """Transfers between accounts should update both balances."""
        self.bank.accounts["A1"].deposit(100)
        self.bank.transfer("A1", "B1", 40)
        self.assertEqual(self.bank.accounts["A1"].balance, 60)
        self.assertEqual(self.bank.accounts["B1"].balance, 40)

    def test_transfer_invalid_accounts(self):
        """Transferring to or from an account that doesn't exist should fail."""
        with self.assertRaises(InputError):
            self.bank.transfer("A1", "C1", 10)
        with self.assertRaises(InputError):
            self.bank.transfer("C1", "A1", 10)

    def test_transfer_negative_amount(self):
        """Can't transfer negative amounts."""
        with self.assertRaises(InputError):
            self.bank.transfer("A1", "B1", -5)

    def test_transfer_not_enough_balance(self):
        """Should not transfer more than available."""
        self.bank.accounts["A1"].deposit(20)
        with self.assertRaises(TransferError):
            self.bank.transfer("A1", "B1", 100)

    def test_phone_topup(self):
        """Topping up a phone should work and remember the balance."""
        self.bank.top_up_phone("9841234567", 25)
        self.assertEqual(self.bank.phone_balances["9841234567"], 25)

    def test_phone_topup_negative(self):
        """Negative top-ups should raise an error."""
        with self.assertRaises(InputError):
            self.bank.top_up_phone("9841234567", -10)

    def test_delete_account(self):
        """Deleting an account should remove it from the bank."""
        self.bank.delete_account("B1")
        self.assertNotIn("B1", self.bank.accounts)

    def test_delete_account_nonexistent(self):
        """Trying to delete an account that doesn't exist should raise an error."""
        with self.assertRaises(InputError):
            self.bank.delete_account("C2")

    def test_deposit_to_nonexistent_account(self):
        """Should get KeyError if you try to deposit to a missing account."""
        with self.assertRaises(KeyError):
            self.bank.accounts["Z9"].deposit(10)

    def test_withdraw_from_nonexistent_account(self):
        """Should get KeyError if you try to withdraw from a missing account."""
        with self.assertRaises(KeyError):
            self.bank.accounts["Z9"].withdraw(5)

if __name__ == '__main__':
    unittest.main()

