import customtkinter as ctk
from tkinter import messagebox
from models.rack_table import RackTable

class NewProjectTab(ctk.CTkFrame):
    def __init__(self, master, rack_table=None):
        super().__init__(master)
        self.rack_table = rack_table or RackTable()
        self.project_name = ctk.StringVar(value="New Project")
        self.entries = []  # row -> list of Entry widgets

        # Project Name Row
        name_frame = ctk.CTkFrame(self, fg_color="transparent")
        name_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(name_frame, text="Project:", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=(0,8))
        self.name_entry = ctk.CTkEntry(name_frame, textvariable=self.project_name, width=400, height=35)
        self.name_entry.pack(side="left")

        # Only ADD RACK button now
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="ADD RACK", height=40, width=200,
                     command=self.show_add_rack_dialog).pack()

        # Scrollable Grid
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
        """Clear and reload grid from database"""
        for widget in list(self.scroll_frame.grid_slaves()):
            if int(widget.grid_info().get("row", 0)) > 0:
                widget.destroy()

        self.entries.clear()
        rows = self.rack_table.get_all_rows()

        for row_idx, row_data in enumerate(rows, start=1):
            row_entries = []
            for col_idx, value in enumerate(row_data):
                entry = ctk.CTkEntry(self.scroll_frame, width=130)
                entry.insert(0, str(value) if value is not None else "")
                entry.grid(row=row_idx, column=col_idx, padx=3, pady=2)
                
                # Auto-save when user leaves the cell
                entry.bind("<FocusOut>", lambda e, r=row_idx-1, c=col_idx: self.auto_save_cell(r, c))
                entry.bind("<Return>", lambda e, r=row_idx-1, c=col_idx: self.auto_save_cell(r, c))
                
                row_entries.append(entry)
            self.entries.append(row_entries)

    def auto_save_cell(self, row_idx: int, col_idx: int):
        """Save single cell change to database automatically"""
        if row_idx >= len(self.entries):
            return
        try:
            new_value = self.entries[row_idx][col_idx].get().strip()
            # Rebuild full row and save
            full_row = [entry.get().strip() for entry in self.entries[row_idx]]
            self.rack_table.update_row(row_idx, full_row)
        except:
            pass  # Silent fail - don't annoy user

    def show_add_rack_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Rack")
        dialog.geometry("420x280")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Rack Type:").pack(anchor="w", padx=40, pady=(30,5))
        type_var = ctk.StringVar(value="112")
        type_combo = ctk.CTkComboBox(dialog, values=["223", "117", "112", "112(AIS)"], variable=type_var, width=200)
        type_combo.pack(padx=40, pady=5)

        ctk.CTkLabel(dialog, text="Rack Number:").pack(anchor="w", padx=40, pady=(15,5))
        num_entry = ctk.CTkEntry(dialog, width=200, placeholder_text="e.g. R01")
        num_entry.pack(padx=40, pady=5)

        def on_add():
            rtype = type_var.get()
            rnum = num_entry.get().strip()
            if not rnum:
                messagebox.showwarning("Missing Info", "Please enter a Rack Number")
                return
            self.rack_table.add_rack(rack_type=rtype, rack_number=rnum)
            dialog.destroy()
            self.load_data_into_grid()

        add_button = ctk.CTkButton(dialog, text="ADD", command=on_add, height=40, width=120)
        add_button.pack(pady=25)
        num_entry.bind("<Return>", lambda e: on_add())
        num_entry.focus_set()

    # Removed SAVE ALL button entirely