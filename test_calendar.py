import tkinter as tk
from tkcalendar import DateEntry

root = tk.Tk()
root.geometry("400x300")

cal = DateEntry(
    root,
    date_pattern="dd-mm-yyyy"
)
cal.pack(pady=50)

root.mainloop()