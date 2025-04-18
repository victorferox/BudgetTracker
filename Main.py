import sqlite3
from tkinter import messagebox
from tkinter import *
import GUI

def create_database():
    with sqlite3.connect("budget_tracker.db") as conn:
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
        with sqlite3.connect("budget_tracker.db") as conn:
            conn.execute("INSERT INTO transactions (date, description, category, amount) VALUES (?, ?, ?, ?)",
                         (date, description, category, amount))
        messagebox.showinfo(title='Information', message="Transaction has been added")
    except Exception as e:
        messagebox.showerror("Transaction ID doesn't exist.")

def view_transactions(sort_by=None, sort_order='DESC', filter_category=None):
    with sqlite3.connect("budget_tracker.db") as conn:
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
            query += " ORDER BY id DESC" # Default ordering

        cursor.execute(query, tuple(params))
        transactions = cursor.fetchall()

        total_income = sum(t[4] for t in transactions if t[4] > 0)
        total_expenses = sum(abs(t[4]) for t in transactions if t[4] < 0)
        net_balance = total_income + sum(t[4] for t in transactions if t[4] < 0)

        GUI.view_transactions_gui(transactions, total_income, total_expenses, net_balance)| Category: {transaction[3]} | Description: {transaction[2]}\n")

def delete_transaction(transaction_number):
    try:
        transaction_number = int(transaction_number)
        with sqlite3.connect("budget_tracker.db") as conn:
            conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_number,))
        messagebox.showinfo(title='Information', message='The transaction had been deleted')
    except ValueError:
        messagebox.showerror("Transaction ID is invalid")

def update_transaction(transaction_number, date, description, category, amount):
    try:
        transaction_number = int(transaction_number)
        with sqlite3.connect("budget_tracker.db") as conn:
            conn.execute('''
                UPDATE transactions SET date = ?, description = ?, category = ?, amount = ? WHERE id = ?
            ''', (date, description, category, amount, transaction_number))
        messagebox.showinfo(title='Information', message="Transaction has been updated")
    except Exception as e:
        messagebox.showerror("Transaction ID doesn't exist")

if __name__ == "__main__":
    GUI.main_gui() 
