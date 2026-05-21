# modules/input_handler.py
import json
from pathlib import Path
from tkinter import filedialog, messagebox

def save_current_project(tab_instance):
    """Save using the current project_name StringVar"""
    proj_name = tab_instance.project_name.get().strip()
    if not proj_name:
        messagebox.showwarning("Save", "Please enter a Project Name first!")
        return None

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
        data = {
            "project_name": proj_name,
            "racks": tab_instance.rack_table.df.to_dict('records')
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        messagebox.showinfo("Saved", f"Project '{proj_name}' saved successfully!")
        return file_path
    except Exception as e:
        messagebox.showerror("Save Error", str(e))
        return None


def load_current_project(tab_instance):
    """Load project and update table + name"""
    file_path = filedialog.askopenfilename(
        initialdir=Path.home() / "Documents",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if not file_path:
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tab_instance.rack_table.reset()
        for row in data.get("racks", []):
            rtype = row.get("Rack Type", "112")
            rnum = row.get("Rack #", "")
            if rnum:
                tab_instance.rack_table.add_rack(rtype, rnum)
        
        tab_instance.project_name.set(data.get("project_name", "Loaded Project"))
        tab_instance.refresh_table()
        messagebox.showinfo("Loaded", f"Project '{data.get('project_name')}' loaded!")
        return True
    except Exception as e:
        messagebox.showerror("Load Error", f"Failed to load:\n{str(e)}")
        return None