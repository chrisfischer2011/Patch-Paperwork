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
        
        # Project Name Row (horizontal)
        name_frame = ctk.CTkFrame(self, fg_color="transparent")
        name_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(name_frame, text="Project Name:", width=120, anchor="w").pack(side="left", padx=(0, 10))
        
        self.name_entry = ctk.CTkEntry(name_frame, height=35)
        self.name_entry.pack(side="left", fill="x", expand=True)
        self.name_entry.insert(0, self.project.project_name)

        # Buttons frame (below)
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=15)
        
        ctk.CTkButton(btn_frame, text="+ Add 112 Amp Rack", 
                     command=self.add_rack).pack(side="left", padx=5)
        



    def add_rack(self):
        # Placeholder for now - we'll expand this next
        rack = create_amp_rack()
        if rack:
            self.project.racks.append(rack)
            messagebox.showinfo("Rack Added", f"Added rack: {rack.rack_id}")
