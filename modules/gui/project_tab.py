import customtkinter as ctk
from tkinter import ttk, messagebox
from models.rack_table import RackTable

class NewProjectTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.rack_table = RackTable()   # SQLite backend
        
        # Title + New Project Button
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=10)
        
        title = ctk.CTkLabel(top_frame, text="Project Management", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(side="left")
        
        # ADD RACK button
        add_btn = ctk.CTkButton(self, text="ADD RACK", 
                               height=50, width=220,
                               font=ctk.CTkFont(size=16, weight="bold"),
                               command=self.show_add_rack_dialog)
        add_btn.pack(pady=15)
        
        # Treeview Table
        self.tree = ttk.Treeview(self, show="headings", height=18)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = [
            "#","Rack Location", "Rack #", "Rack Type", "Switch Cor", "Off Ramp",
            "AES Input", "Analog Inp", "Distro 1", "Distro 2",
            "Maps 1", "Maps 2", "Maps 3", "Maps 4", "Maps 5", "Maps 6",
            "Signal In", "Signal Thrc", "Signal Out", "Signal Out 2"
        ]
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="w")
        
        self.refresh_table()

    def show_add_rack_dialog(self):
        # (same as before - unchanged)
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Rack")
        dialog.geometry("420x280")
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Rack Type:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=40, pady=(30,5))
        type_var = ctk.StringVar(value="112")
        type_combo = ctk.CTkComboBox(dialog, values=["223", "117", "112", "112(AIS)"],
                                    variable=type_var, width=200)
        type_combo.pack(padx=40, pady=5)
        
        ctk.CTkLabel(dialog, text="Rack Number:", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=40, pady=(15,5))
        num_entry = ctk.CTkEntry(dialog, width=200, placeholder_text="e.g. R01")
        num_entry.pack(padx=40, pady=5)
        
        def on_add():
            rtype = type_var.get()
            rnum = num_entry.get().strip()
            if not rnum:
                messagebox.showwarning("Missing Info", "Please enter a Rack Number")
                return
            self.rack_table.add_rack(rack_type=rtype, rack_number=rnum)
            messagebox.showinfo("Success", f"Rack Added → {rtype} - {rnum}")
            dialog.destroy()
            self.refresh_table()
        
        ctk.CTkButton(dialog, text="ADD", command=on_add, height=40, width=120).pack(pady=25)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row in self.rack_table.get_all_rows():
            self.tree.insert("", "end", values=row)