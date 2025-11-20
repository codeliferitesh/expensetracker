import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Personal Finance Manager - Ritesh Verma Apps")
        self.root.geometry("900x750")
        self.root.config(bg="#212121")

        self.transactions = []
        self.has_income = False  

        # --- Styling ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#212121')
        style.configure('TLabel', background='#212121', foreground='white', font=('Arial', 12))

        # --- Title ---
        title = tk.Label(root, text="💸 Income & Expense Tracker", font=("Arial", 28, "bold"), fg="#00ff99", bg="#212121")
        title.pack(pady=15)

        # --- Balance Display ---
        self.balance_var = tk.StringVar(value="Current Balance: ₹0.00")
        self.balance_label = tk.Label(root, textvariable=self.balance_var, font=("Arial", 18, "bold"), fg="#ff9900", bg="#212121")
        self.balance_label.pack(pady=5)

        # --- Input Form ---
        form_frame = ttk.Frame(root, padding="10 10 10 10")
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Date (YYYY-MM-DD):", fg="#a0a0a0", bg="#212121", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Category/Source:", fg="#a0a0a0", bg="#212121", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(form_frame, text="Amount (₹):", fg="#a0a0a0", bg="#212121", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.category_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.transaction_type_var = tk.StringVar(value='Income') 

        self.date_entry = tk.Entry(form_frame, textvariable=self.date_var, font=("Arial", 12), width=25, bg="#333333", fg="white", insertbackground='white')
        self.date_entry.grid(row=0, column=1, pady=5)

        self.expense_categories = ['Food 🍕', 'Transport 🚗', 'Shopping 🛍️', 'Bills 🧾', 'Entertainment 🎬', 'Health 🏥', 'Other ❓']
        self.income_sources = ['Salary 💵', 'Investment 📈', 'Gift 🎁', 'Other Income']
        
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=self.income_sources, state="readonly", font=("Arial", 12), width=23)
        self.category_combo.grid(row=1, column=1, pady=5)
        self.category_combo.current(0)
        
        self.amount_entry = tk.Entry(form_frame, textvariable=self.amount_var, font=("Arial", 12), width=25, bg="#333333", fg="white", insertbackground='white')
        self.amount_entry.grid(row=2, column=1, pady=5)

        # --- Radio Buttons ---
        type_frame = ttk.Frame(form_frame)
        type_frame.grid(row=3, column=0, columnspan=2, pady=5)

        self.expense_radio = tk.Radiobutton(type_frame, text="Expense", variable=self.transaction_type_var, value='Expense', bg="#212121", fg="white", selectcolor="#212121", font=("Arial", 12), command=lambda: self.update_categories(self.expense_categories))
        self.expense_radio.pack(side=tk.LEFT, padx=10)
        
        self.income_radio = tk.Radiobutton(type_frame, text="Income", variable=self.transaction_type_var, value='Income', bg="#212121", fg="white", selectcolor="#212121", font=("Arial", 12), command=lambda: self.update_categories(self.income_sources))
        self.income_radio.pack(side=tk.LEFT, padx=10)
        
        self.expense_radio.config(state=tk.DISABLED, fg="#777777")
        self.income_radio.config(state=tk.NORMAL)

        # --- Buttons ---
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        self.add_btn = tk.Button(button_frame, text="➕ Add Transaction", font=("Arial", 12, "bold"), bg="#00ff99", fg="#000", activebackground="#00cc7a", command=self.add_transaction, relief=tk.FLAT, padx=10, pady=5)
        self.add_btn.grid(row=0, column=0, padx=5)

        delete_btn = tk.Button(button_frame, text="➖ Delete Selected", font=("Arial", 12, "bold"), bg="#ff6666", fg="#000", activebackground="#cc5252", command=self.delete_transaction, relief=tk.FLAT, padx=5, pady=5)
        delete_btn.grid(row=0, column=1, padx=5)

        summary_btn = tk.Button(button_frame, text="📊 Category Summary", font=("Arial", 12, "bold"), bg="#ffcc00", fg="#000", activebackground="#ccaa00", command=self.show_category_summary, relief=tk.FLAT, padx=5, pady=5)
        summary_btn.grid(row=0, column=2, padx=5)
        
        balance_plot_btn = tk.Button(button_frame, text="📈 Balance History", font=("Arial", 12, "bold"), bg="#66ccff", fg="#000", activebackground="#52a3cc", command=self.show_balance_history, relief=tk.FLAT, padx=5, pady=5)
        balance_plot_btn.grid(row=0, column=3, padx=5)

        # --- Transaction List ---
        list_frame = ttk.Frame(root)
        list_frame.pack(padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.transaction_listbox = tk.Listbox(list_frame, font=("Courier New", 11), width=85, height=12, bg="#333333", fg="white", selectbackground="#00ff99", selectforeground="#000", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.transaction_listbox.yview)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.transaction_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        footer_label = tk.Label(root, text="Made with ❤️ by Ritesh", font=("Arial", 10, "italic"), fg="#777777", bg="#212121")
        footer_label.pack(side=tk.BOTTOM, pady=10)

        self.update_balance()

    def update_categories(self, new_values):
        self.category_combo['values'] = new_values
        self.category_combo.current(0)
        self.category_var.set(new_values[0])
        
    def calculate_balance(self):
        balance = 0.0
        for item in self.transactions:
            amount = item[2]
            trans_type = item[3]
            
            if trans_type == 'Income':
                balance += amount
            else:
                balance -= amount
        return balance

    def update_balance(self):
        current_balance = self.calculate_balance()
        fg_color = '#00ff99' if current_balance >= 0 else '#ff6666'
        self.balance_var.set(f"Current Balance: ₹{current_balance:,.2f}")
        self.balance_label.config(fg=fg_color)

    def add_transaction(self):
        date_str = self.date_var.get()
        category = self.category_var.get()
        amount_str = self.amount_var.get()
        type_ = self.transaction_type_var.get()

        if type_ == 'Expense' and not self.has_income:
            messagebox.showwarning("🚫 Income Required", "Please record your first Income before adding any Expenses!")
            self.transaction_type_var.set('Income')
            self.update_categories(self.income_sources)
            return

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            messagebox.showerror("❌ Invalid Input", f"Please check format.\nError: {e}")
            return

        self.transactions.append((date_obj, category, amount, type_))
        
        if type_ == 'Income' and not self.has_income:
            self.has_income = True
            self.expense_radio.config(state=tk.NORMAL, fg="white")
            self.income_radio.config(state=tk.NORMAL)
        
        display_amount = f"+₹{amount:,.2f}" if type_ == 'Income' else f"-₹{amount:,.2f}"
        display_text = f"{date_obj.date()} | {type_:<7} | {category[:15]:<15} | {display_amount:<15}"
        
        self.transaction_listbox.insert(tk.END, display_text)
        
        # --- FIXED COLORING LOGIC HERE ---
        # Get the index of the last item added
        last_index = self.transaction_listbox.size() - 1
        
        if type_ == 'Income':
            self.transaction_listbox.itemconfig(last_index, {'fg': '#00ff99'})
        else:
            self.transaction_listbox.itemconfig(last_index, {'fg': '#ff6666'})
        # ---------------------------------

        self.amount_var.set("")
        self.update_balance()

    def delete_transaction(self):
        try:
            selected_index = self.transaction_listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a transaction to delete.")
            return

        deleted_type = self.transactions[selected_index][3]
        
        self.transactions.pop(selected_index)
        self.transaction_listbox.delete(selected_index)
        
        if deleted_type == 'Income':
            self.has_income = any(t[3] == 'Income' for t in self.transactions)
            if not self.has_income:
                self.expense_radio.config(state=tk.DISABLED, fg="#777777")
                self.transaction_type_var.set('Income')
                self.update_categories(self.income_sources)
        
        self.update_balance()
        messagebox.showinfo("Deletion Successful", "Transaction deleted.")

    def show_category_summary(self):
        if not self.transactions:
            messagebox.showinfo("No Data", "Add some transactions first!")
            return

        expense_transactions = [t for t in self.transactions if t[3] == 'Expense']
        if not expense_transactions:
            messagebox.showinfo("No Expense Data", "Add some expenses to view the category breakdown.")
            return

        summary_by_category = {}
        for _, category, amount, _ in expense_transactions:
            summary_by_category[category] = summary_by_category.get(category, 0) + amount

        plot_win = tk.Toplevel(self.root)
        plot_win.title("📊 Expense Category Breakdown")
        plot_win.geometry("500x550")
        plot_win.config(bg="#212121")

        fig, ax = plt.subplots(figsize=(5, 5))
        categories = list(summary_by_category.keys())
        amounts_category = list(summary_by_category.values())
        
        def func(pct, allvalues):
            absolute = int(pct/100.*sum(allvalues))
            return f"{pct:.1f}%\n(₹{absolute:,.0f})"

        colors = ['#00ff99', '#ff9900', '#66ccff', '#ff6666', '#cc66ff', '#ccff66', '#999999']
        
        ax.pie(amounts_category, labels=categories, autopct=lambda pct: func(pct, amounts_category), 
               startangle=90, colors=colors[:len(categories)],
               wedgeprops={'edgecolor': 'black'},
               textprops={'color': 'white', 'fontsize': 9})
        ax.set_title("Expense Category Breakdown", fontsize=14, fontweight="bold", color='white')
        fig.patch.set_facecolor('#333333')
        
        canvas_pie = FigureCanvasTkAgg(fig, master=plot_win)
        canvas_pie.draw()
        canvas_pie.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def show_balance_history(self):
        if not self.transactions:
            messagebox.showinfo("No Data", "Add some transactions first!")
            return

        df = pd.DataFrame(self.transactions, columns=['Date', 'Category', 'Amount', 'Type'])
        df['Signed_Amount'] = df.apply(lambda row: row['Amount'] if row['Type'] == 'Income' else -row['Amount'], axis=1)
        df = df.sort_values(by='Date')
        df['Running_Balance'] = df['Signed_Amount'].cumsum()
        
        dates = df['Date']
        running_balance = df['Running_Balance']

        plot_win = tk.Toplevel(self.root)
        plot_win.title("📈 Running Balance History")
        plot_win.geometry("600x450")
        plot_win.config(bg="#212121")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(dates, running_balance, marker='o', linestyle='-', color='#66ccff', linewidth=2, markersize=4)
        ax.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.7)
        ax.set_title("Cumulative Balance Over Time", fontsize=14, fontweight="bold", color='white')
        ax.set_ylabel("Balance (₹)", color='white')
        ax.set_xlabel("Date", color='white')
        ax.tick_params(axis='x', rotation=45, colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.grid(axis='both', linestyle='--', alpha=0.5)
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')
        plt.tight_layout()

        canvas_line = FigureCanvasTkAgg(fig, master=plot_win)
        canvas_line.draw()
        canvas_line.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
