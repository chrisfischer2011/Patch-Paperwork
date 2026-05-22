import sqlite3
import pandas as pd

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
                    "Location" TEXT,
                    "Rack #" TEXT,
                    "Rack Type" TEXT,
                    "Switch Config" TEXT,
                    "Off Ramp" TEXT,
                    "AES Input" TEXT,
                    "Analog Input" TEXT,
                    "Distro 1" TEXT,
                    "Distro 2" TEXT,
                    "Maps 1" TEXT,
                    "Maps 2" TEXT,
                    "Maps 3" TEXT,
                    "Maps 4" TEXT,
                    "Maps 5" TEXT,
                    "Maps 6" TEXT,
                    "Signal In" TEXT,
                    "Signal Thru" TEXT,
                    "Signal Out" TEXT,
                    "Signal Out 2" TEXT
                )
            ''')

    def add_rack(self, rack_type: str, rack_number: str):
        """Quick add from dialog"""
        with self.conn:
            self.conn.execute('''
                INSERT INTO racks ("Rack #", "Rack Type")
                VALUES (?, ?)
            ''', (rack_number, rack_type))
        self.df = self.load_to_pandas()

    def add_full_row(self, values: list):
        """Add complete row from grid with NaN cleaning"""
        clean_values = ["" if v == "" or v is None or str(v).lower() == "nan" else v 
                       for v in values]
        
        placeholders = ",".join(["?"] * len(clean_values))
        columns = '", "'.join(self.get_column_names())
        
        with self.conn:
            self.conn.execute(f'INSERT INTO racks ("{columns}") VALUES ({placeholders})', clean_values)
        
        self.df = self.load_to_pandas()

    def update_row(self, row_index: int, values: list):
        """Update an entire row in the database by its position (0-based)"""
        try:
            # Get the actual database row id
            rows_with_id = self.get_all_rows_with_id()
            if row_index >= len(rows_with_id):
                return False
            
            row_id = rows_with_id[row_index][0]  # First column is the id
            
            clean_values = ["" if v == "" or v is None or str(v).lower() == "nan" else v 
                           for v in values]
            
            columns = self.get_column_names()
            
            # Build SET clause
            set_clause = ", ".join([f'"{col}" = ?' for col in columns])
            
            with self.conn:
                self.conn.execute(f'UPDATE racks SET {set_clause} WHERE id = ?', 
                                (*clean_values, row_id))
            
            self.df = self.load_to_pandas()
            return True
        except Exception as e:
            print(f"Error updating row: {e}")
            return False
    
    def reset(self):
        with self.conn:
            self.conn.execute("DELETE FROM racks")
        self.df = self.load_to_pandas()

    def get_all_rows_with_id(self):
        df = pd.read_sql_query("SELECT * FROM racks", self.conn)
        return df.values.tolist()

    def load_to_pandas(self):
        return pd.read_sql_query("SELECT * FROM racks", self.conn)

    def get_all_rows(self):
        """Return clean rows with NO NaN values - This is the most important fix"""
        df = pd.read_sql_query('''
            SELECT "Location", "Rack #", "Rack Type", "Switch Config", "Off Ramp",
                   "AES Input", "Analog Input", "Distro 1", "Distro 2",
                   "Maps 1", "Maps 2", "Maps 3", "Maps 4", "Maps 5", "Maps 6",
                   "Signal In", "Signal Thru", "Signal Out", "Signal Out 2"
            FROM racks
        ''', self.conn)
        
        # Clean NaN values - this should fix the issue
        df = df.fillna("")
        return df.values.tolist()

    def get_column_names(self):
        """Return list of column names (excluding id)"""
        return [
            "Location", "Rack #", "Rack Type", "Switch Config", "Off Ramp",
            "AES Input", "Analog Input", "Distro 1", "Distro 2",
            "Maps 1", "Maps 2", "Maps 3", "Maps 4", "Maps 5", "Maps 6",
            "Signal In", "Signal Thru", "Signal Out", "Signal Out 2"
        ]
    

    def close(self):
        self.conn.close()