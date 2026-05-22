import customtkinter as ctk
from tkinter import messagebox
from models.rack_table import RackTable

class NewProjectTab(ctk.CTkFrame):
    def __init__(self, master, rack_table=None):
        super().__init__(master)
        self.rack_table = rack_table or RackTable()
        self.project_name = ctk.StringVar(value="New Project")
        self.entries = []  # Store all entry widgets for easy access

        # Project Name
        name_frame = ctk.CTkFrame(self, fg_color="transparent")
        name_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(name_frame, text="Project:", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=(0,8))
        self.name_entry = ctk.CTkEntry(name_frame, textvariable=self.project_name, width=400, height=35)
        self.name_entry.pack(side="left")

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="ADD RACK", height=40, width=180,
                     command=self.add_new_row).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="SAVE ALL", height=40, width=180,
                     fg_color="green", command=self.save_all_to_db).pack(side="left", padx=10)

        # Scrollable Grid Container
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=500)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.headers = [
            "Location", "Rack #", "Rack Type", "Switch Config", "Off Ramp",
            "AES Input", "Analog Input", "Distro 1", "Distro 2",
            "Maps 1", "Maps 2", "Maps 3", "Maps 4", "Maps 5", "Maps 6",
            "Signal In", "Signal Thru", "Signal Out", "Signal Out 2"
        ]

        self.build_grid_headers()
        self.load_data_into_grid()

    def build_grid_headers(self):
        for col, header in enumerate(self.headers):
            lbl = ctk.CTkLabel(self.scroll_frame, text=header, font=ctk.CTkFont(size=12, weight="bold"))
            lbl.grid(row=0, column=col, padx=5, pady=5, sticky="w")

    def load_data_into_grid(self):
        """Clear and reload all rows from database"""
        # Clear existing data rows
        for widget in self.scroll_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        self.entries.clear()
        rows = self.rack_table.get_all_rows()

        for row_idx, row_data in enumerate(rows, start=1):
            row_entries = []
            for col_idx, value in enumerate(row_data):
                entry = ctk.CTkEntry(self.scroll_frame, width=120)
                entry.insert(0, str(value) if value is not None else "")
                entry.grid(row=row_idx, column=col_idx, padx=2, pady=2)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def add_new_row(self):
        """Add a new blank row directly in the grid"""
        row_entries = []
        row_idx = len(self.entries) + 1
        
        for col_idx in range(len(self.headers)):
            entry = ctk.CTkEntry(self.scroll_frame, width=120)
            if col_idx == 2:   # Default Rack Type
                entry.insert(0, "112")
            entry.grid(row=row_idx, column=col_idx, padx=2, pady=2)
            row_entries.append(entry)
        
        self.entries.append(row_entries)
        messagebox.showinfo("New Row", "New row added at the bottom. Fill it and click SAVE ALL.")

    def save_all_to_db(self):
        """Save all grid data back to SQLite"""
        try:
            self.rack_table.reset()  # Clear old data
            
            for row_entries in self.entries:
                values = [entry.get().strip() for entry in row_entries]
                if not values[1]:  # Skip if Rack # is empty
                    continue
                
                self.rack_table.add_full_row(values)
            
            messagebox.showinfo("Saved", "All changes saved to database successfully!")
            self.load_data_into_grid()   # Refresh grid
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def show_add_rack_dialog(self):
        # Optional fallback - kept for now
        pass