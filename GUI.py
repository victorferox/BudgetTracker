from tkinter import *
from tkinter import messagebox
import Main
from tkinter import ttk  # Import missing for Combobox

CATEGORIES = ["Food", "Transportation", "Entertainment", "Utilities", "Salary", "Other"]

def add_transaction_gui():
    add_window = Toplevel()
    add_window.title("Add a new transaction")

    Label(add_window, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
    date_entry = Entry(add_window)
    date_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(add_window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
    description_entry = Entry(add_window)
    description_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(add_window, text="Category:").grid(row=2, column=0, padx=5, pady=5)
    category_combo = ttk.Combobox(add_window, values=CATEGORIES) # Use Combobox
    category_combo.set(CATEGORIES[0]) # Set a default
    category_combo.grid(row=2, column=1, padx=5, pady=5)

    Label(add_window, text="Amount:").grid(row=3, column=0, padx=5, pady=5)
    amount_entry = Entry(add_window)
    amount_entry.grid(row=3, column=1, padx=5, pady=5)

    def add_button_click():
        try:
            amount = float(amount_entry.get())
            Main.add_transaction(date_entry.get(), description_entry.get(), category_combo.get(), amount)
            add_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the amount.")

    Button(add_window, text="Add", command=add_button_click).grid(row=4, column=0, columnspan=2, pady=10)

def delete_transaction_gui():
    delete_window = Toplevel()
    delete_window.title("Delete a transaction")

    Label(delete_window, text="Transaction ID:").grid(row=0, column=0, padx=5, pady=5)
    id_entry = Entry(delete_window)
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    def delete_button_click():
        Main.delete_transaction(id_entry.get())
        delete_window.destroy()

    Button(delete_window, text="Delete", command=delete_button_click).grid(row=1, column=0, columnspan=2, pady=10)

def update_transaction_gui():
    update_window = Toplevel()
    update_window.title("Update a transaction")

    Label(update_window, text="Transaction ID:").grid(row=0, column=0, padx=5, pady=5)
    id_entry = Entry(update_window)
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(update_window, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
    date_entry = Entry(update_window)
    date_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(update_window, text="Description:").grid(row=2, column=0, padx=5, pady=5)
    description_entry = Entry(update_window)
    description_entry.grid(row=2, column=1, padx=5, pady=5)

    Label(update_window, text="Category:").grid(row=3, column=0, padx=5, pady=5)
    category_combo = ttk.Combobox(update_window, values=CATEGORIES) # Use Combobox
    category_combo.grid(row=3, column=1, padx=5, pady=5)

    Label(update_window, text="Amount:").grid(row=4, column=0, padx=5, pady=5)
    amount_entry = Entry(update_window)
    amount_entry.grid(row=4, column=1, padx=5, pady=5)

    def update_button_click():
        try:
            amount = float(amount_entry.get())
            Main.update_transaction(id_entry.get(), date_entry.get(), description_entry.get(), category_combo.get(), amount) 
            update_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the amount.")

   
    Button(update_window, text="Update", command=update_button_click).grid(row=5, column=0, columnspan=2, pady=10)

def view_transactions_gui(transactions, total_income=0, total_expenses=0, net_balance=0):
    view_window = Toplevel()
    view_window.title("Transaction History")

    filter_frame = Frame(view_window)
    filter_frame.pack(pady=5)

    Label(filter_frame, text="Filter by Category:").pack(side=LEFT, padx=5)
    categories = ["All"] + CATEGORIES 
    category_combo = ttk.Combobox(filter_frame, values=categories)
    category_combo.set("All")
    category_combo.pack(side=LEFT, padx=5)

    filter_button = Button(filter_frame, text="Filter",
                           command=lambda: Main.view_transactions(filter_category=category_combo.get()))
    filter_button.pack(side=LEFT, padx=5)

    sort_frame = Frame(view_window)
    sort_frame.pack(pady=5)

    sort_by = StringVar(value="id")
    sort_order = StringVar(value="DESC")

    Label(sort_frame, text="Sort by:").pack(side=LEFT, padx=5)
    sort_by_combo = ttk.Combobox(sort_frame, values=["Date", "Amount"])
    sort_by_combo.set("Date")
    sort_by_combo.pack(side=LEFT, padx=5)

    Label(sort_frame, text="Order:").pack(side=LEFT, padx=5)
    order_combo = ttk.Combobox(sort_frame, values=["Ascending", "Descending"])
    order_combo.set("Descending")
    order_combo.pack(side=LEFT, padx=5)

    sort_button = Button(sort_frame, text="Sort",
                         command=lambda: Main.view_transactions(
                             sort_by=sort_by_combo.get().lower(),
                             sort_order="ASC" if order_combo.get() == "Ascending" else "DESC",
                             filter_category=category_combo.get()
                         ))
    sort_button.pack(side=LEFT, padx=5)

    text_area = Text(view_window, width=70, height=15)
    text_area.pack(padx=10, pady=10)
    text_area.insert(END, "TRANSACTION ID | Date       | Amount    | Category      | Description\n")
    text_area.insert(END, "-----------------------------------------------------------------------\n")
    for transaction in transactions:
        text_area.insert(END, f"{transaction[0]:<14} | {transaction[1]:<10} | {transaction[4]:<9.2f} | {transaction[3]:<13} | {transaction[2]}\n")

    summary_text = f"\n--- Summary ---\nTotal Income: ${total_income:.2f}\nTotal Expenses: ${total_expenses:.2f}\nNet Balance: ${net_balance:.2f}"
    text_area.insert(END, summary_text)
    text_area.config(state=DISABLED)

def main_gui():
    Main.create_database()

    root = Tk()
    root.title("Budget Tracker")
    root.geometry('350x200')
    Label(root, text="Budget Tracker").grid(column=0, row=0, columnspan=2, padx=10, pady=10)

    button_font = ("Times New Roman", 12)

    Button(root, text="Add a new transaction", command=add_transaction_gui, font=button_font).grid(column=0, row=1, padx=10, pady=5, sticky="ew")
    Button(root, text="View all transactions", command=Main.view_transactions, font=button_font).grid(column=0, row=2, padx=10, pady=5, sticky="ew")
    Button(root, text="Delete a transaction", command=delete_transaction_gui,font=button_font).grid(column=0, row=3, padx=10, pady=5, sticky="ew")
    Button(root, text="Update a transaction", command=update_transaction_gui, font=button_font).grid(column=0, row=4, padx=10, pady=5, sticky="ew")
    Button(root, text="Exit", command=root.quit, font=button_font).grid(column=0, row=5, padx=10, pady=5, sticky="ew")



    root.mainloop()
