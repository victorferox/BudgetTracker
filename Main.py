import sqlite3
from tkinter import messagebox
from tkinter import *
import GUI

DATABASE_NAME = "budget_tracker.db"

def create_database():
    with sqlite3.connect(DATABASE_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL
            )
        ''')

def add_transaction(date, description, category, amount):
    try:
        amount = float(amount)
        with sqlite3.connect(DATABASE_NAME) as conn:
            conn.execute("INSERT INTO transactions (date, description, category, amount) VALUES (?, ?, ?, ?)",
                         (date, description, category, amount))
            conn.commit()
            messagebox.showinfo(title='Information', message="Transaction has been added")
    except ValueError:
        messagebox.showerror("EPlease enter a valid number")


def view_transactions(sort_by=None, sort_order='DESC', filter_category=None):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []

        if filter_category and filter_category != "All":
            query += " AND category = ?"
            params.append(filter_category)

        if sort_by == 'date':
            query += " ORDER BY date " + sort_order.upper()
        elif sort_by == 'amount':
            query += " ORDER BY amount " + sort_order.upper()
        else:
            query += " ORDER BY id DESC"

        cursor.execute(query, tuple(params))
        transactions = cursor.fetchall()

        total_income = 0
        total_expenses = 0
        for transaction in transactions:
            if transaction[3] == "Salary" and transaction[4] > 0:
                total_income += transaction[4]
            elif transaction[4] < 0:
                total_expenses += abs(transaction[4])
            elif transaction[4] > 0 and transaction[3] != "Salary":
                total_expenses += transaction[4] 
        net_balance = total_income - total_expenses

        GUI.view_transactions_gui(transactions, total_income, total_expenses, net_balance)

def delete_transaction(transaction_number):
    try:
        transaction_number = int(transaction_number)
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_number,))
            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo(title='Information', message='The transaction has been deleted')
    except ValueError:
        messagebox.showerror("Please enter a valid Transaction ID.")


def update_transaction(transaction_number, date, description, category, amount):
    try:
        transaction_number = int(transaction_number)
        amount = float(amount)
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE transactions SET date = ?, description = ?, category = ?, amount = ? WHERE id = ?
            ''', (date, description, category, amount, transaction_number))
            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo(title='Information', message="Transaction has been updated")
    except ValueError:
        messagebox.showerror("Please enter a valid transaction ID")


if __name__ == "__main__":
    GUI.main_gui()
