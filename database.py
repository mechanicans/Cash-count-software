import sqlite3
from config import DB_FILE

def get_connection():
    return sqlite3.connect(DB_FILE)

def create_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ledger (
        entry_date TEXT PRIMARY KEY,
        d2000 INTEGER,
        d500 INTEGER,
        d200 INTEGER,
        d100 INTEGER,
        d50 INTEGER,
        d20 INTEGER,
        d10 INTEGER,
        d5 INTEGER,
        d2 INTEGER,
        d1 INTEGER,
        expense REAL,
        remarks TEXT,
        total_cash REAL,
        net_cash REAL
    )
    """)

    conn.commit()
    conn.close()

def save_record(record):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO ledger
    VALUES (
        ?,?,?,?,?,?,?,?,?,?,
        ?,?,?,?,?
    )
    """,
    (
        record["entry_date"],
        record["d2000"],
        record["d500"],
        record["d200"],
        record["d100"],
        record["d50"],
        record["d20"],
        record["d10"],
        record["d5"],
        record["d2"],
        record["d1"],
        record["expense"],
        record["remarks"],
        record["total_cash"],
        record["net_cash"]
    ))

    conn.commit()
    conn.close()

def load_record(date_string):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM ledger WHERE entry_date=?",
        (date_string,)
    )

    row = cur.fetchone()
    conn.close()

    return row
def load_record_dict(date_string):

    row = load_record(date_string)

    if row is None:
        return None

    return {
        "entry_date": row[0],

         "d2000": row[1],
         "d500": row[2],
         "d200": row[3],
         "d100": row[4],
         "d50": row[5],
         "d20": row[6],
         "d10": row[7],
         "d5": row[8],
         "d2": row[9],
         "d1": row[10],

         "expense": row[11],
         "remarks": row[12],

         "total_cash": row[13],
         "net_cash": row[14]
    }
#--------------------------------------------------------
def load_records_between(start_date, end_date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM ledger
        WHERE entry_date BETWEEN ? AND ?
        ORDER BY entry_date ASC
        """,
        (start_date, end_date)
    )

    rows = cur.fetchall()

    conn.close()

    return rows

def clear_all_records():

    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM ledger"
        )

        conn.commit()

    finally:
        conn.close()