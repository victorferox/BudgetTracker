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

def view_transactions():
    with sqlite3.connect("budget_tracker.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()

    view_window = Toplevel()
    view_window.title("Transaction History")
    text_area = Text(view_window, width=60, height=10)
    text_area.pack(padx=10, pady=10)

    for transaction in transactions:
        text_area.insert(END, f"TRANSACTION ID: {transaction[0]} | Date: {transaction[1]} | Amount: {transaction[4]:.2f} | Category: {transaction[3]} | Description: {transaction[2]}\n")

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