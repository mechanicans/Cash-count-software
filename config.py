APP_TITLE = "Ramakrishna Math & Mission Ashram Midnapore"

WINDOW_WIDTH = 1350
WINDOW_HEIGHT = 1000

#DB_FILE = "data/cash_ledger.db"
import os

APP_DATA_DIR = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
    "CashLedger"
)

os.makedirs(
    APP_DATA_DIR,
    exist_ok=True
)

DB_FILE = os.path.join(
    APP_DATA_DIR,
    "cash_ledger.db"
)

DENOMINATIONS = [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]

# Young banana leaf theme

BG_COLOR = "#E4F5D4"
HEADER_COLOR = "#4E944F"

CURRENT_PANEL_COLOR = "#F8FFF2"
REFERENCE_PANEL_COLOR = "#EDF6E7"

SAVE_BUTTON_COLOR = "#2E7D32"
EXPORT_BUTTON_COLOR = "#00897B"
CALENDAR_BUTTON_COLOR = "#1976D2"

TEXT_COLOR = "#1F2937"

FONT_NORMAL = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")
