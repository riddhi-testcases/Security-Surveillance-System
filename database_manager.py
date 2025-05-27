import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='attendance.db'):
        self.conn = sqlite3.connect(db_name)
        self.setup_database()

    def setup_database(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS PERSONNEL (
                    personnel_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT,
                    current_position TEXT,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

    def add_person(self, full_name, position):
        sql = 'INSERT INTO PERSONNEL (full_name, current_position) values(?, ?)'
        with self.conn:
            self.conn.execute(sql, (full_name, position))

    def update_location(self, person_id, new_location):
        query = "UPDATE PERSONNEL SET current_position=?, last_seen=? WHERE personnel_id=?"
        with self.conn:
            self.conn.execute(query, (new_location, datetime.now().timestamp(), person_id))

    def get_person_details(self, person_id):
        query = "SELECT full_name, current_position, last_seen FROM PERSONNEL WHERE personnel_id=?"
        with self.conn:
            return self.conn.execute(query, (person_id,)).fetchone()

    def get_all_personnel(self):
        with self.conn:
            return self.conn.execute("SELECT * FROM PERSONNEL").fetchall()