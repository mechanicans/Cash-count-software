import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

from config import *

class CashLedgerGUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(bg=BG_COLOR)

        self.count_vars = {}
        self.amount_labels = {}
        self.ref_amount_labels = {}

        self.expense_var = tk.StringVar(value="0")
        self.total_cash_var = tk.StringVar(value="₹0")
        self.net_cash_var = tk.StringVar(value="₹0")

        self.current_date = tk.StringVar(
            value=datetime.now().strftime("%Y-%m-%d")
            )

        yesterday = datetime.now() - timedelta(days=1)
        self.reference_date = tk.StringVar(
            value=yesterday.strftime("%Y-%m-%d")
            )

        self.create_header()
        self.create_main_panels()
        self.create_difference_panel()
        self.create_bottom_buttons()
        self.update_totals()

    # -------------------------------------------------

    def create_header(self):
        header = tk.Frame(
            self,
            bg=HEADER_COLOR,
            height=60
            )
        header.pack(fill="x")

        tk.Label(
            header,
            text=APP_TITLE,
            font=FONT_TITLE,
            fg="white",
            bg=HEADER_COLOR
            ).pack(pady=12)

    # -------------------------------------------------

    def create_main_panels(self):
        container = tk.Frame(
            self,
            bg=BG_COLOR
            )
        container.pack(
            fill="x",
            expand=True,
            padx=10,
            pady=10
            )

        self.create_current_panel(container)
        self.create_reference_panel(container)
        self.create_chart_panel(container)

    # -------------------------------------------------

    def create_current_panel(self, parent):
        frame = tk.LabelFrame(
            parent,
            text="Current Entry (Editable)",
            bg=CURRENT_PANEL_COLOR,
            font=FONT_BOLD
            )
        frame.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(
            frame,
            textvariable=self.current_date,
            bg=CURRENT_PANEL_COLOR,
            font=FONT_BOLD
            ).grid(row=0, column=0, columnspan=5, pady=10)

        row = 1

        for denom in DENOMINATIONS:
            tk.Label(
                frame,
                text=f"₹{denom}",
                bg=CURRENT_PANEL_COLOR
                ).grid(row=row, column=0, sticky="w", padx=5)

            var = tk.StringVar(value="0")
            self.count_vars[denom] = var

            minus_btn = tk.Button(
                frame,
                text="-",
                width=2,
                font=FONT_BOLD,
                command=lambda d=denom: self.change_count(d, -1)
                )
            minus_btn.grid(row=row, column=1, padx=2)

            entry = tk.Entry(
                frame,
                textvariable=var,
                width=10,
                justify="center",
                font=FONT_NORMAL
                )
            entry.grid(row=row, column=2, padx=2)
            entry.bind(
                "<KeyRelease>",
                lambda e: self.update_totals()
                )

            plus_btn = tk.Button(
                frame,
                text="+",
                width=2,
                font=FONT_BOLD,
                command=lambda d=denom: self.change_count(d, 1)
                )
            plus_btn.grid(row=row, column=3, padx=2)

            amount = tk.Label(
                frame,
                text="₹0",
                bg=CURRENT_PANEL_COLOR,
                font=FONT_NORMAL
                )
            amount.grid(row=row, column=4, padx=5)

            self.amount_labels[denom] = amount

            

            row += 1

        tk.Label(
            frame,
            text="Expense",
            bg=CURRENT_PANEL_COLOR
            ).grid(row=row, column=0)

        expense_entry = tk.Entry(
            frame,
            textvariable=self.expense_var,
            width=10
            )
        expense_entry.grid(row=row, column=1)
        expense_entry.bind(
            "<KeyRelease>",
            lambda e: self.update_totals()
            )

        row += 1

        tk.Label(
            frame,
            text="Total Cash",
            bg=CURRENT_PANEL_COLOR,
            font=FONT_BOLD
            ).grid(row=row, column=0)

        tk.Label(
            frame,
            textvariable=self.total_cash_var,
            bg=CURRENT_PANEL_COLOR,
            font=FONT_BOLD
            ).grid(row=row, column=1)

        row += 1

        tk.Label(
            frame,
            text="Net Cash",
            bg=CURRENT_PANEL_COLOR,
            font=FONT_BOLD
            ).grid(row=row, column=0)

        tk.Label(
            frame,
            textvariable=self.net_cash_var,
            bg=CURRENT_PANEL_COLOR,
            font=FONT_BOLD
            ).grid(row=row, column=1)

    # -------------------------------------------------

    def create_reference_panel(self, parent):
        frame = tk.LabelFrame(
            parent,
            text="Reference Entry (Read Only)",
            bg=REFERENCE_PANEL_COLOR,
            font=FONT_BOLD
            )
        frame.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(
            frame,
            textvariable=self.reference_date,
            bg=REFERENCE_PANEL_COLOR,
            font=FONT_BOLD
            ).grid(row=0, column=0, columnspan=2, pady=10)

        row = 1

        for denom in DENOMINATIONS:
            tk.Label(
                frame,
                text=f"₹{denom}",
                bg=REFERENCE_PANEL_COLOR
                ).grid(row=row, column=0, sticky="w")

            lbl = tk.Label(
                frame,
                text="₹0",
                bg=REFERENCE_PANEL_COLOR
                )
            lbl.grid(row=row, column=1)
            self.ref_amount_labels[denom] = lbl

            row += 1

    # -------------------------------------------------

    def create_chart_panel(self, parent):
        frame = tk.LabelFrame(
            parent,
            text="Cash Composition",
            bg=CURRENT_PANEL_COLOR,
            font=FONT_BOLD
            )
        frame.pack(side="left", fill="both", expand=True, padx=5)

        self.chart_text = tk.Text(
            frame,
            width=30,
            height=12
            )
        self.chart_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
            )

    # -------------------------------------------------

    def create_difference_panel(self):
        frame = tk.LabelFrame(
            self,
            text="Difference Analysis",
            bg=BG_COLOR,
            font=FONT_BOLD
            )
        frame.pack(
            fill="x",
            padx=10,
            pady=5
            )

        self.diff_label = tk.Label(
            frame,
            text="Difference from reference will appear here.",
            bg=BG_COLOR
            )
        self.diff_label.pack(pady=5)

    # -------------------------------------------------

    def create_bottom_buttons(self):
        print("Creating buttons")
        frame = tk.Frame(
            self,
            bg=BG_COLOR
            )
        frame.pack(
            side="bottom",
            fill="x",
            pady=10
        )

        tk.Button(
            frame,
            text="Save",
            bg=SAVE_BUTTON_COLOR,
            fg="white",
            width=15
            ).pack(side="left", padx=10)

        tk.Button(
            frame,
            text="Export",
            bg=EXPORT_BUTTON_COLOR,
            fg="white",
            width=15
            ).pack(side="left", padx=10)

    # -------------------------------------------------
    def change_count(self, denom, delta):
        try:
            value = int(self.count_vars[denom].get())
        except:
            value = 0

        value += delta

        if value < 0:
            value = 0

        self.count_vars[denom].set(str(value))
        self.update_totals()

    #------------------------------------------------
    def update_totals(self):
        total = 0
        chart_data = []
    
        for denom in DENOMINATIONS:
            try:
                count = int(self.count_vars[denom].get())
            except:
                count = 0
            
            value = denom * count
            total += value
        
            self.amount_labels[denom].config(text=f"₹{value}")
            chart_data.append((denom, value))
        
        try:
            expense = float(self.expense_var.get())
        except:
            expense = 0
        
        net = total - expense
    
        self.total_cash_var.set(f"₹{total:,.0f}")
        self.net_cash_var.set(f"₹{net:,.0f}")
        self.update_chart(chart_data, total)

    # -------------------------------------------------

    def update_chart(self, chart_data, total):
        self.chart_text.delete("1.0", tk.END)

        if total == 0:
            return

        for denom, value in chart_data:
            if value == 0:
                continue

            percent = (value / total) * 100
            bars = "█" * int(percent / 5)

            self.chart_text.insert(
                tk.END, 
                f"₹{denom:<5} {bars} {percent:.1f}%\n"
            )

