# modules/input_handler.py
import json
from pathlib import Path
from tkinter import filedialog, messagebox

def save_current_project(tab_instance):
    """Save current grid data to JSON"""
    proj_name = tab_instance.project_name.get().strip()
    if not proj_name:
        proj_name = "Untitled_Project"

    default_name = f"{proj_name.replace(' ', '_')}.json"
    
    file_path = filedialog.asksaveasfilename(
        initialdir=Path.home() / "Documents",
        initialfile=default_name,
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    
    if not file_path:
        return None

    try:
        # Get latest data directly from the grid (most important change)
        all_rows = []
        for row_entries in tab_instance.entries:
            values = [entry.get().strip() for entry in row_entries]
            if values[1]:  # Require Rack # 
                all_rows.append(values)

        data = {
            "project_name": proj_name,
            "racks": all_rows,
            "headers": tab_instance.headers
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        messagebox.showinfo("Saved", f"Project '{proj_name}' saved successfully!")
        return file_path
    except Exception as e:
        messagebox.showerror("Save Error", str(e))
        return None


def load_current_project(tab_instance):
    """Load from JSON and populate grid"""
    file_path = filedialog.askopenfilename(
        initialdir=Path.home() / "Documents",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if not file_path:
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Clear current data
        tab_instance.rack_table.reset()
        
        # Load racks from JSON
        for row in data.get("racks", []):
            if len(row) > 1 and row[1]:   # Check Rack # exists
                tab_instance.rack_table.add_full_row(row)
        
        # Update project name
        tab_instance.project_name.set(data.get("project_name", "Loaded Project"))
        
        # Refresh grid
        tab_instance.load_data_into_grid()
        
        # messagebox.showinfo("Loaded", ...)   # You can remove this if you want
        return True
    except Exception as e:
        messagebox.showerror("Load Error", f"Failed to load:\n{str(e)}")
        return None