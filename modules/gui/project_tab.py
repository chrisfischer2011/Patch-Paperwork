# modules/gui/new_project_tab.py
import customtkinter as ctk
from tkinter import messagebox
from models.project import AmpProject
from modules.amp_rack_handler import create_amp_rack
from modules.input_handler import save_project, load_project   # <-- make sure this line exists

class NewProjectTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.project = AmpProject(project_name="New Amp Project")  # Start with empty project
        
        # Project Name
        ctk.CTkLabel(self, text="Project Name:").pack(pady=5)
        self.name_entry = ctk.CTkEntry(self, width=300)
        self.name_entry.insert(0, self.project.project_name)
        self.name_entry.pack(pady=5)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="+ Add 112 Amp Rack", 
                     command=self.add_rack).pack(side="left", padx=5)
        



    def add_rack(self):
        # Placeholder for now - we'll expand this next
        rack = create_amp_rack()
        if rack:
            self.project.racks.append(rack)
            messagebox.showinfo("Rack Added", f"Added rack: {rack.rack_id}")
