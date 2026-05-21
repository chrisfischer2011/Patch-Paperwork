import sqlite3
import pandas as pd
import os
from datetime import datetime

class RackTable:
    def __init__(self, db_path='project_data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()
        self.df = self.load_to_pandas()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS racks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rack_local TEXT,
                rack_number TEXT,
                rack_type TEXT,
                switch_cor TEXT,
                off_ramp TEXT,
                aes_input TEXT,
                analog_inp TEXT,
                distro_1 TEXT,
                distro_2 TEXT,
                maps_1 TEXT,
                maps_2 TEXT,
                maps_3 TEXT,
                maps_4 TEXT,
                maps_5 TEXT,
                maps_6 TEXT,
                signal_in TEXT,
                signal_thrc TEXT,
                signal_out TEXT,
                signal_out_2 TEXT,
                created_at TEXT
            )
        ''')
        self.conn.commit()
    
    def add_rack(self, rack_type, rack_number, **kwargs):
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        
        data = {
            'rack_local': kwargs.get('rack_local', ''),
            'rack_number': rack_number,
            'rack_type': rack_type,
            'switch_cor': kwargs.get('switch_cor', ''),
            'off_ramp': kwargs.get('off_ramp', ''),
            'aes_input': kwargs.get('aes_input', ''),
            'analog_inp': kwargs.get('analog_inp', ''),
            'distro_1': kwargs.get('distro_1', ''),
            'distro_2': kwargs.get('distro_2', ''),
            'maps_1': kwargs.get('maps_1', ''),
            'maps_2': kwargs.get('maps_2', ''),
            'maps_3': kwargs.get('maps_3', ''),
            'maps_4': kwargs.get('maps_4', ''),
            'maps_5': kwargs.get('maps_5', ''),
            'maps_6': kwargs.get('maps_6', ''),
            'signal_in': kwargs.get('signal_in', ''),
            'signal_thrc': kwargs.get('signal_thrc', ''),
            'signal_out': kwargs.get('signal_out', ''),
            'signal_out_2': kwargs.get('signal_out_2', ''),
            'created_at': now
        }
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = list(data.values())
        
        cursor.execute(f'''
            INSERT INTO racks ({columns}) VALUES ({placeholders})
        ''', values)
        self.conn.commit()
        
        self.df = self.load_to_pandas()
        return data
    
    def load_to_pandas(self):
        return pd.read_sql_query("SELECT * FROM racks", self.conn)
    
    def get_dataframe(self):
        return self.df
    
    def close(self):
        self.conn.close()