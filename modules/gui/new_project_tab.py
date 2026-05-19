import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from typing import List

# We'll call modules instead of writing everything here
from models.project import AmpProject
from modules.amp_rack_handler import create_amp_rack
from modules.input_handler import save_project


class NewProjectTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.amp_racks = []          # List of dicts for now
        self.project = None
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = ctk.CTkLabel(self, text="New Amp Rack Project", 
                           font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(20, 30))

        # Project Name
        proj_frame = ctk.CTkFrame(self)
        proj_frame.pack(fill="x", padx=40, pady=10)
        ctk.CTkLabel(proj_frame, text="Project Name:").pack(anchor="w", padx=10, pady=(10,5))
        self.project_name = ctk.CTkEntry(proj_frame, width=500, height=35, 
                                       placeholder_text="e.g. Adamson Arena - July 2026")
        self.project_name.pack(padx=10, pady=5)
        self.project_name.insert(0, f"Adamson Amp Racks - {datetime.now().strftime('%Y-%m-%d')}")

        # Add Amp Rack Button
        add_btn = ctk.CTkButton(self, text="+ Add 112 Amp Rack", height=45, 
                               width=300, font=ctk.CTkFont(size=16), 
                               command=self.open_add_rack_dialog)
        add_btn.pack(pady=30)

        # List of added racks
        self.list_frame = ctk.CTkScrollableFrame(self, height=300)
        self.list_frame.pack(fill="both", expand=True, padx=40, pady=10)

        self.refresh_rack_list()

        # Bottom buttons
        bottom = ctk.CTkFrame(self)
        bottom.pack(fill="x", padx=40, pady=30)
        ctk.CTkButton(bottom, text="Save Project", fg_color="green", height=45,
                     command=self.save_project).pack(side="left", padx=10)
        ctk.CTkButton(bottom, text="Generate Patch Paperwork", height=45,
                     command=self.generate_paperwork).pack(side="right", padx=10)

    def open_add_rack_dialog(self):
        # We'll build a nice dialog next
        from tkinter import messagebox
        messagebox.showinfo("Next Step", "Add Amp Rack Dialog coming in next message")
        # TODO: Call dialog and add to self.amp_racks

    def refresh_rack_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        if not self.amp_racks:
            ctk.CTkLabel(self.list_frame, text="No racks added yet.\nClick the button above to add 112 Amp Racks", 
                        text_color="gray").pack(pady=60)
            return
        # Display added racks here later

    def save_project(self):
        name = self.project_name.get().strip()
        if not name:
            messagebox.showwarning("Error", "Project name is required")
            return
        messagebox.showinfo("Saved", f"Project '{name}' would be saved here.\n(We will connect real save next)")

    def generate_paperwork(self):
        messagebox.showinfo("Ready", "Paperwork generation will start here once we have racks.")