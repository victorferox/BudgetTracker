import unittest
import sqlite3
from Main import create_database, add_transaction, delete_transaction, update_transaction

class SimpleTestBudgetTracker(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        create_database(self.conn)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_add_transaction_simple(self):
        add_transaction("2025-04-21", "Test Add", "Random", -5.00, self.conn)
        self.cursor.execute("SELECT * FROM transactions")
        transactions = self.cursor.fetchall()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0][2], "Test Add")

    def test_delete_transaction_simple(self):
        add_transaction("2025-04-21", "Test Delete", "Random", -10.00, self.conn)
        self.cursor.execute("SELECT id FROM transactions WHERE description = 'Test Delete'")
        result = self.cursor.fetchone()
        if result:
            transaction_id = result[0]
            delete_transaction(str(transaction_id), self.conn)
            self.cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
            deleted_transaction = self.cursor.fetchone()
            self.assertIsNone(deleted_transaction)
        else:
            self.fail("Transaction delete not found during setup")

    def test_update_transaction_simple(self):
        add_transaction("2025-04-21", "Old", "Random", -20.00, self.conn)
        self.cursor.execute("SELECT id FROM transactions WHERE description = 'Old'")
        result = self.cursor.fetchone()
        if result:
            transaction_id = result[0]
            update_transaction(str(transaction_id), "2025-04-22", "New", "Random", -25.00, self.conn)
            self.cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
            updated_transaction = self.cursor.fetchone()
            self.assertEqual(updated_transaction[2], "New")
            self.assertEqual(updated_transaction[4], -25.00)
        else:
            self.fail("Transaction to update not found during setup")

    def test_summary_calculations_simple(self):
        add_transaction("2025-04-21", "Pay", "Salary", 100.00, self.conn)
        add_transaction("2025-04-21", "Food", "Expense", -30.00, self.conn)
        add_transaction("2025-04-21", "Other", "Expense", -20.00, self.conn)

        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(CASE WHEN category = 'Salary' AND amount > 0 THEN amount ELSE 0 END), "
                       "SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) "
                       "FROM transactions")
        summary = cursor.fetchone()
        total_income = summary[0] if summary[0] else 0
        total_expenses = summary[1] if summary[1] else 0

        self.assertEqual(total_income, 100.00)
        self.assertEqual(total_expenses, 50.00)

if __name__ == "__main__":
    unittest.main()