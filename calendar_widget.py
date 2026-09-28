import tkinter as tk
from tkinter import ttk
from datetime import date, datetime, timedelta
import calendar


class CalendarSelector(tk.Frame):

    def __init__(self, master, callback=None, **kwargs):
        super().__init__(master, bg=master["bg"])

        self.callback = callback

        today = date.today()

        # -------------------------
        # Variables
        # -------------------------
        self.day_var = tk.IntVar(value=today.day)
        self.month_var = tk.StringVar(value=calendar.month_name[today.month])
        self.year_var = tk.IntVar(value=today.year)

        # -------------------------
        # Previous Day Button
        # -------------------------
        self.prev_btn = tk.Button(
            self,
            text="◀",
            width=2,
            font=("Segoe UI", 10, "bold"),
            bg="#4E944F",
            fg="white",
            relief="raised",
            command=self.previous_day
        )
        self.prev_btn.grid(row=0, column=0, padx=(0, 5))

        # -------------------------
        # Day Combobox
        # -------------------------
        self.day_box = ttk.Combobox(
            self,
            width=5,
            state="readonly",
            textvariable=self.day_var
        )
        self.day_box.grid(row=0, column=1)

        # -------------------------
        # Month Combobox
        # -------------------------
        self.month_box = ttk.Combobox(
            self,
            width=11,
            state="readonly",
            textvariable=self.month_var,
            values=list(calendar.month_name)[1:]
        )
        self.month_box.grid(row=0, column=2, padx=5)

        # -------------------------
        # Year Combobox
        # -------------------------
        self.year_box = ttk.Combobox(
            self,
            width=7,
            state="readonly",
            textvariable=self.year_var,
            values=list(range(2020, 2051))
        )
        self.year_box.grid(row=0, column=3)

        # -------------------------
        # Next Day Button
        # -------------------------
        self.next_btn = tk.Button(
            self,
            text="▶",
            width=2,
            font=("Segoe UI", 10, "bold"),
            bg="#4E944F",
            fg="white",
            relief="flat",
            command=self.next_day
        )
        self.next_btn.grid(row=0, column=4, padx=(5, 0))

        self.update_days()

        self.day_box.bind("<<ComboboxSelected>>", self.selection_changed)
        self.month_box.bind("<<ComboboxSelected>>", self.month_changed)
        self.year_box.bind("<<ComboboxSelected>>", self.year_changed)

    # ==================================================

    def update_days(self):

        month = list(calendar.month_name).index(
            self.month_var.get()
        )

        year = self.year_var.get()

        last_day = calendar.monthrange(year, month)[1]

        self.day_box["values"] = list(range(1, last_day + 1))

        if self.day_var.get() > last_day:
            self.day_var.set(last_day)

    # ==================================================

    def month_changed(self, event=None):

        self.update_days()
        self.selection_changed()

    # ==================================================

    def year_changed(self, event=None):

        self.update_days()
        self.selection_changed()

    # ==================================================

    def selection_changed(self, event=None):

        if self.callback:
            self.callback(self.get_date())

    # ==================================================

    def get_date(self):

        month = list(calendar.month_name).index(
            self.month_var.get()
        )

        return date(
            self.year_var.get(),
            month,
            self.day_var.get()
        )

    # ==================================================

    def get_date_string(self):

        return self.get_date().strftime("%Y-%m-%d")

    # ==================================================

    def set_date(self, dt):

        if isinstance(dt, str):
            dt = datetime.strptime(dt, "%Y-%m-%d").date()

        self.year_var.set(dt.year)

        self.month_var.set(
            calendar.month_name[dt.month]
        )

        self.update_days()

        self.day_var.set(dt.day)

    # ==================================================

    def previous_day(self):

        dt = self.get_date()

        dt -= timedelta(days=1)

        self.set_date(dt)

        if self.callback:
            self.callback(dt)

    # ==================================================

    def next_day(self):

        dt = self.get_date()

        dt += timedelta(days=1)

        self.set_date(dt)

        if self.callback:
            self.callback(dt)
    #-----------------------------------------------------
    def set_today(self):

        self.set_date(date.today())