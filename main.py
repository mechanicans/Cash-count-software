from database import create_database
from gui import CashLedgerGUI


def main():
    create_database()

    app = CashLedgerGUI()
    app.mainloop()


if __name__ == "__main__":
    main()