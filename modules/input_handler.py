# modules/input_handler.py
import json
from pathlib import Path
from tkinter import filedialog, messagebox
from models.project import AmpProject

def save_project(project: AmpProject):
    if not project.project_name:
        messagebox.showwarning("Save", "Please enter a project name first!")
        return None

    default_name = f"{project.project_name.replace(' ', '_')}.json"
    
    file_path = filedialog.asksaveasfilename(
        initialdir=Path.home() / "Documents",
        initialfile=default_name,
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    
    if not file_path:
        return None

    try:
        data = project.model_dump(mode='json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        messagebox.showinfo("Saved", f"Project saved to:\n{file_path}")
        return file_path
    except Exception as e:
        messagebox.showerror("Save Error", str(e))
        return None

def load_project() -> AmpProject | None:
    """Load project from user-chosen JSON file"""
    file_path = filedialog.askopenfilename(
        initialdir=Path.home() / "Documents",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    
    if not file_path:
        return None   # User cancelled → return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        project = AmpProject.model_validate(data)
        messagebox.showinfo("Loaded", f"Loaded project: {project.project_name}")
        return project
    except Exception as e:
        messagebox.showerror("Load Error", f"Failed to load file:\n{str(e)}")
        return None
    
def save_current_project(tab_instance):
    """Reusable Save - can be called from main_window sidebar or tab"""
    from tkinter import messagebox
    
    if not hasattr(tab_instance, 'project') or not hasattr(tab_instance, 'name_entry'):
        messagebox.showerror("Error", "Invalid tab passed to save.")
        return None
    
    # Update name from GUI field
    tab_instance.project.project_name = tab_instance.name_entry.get().strip()
    
    if not tab_instance.project.project_name:
        messagebox.showwarning("Save", "Project name cannot be empty!")
        return None
    
    file_path = save_project(tab_instance.project)
    if file_path:
        messagebox.showinfo("Success", f"Project saved successfully!")
    return file_path


def load_current_project(tab_instance):
    """Reusable Load - mirrors save pattern"""
    from tkinter import messagebox
    
    if not hasattr(tab_instance, 'project') or not hasattr(tab_instance, 'name_entry'):
        messagebox.showerror("Error", "Invalid tab passed to load.")
        return None
    
    loaded = load_project()   # This opens the file dialog
    if loaded is not None:
        tab_instance.project = loaded
        tab_instance.name_entry.delete(0, "end")
        tab_instance.name_entry.insert(0, loaded.project_name)
        messagebox.showinfo("Success", f"Project '{loaded.project_name}' loaded successfully!")
        return loaded
    return None