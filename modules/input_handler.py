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