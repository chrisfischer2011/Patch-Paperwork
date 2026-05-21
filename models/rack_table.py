import sqlite3
import pandas as pd
import os

class RackTable:
    def __init__(self, db_path="project_data.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()
        self.df = self.load_to_pandas()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS racks (
                    id INTEGER PRIMARY KEY,
                    "Rack Location" TEXT,
                    "Rack #" TEXT,
                    "Rack Type" TEXT,
                    "Switch Cor" TEXT,
                    "Off Ramp" TEXT,
                    "AES Input" TEXT,
                    "Analog Inp" TEXT,
                    "Distro 1" TEXT,
                    "Distro 2" TEXT,
                    "Maps 1" TEXT,
                    "Maps 2" TEXT,
                    "Maps 3" TEXT,
                    "Maps 4" TEXT,
                    "Maps 5" TEXT,
                    "Maps 6" TEXT,
                    "Signal In" TEXT,
                    "Signal Thrc" TEXT,
                    "Signal Out" TEXT,
                    "Signal Out 2" TEXT
                )
            ''')

    def add_rack(self, rack_type: str, rack_number: str):
        with self.conn:
            self.conn.execute('''
                INSERT INTO racks ("Rack #", "Rack Type")
                VALUES (?, ?)
            ''', (rack_number, rack_type))
        self.df = self.load_to_pandas()

    def reset(self):
        """Clear all racks for a New Project"""
        with self.conn:
            self.conn.execute("DELETE FROM racks")
        self.df = self.load_to_pandas()

    def load_to_pandas(self):
        return pd.read_sql_query("SELECT * FROM racks", self.conn)

    def get_all_rows(self):
        return self.df.values.tolist()

    def close(self):
        self.conn.close()