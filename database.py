import sqlite3


class Database:
    def __init__(self, path: str = "database.db"):
        self.path = path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _init_db(self) -> None:
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                telegram TEXT NOT NULL
            )
            """
        )
        connection.commit()
        connection.close()

    def add_entry(self, service: str, date: str, time: str, name: str, phone: str, telegram: str) -> int:
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO entries (service, date, time, name, phone, telegram) VALUES (?, ?, ?, ?, ?, ?)",
            (service, date, time, name, phone, telegram),
        )
        connection.commit()
        entry_id = cursor.lastrowid
        connection.close()
        return entry_id

    def get_booked_slots(self, service: str, date: str) -> list[str]:
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT time FROM entries WHERE service = ? AND date = ?",
            (service, date),
        )
        rows = cursor.fetchall()
        connection.close()
        return [row[0] for row in rows]

    def get_dates_with_entries(self) -> list[str]:
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT date FROM entries ORDER BY date")
        rows = cursor.fetchall()
        connection.close()
        return [row[0] for row in rows]

    def get_entries_by_date(self, date: str) -> list[tuple]:
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT service, time, name, phone, telegram FROM entries WHERE date = ? ORDER BY time",
            (date,),
        )
        rows = cursor.fetchall()
        connection.close()
        return rows
