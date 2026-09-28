import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from calendar_widget import CalendarSelector
from database import save_record,load_record_dict
from export import export_cash_ledger, EXPORT_OPTIONS

from config import *

class CashLedgerGUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        #self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        # Open maximized
        self.state("zoomed")
        # Prevent the window becoming too small
        self.minsize(1350, 850)
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
        self.status_var = tk.StringVar(value="🟢 New Today's Entry")
        self.create_header()
        self.create_main_panels()
        #self.create_difference_panel()
        self.create_bottom_buttons()
        self.update_totals()
        self.load_current_record()
        self.load_reference_record()


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
            # expand=True,
            padx=10,
            pady=10
            )

        self.create_current_panel(container)
        self.create_reference_panel(container)
        self.create_chart_panel(container)

    # -------------------------------------------------

    def create_current_panel(self, parent):
        self.current_frame = tk.LabelFrame(
            parent,
            text="Current Entry (Editable)",
            bg=CURRENT_PANEL_COLOR,
            font=FONT_BOLD
            )
        self.current_frame.pack(side="left", fill="both", expand=True, padx=5)
        #frame.pack(side="left", fill="y", padx=5)

        tk.Label(
            self.current_frame, 
            text="Current Date", 
            bg=CURRENT_PANEL_COLOR, 
            font=FONT_BOLD
        ).grid(row=0, column=0, sticky="w", padx=5)

        self.current_calendar = CalendarSelector(
            self.current_frame, 
            callback=self.current_date_changed
        )
        
        self.current_calendar.grid(
            row=0, 
            column=1, 
            columnspan=3, 
            pady=10, 
            sticky="w"
        )
        self.current_calendar.set_date(
            datetime.now().date()
        )
        self.status_label =tk.Label(
            self.current_frame,
            textvariable=self.status_var,
            bg=CURRENT_PANEL_COLOR,
            fg="#1B5E20",
            font=FONT_BOLD
        )
        self.status_label.grid(
            row=1,
            column=0,
            columnspan=5,
            pady=(0,10)
        )      
        row = 2
        for denom in DENOMINATIONS:
            tk.Label(
                self.current_frame,
                text=f"₹{denom}",
                bg=CURRENT_PANEL_COLOR,
                font=FONT_NORMAL
                ).grid(row=row, column=0, sticky="w", padx=10,pady=2)

            var = tk.StringVar(value="0")
            self.count_vars[denom] = var

            minus_btn = tk.Button(
                self.current_frame,
                text="-",
                width=2,
                font=FONT_BOLD,
                command=lambda d=denom: self.change_count(d, -1)
                )
            minus_btn.grid(row=row, column=1, padx=2)

            entry = tk.Entry(
                self.current_frame,
                textvariable=var,
                width=6,
                justify="center",
                font=FONT_NORMAL
                )
            entry.grid(row=row, column=2, padx=2)
            entry.bind(
                "<KeyRelease>",
                lambda e: self.update_totals()
                )

            plus_btn = tk.Button(
                self.current_frame,
                text="+",
                width=2,
                font=FONT_BOLD,
                command=lambda d=denom: self.change_count(d, 1)
                )
            plus_btn.grid(row=row, column=3, padx=2)

            amount = tk.Label(
                self.current_frame,
                text="₹0",
                bg=CURRENT_PANEL_COLOR,
                font=FONT_NORMAL
                )
            amount.grid(row=row, column=4, padx=5)

            self.amount_labels[denom] = amount

            

            row += 1

        tk.Label(
            self.current_frame,
            text="Expense",
            bg=CURRENT_PANEL_COLOR
            ).grid(row=row, column=0)

        expense_entry = tk.Entry(
            self.current_frame,
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
            self.current_frame,
            text="Total Cash",
            bg=CURRENT_PANEL_COLOR,
            font=FONT_BOLD
            ).grid(row=row, column=0)

        tk.Label(
            self.current_frame,
            textvariable=self.total_cash_var,
            bg=CURRENT_PANEL_COLOR,
            font=FONT_BOLD
            ).grid(row=row, column=1)

        row += 1

        tk.Label(
            self.current_frame,
            text="Net Cash",
            bg=CURRENT_PANEL_COLOR,
            font=FONT_BOLD
            ).grid(row=row, column=0)

        tk.Label(
            self.current_frame,
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
        #frame.pack(side="left", fill="y", padx=5)
        tk.Label(
            frame,
            text="Reference Date",
            bg=REFERENCE_PANEL_COLOR,
            font=FONT_BOLD
        ).grid(row=0, column=0, sticky="w", padx=5)

        self.reference_calendar = CalendarSelector(
            frame,
            callback=self.reference_date_changed
        )
        yesterday = datetime.now().date() - timedelta(days=1)

        self.reference_calendar.set_date(yesterday)
        self.reference_date.set(
            yesterday.strftime("%Y-%m-%d")
        )
        self.reference_calendar.grid(
            row=0,
            column=1,
            pady=10,
            sticky="w"
        )

        row = 1

        for denom in DENOMINATIONS:
            tk.Label(
                frame,
                text=f"₹{denom}",
                bg=REFERENCE_PANEL_COLOR,
                font=FONT_NORMAL
                ).grid(row=row, column=0, sticky="w",padx=10,pady=2)

            lbl = tk.Label(
                frame,
                text="0",
                bg=REFERENCE_PANEL_COLOR,
                font=FONT_NORMAL
            )
            lbl.grid(row=row, column=1,padx=10,pady=2)
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
        #frame.pack(side="left", fill="y", padx=5)

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

    # def create_difference_panel(self):
    #     frame = tk.LabelFrame(
    #         self,
    #         text="Difference Analysis",
    #         bg=BG_COLOR,
    #         font=FONT_BOLD
    #         )
    #     frame.pack(
    #         fill="x",
    #         padx=10,
    #         pady=5
    #         )

    #     self.diff_label = tk.Label(
    #         frame,
    #         text="Difference from reference will appear here.",
    #         bg=BG_COLOR
    #         )
    #     self.diff_label.pack(pady=5)

    # -------------------------------------------------

    def create_bottom_buttons(self):
        
        frame = tk.Frame(
            self,
            bg=BG_COLOR,
            height=60
            )
        frame.pack(
            side="bottom",
            fill="x",
            pady=10
        )

        self.save_button = tk.Button(
            frame,
            text="💾 Save Today's Cash",
            command=self.save_current_record,
            bg=SAVE_BUTTON_COLOR,
            fg="white",
            width=18,
            height=2,
            font=FONT_BOLD
        )
        self.save_button.pack(
            side="left",
            padx=10
        )

        self.export_button =tk.Button(
            frame,
            text="📊 Export Excel",
            bg=EXPORT_BUTTON_COLOR,
            fg="white",
            width=18,
            height=2,
            font=FONT_BOLD,
            command=self.open_export_dialog
        )

        self.export_button.pack(
            side="left", 
            padx=10
        )

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
    #--------------------------------------------------
    def current_date_changed(self, selected_date):

        
        self.current_date.set(
            selected_date.strftime("%Y-%m-%d")
        )
        self.update_current_status(selected_date)
        self.load_current_record()
      
    #--------------------------------------------------
    def update_current_status(self, selected_date):
        today = datetime.now().date()

        if selected_date == today:

            self.status_var.set(
                "● Today's Cash Entry"
            )
            self.status_label.config(
                fg="#1B5E20"      # Green
            )
            self.save_button.config(
                text="💾 Save Today's Cash",
                bg=SAVE_BUTTON_COLOR
            )
            self.current_frame.config(
                text="Current Entry"
            )

        else:

            self.status_var.set(
                "● Editing Previous Record"
            )
            self.status_label.config(
                fg="#E67E22"      # Orange
            )

            self.save_button.config(
                text="✏️ Update Record",
                bg="#F57C00"
            )
            self.current_frame.config(
                text="Current Entry (Editing Previous Record)"
            )
        print(self.current_date.get())


    #--------------------------------------------------
    def reference_date_changed(self, selected_date):
        
        self.reference_date.set(
            selected_date.strftime("%Y-%m-%d")
        )

        self.load_reference_record()
    #-------------------------------------------------
    def save_current_record(self):

        record = {}

        record["entry_date"] = self.current_date.get()

        for denom in DENOMINATIONS:

            try:
                count = int(self.count_vars[denom].get())
            except:
                count = 0

            record[f"d{denom}"] = count

        try:
            expense = float(self.expense_var.get())
        except:
            expense = 0

        record["expense"] = expense

        record["remarks"] = ""

        total = 0

        for denom in DENOMINATIONS:
            total += denom * record[f"d{denom}"]

        record["total_cash"] = total
        record["net_cash"] = total - expense

        save_record(record)

        print("Saved Successfully")

#-------------------------------------------------------
    def load_current_record(self):

        record = load_record_dict(
            self.current_date.get()
        )

        if record is None:

            self.clear_current_panel()
            return

        for denom in DENOMINATIONS:

            self.count_vars[denom].set(
                str(record[f"d{denom}"])
            )

        self.expense_var.set(
            str(record["expense"])
        )

        self.update_totals()
# ---------------------------------------------------------
    def load_reference_record(self):

        record = load_record_dict(
            self.reference_date.get()
        )

        if record is None:
            self.clear_reference_panel()
            return

        for denom in DENOMINATIONS:

            count = record[f"d{denom}"]

            if count > 0:
                display_font = FONT_BOLD
            else:
                display_font = FONT_NORMAL

            self.ref_amount_labels[denom].config(
                text=str(count),
                font=display_font
            )
# ---------------------------------------------------------
    def clear_reference_panel(self):

        for denom in DENOMINATIONS:

            self.ref_amount_labels[denom].config(
                text="0",
            font=FONT_NORMAL
            )
#---------------------------------------------------------
    def clear_current_panel(self):
        for denom in DENOMINATIONS:
            self.count_vars[denom].set("0")

        self.expense_var.set("0")

        self.update_totals()
# ---------------------------------------------------------
    def open_export_dialog(self):

        # If export window is already open, bring it forward
        if hasattr(self, "export_window"):

            try:
                if self.export_window.winfo_exists():

                    self.export_window.lift()
                    self.export_window.focus_force()

                    return

            except tk.TclError:
                pass

    # -----------------------------------------------------
    # Create export dialog
    # -----------------------------------------------------

        self.export_window = tk.Toplevel(self)

        self.export_window.title(
            "Export Cash Ledger"
        )

        self.export_window.configure(
            bg=BG_COLOR
        )

        self.export_window.resizable(
            False,
            False
        )

    # Associate dialog with main application
        self.export_window.transient(self)

    # Proper close handling
        self.export_window.protocol(
            "WM_DELETE_WINDOW",
            self.close_export_dialog
        )

    # -----------------------------------------------------
    # Dialog size and position
    # -----------------------------------------------------

        width = 450
        height = 320

        self.update_idletasks()

        x = (
            self.winfo_rootx()
            + (self.winfo_width() // 2)
            - (width // 2)
        )

        y = (
            self.winfo_rooty()
            + (self.winfo_height() // 2)
            - (height // 2)
        )

        self.export_window.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # Keep dialog above main window
        self.export_window.lift()

    # Make dialog modal
        self.export_window.grab_set()

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

        tk.Label(
            self.export_window,
            text="Export Cash Ledger",
            font=FONT_TITLE,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            pady=(20, 15)
        )

    # -----------------------------------------------------
    # END DATE
    # -----------------------------------------------------

        tk.Label(
            self.export_window,
            text="Export ending on:",
            font=FONT_NORMAL,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack()

    # Display user-friendly date
        try:

            selected_date = datetime.strptime(
                self.current_date.get(),
                "%Y-%m-%d"
            )

            display_date = selected_date.strftime(
                "%d-%m-%Y"
            )

        except ValueError:

            display_date = self.current_date.get()

        tk.Label(
            self.export_window,
            text=display_date,
            font=FONT_BOLD,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(
            pady=(2, 15)
        )

    # -----------------------------------------------------
    # EXPORT PERIOD
    # -----------------------------------------------------

        tk.Label(
            self.export_window,
            text="Select Export Period",
            font=FONT_NORMAL,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack()

        self.export_range_var = tk.StringVar(
            value="7 Days"
        )

        export_combo = ttk.Combobox(
            self.export_window,
            textvariable=self.export_range_var,
            values=list(EXPORT_OPTIONS.keys()),
            state="readonly",
            width=20,
            font=FONT_NORMAL
        )

        export_combo.pack(
            pady=10
        )

    # -----------------------------------------------------
    # BUTTON AREA
    # -----------------------------------------------------

        button_frame = tk.Frame(
            self.export_window,
            bg=BG_COLOR
        )

        button_frame.pack(
            pady=20
        )

        tk.Button(
            button_frame,
            text="📊 Export Excel",
            command=self.run_excel_export,
            bg=EXPORT_BUTTON_COLOR,
            fg="white",
            width=15,
            height=2,
            font=FONT_BOLD
        ).pack(
            side="left",
            padx=8
        )

        tk.Button(
            button_frame,
            text="Cancel",
            command=self.close_export_dialog,
            bg="#757575",
            fg="white",
            width=10,
            height=2,
            font=FONT_BOLD
        ).pack(
            side="left",
            padx=8
        )


# ---------------------------------------------------------
    def run_excel_export(self):

        selected_range = self.export_range_var.get()

        export_cash_ledger(
            end_date_string=self.current_date.get(),
            range_name=selected_range,
            parent=self.export_window
        )


# ---------------------------------------------------------
    def close_export_dialog(self):

        if hasattr(self, "export_window"):

            try:
                self.export_window.grab_release()
            except tk.TclError:
                pass

            try:
                self.export_window.destroy()
            except tk.TclError:
                pass    