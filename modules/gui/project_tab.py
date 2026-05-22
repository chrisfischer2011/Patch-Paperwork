import customtkinter as ctk
from tkinter import ttk, messagebox
from models.rack_table import RackTable

class NewProjectTab(ctk.CTkFrame):
    def __init__(self, master, rack_table=None):
        super().__init__(master)
        self.rack_table = rack_table or RackTable()
        self.project_name = ctk.StringVar(value="New Project")

        # Project Name Row
        name_frame = ctk.CTkFrame(self, fg_color="transparent")
        name_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(name_frame, text="Project:", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=(0,8))
        self.name_entry = ctk.CTkEntry(name_frame, textvariable=self.project_name, width=400, height=35)
        self.name_entry.pack(side="left")

        # ADD RACK button
        add_btn = ctk.CTkButton(self, text="ADD RACK", height=50, width=220,
                               font=ctk.CTkFont(size=16, weight="bold"),
                               command=self.show_add_rack_dialog)
        add_btn.pack(pady=15)

        # Scrollable + Editable Treeview
        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(tree_frame, show="headings", height=20)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # === Updated Headers (per your latest changes) ===
        columns = [
            "Location", "Rack #", "Rack Type", "Switch Cor", "Off Ramp",
            "AES Input", "Analog Inp", "Distro 1", "Distro 2",
            "Maps 1", "Maps 2", "Maps 3", "Maps 4", "Maps 5", "Maps 6",
            "Signal In", "Signal Thru", "Signal Out", "Signal Out 2"
        ]

        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="w", minwidth=90)

        # Enable editing
        self.tree.bind("<Double-1>", self.on_double_click)

        self.refresh_table()

    def on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)
        if not item:
            return

        col_index = int(column[1:]) - 1
        col_name = self.tree["columns"][col_index]
        current_values = self.tree.item(item, "values")
        current_value = current_values[col_index]

        x, y, width, height = self.tree.bbox(item, column)
        entry = ttk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, current_value)
        entry.focus()
        entry.select_range(0, "end")

        def save_edit(event=None):
            new_value = entry.get().strip()
            new_values = list(current_values)
            new_values[col_index] = new_value
            self.tree.item(item, values=new_values)
            
            self.update_rack_in_db(item, col_name, new_value)
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def update_rack_in_db(self, tree_item, col_name, new_value):
        try:
            row_index = self.tree.index(tree_item)
            rows_with_id = self.rack_table.get_all_rows_with_id()
            if row_index < len(rows_with_id):
                row_id = rows_with_id[row_index][0]
                
                with self.rack_table.conn:
                    self.rack_table.conn.execute(f'UPDATE racks SET "{col_name}" = ? WHERE id = ?', 
                                               (new_value, row_id))
                
                self.rack_table.df = self.rack_table.load_to_pandas()
        except Exception as e:
            print(f"Database update error: {e}")

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
            messagebox.showinfo("Success", f"Rack Added → {rtype} - {rnum}")
            dialog.destroy()
            self.refresh_table()

        ctk.CTkButton(dialog, text="ADD", command=on_add, height=40, width=120).pack(pady=25)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.rack_table.get_all_rows():
            self.tree.insert("", "end", values=row)