# modules/gui/project_tab.py
import customtkinter as ctk
from tkinter import messagebox
from models.project import AmpProject, AmpRack
from modules.amp_rack_handler import create_amp_rack

class NewProjectTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.project = AmpProject(project_name="New Amp Project")
        
        # Title
        title = ctk.CTkLabel(self, text="Project Management", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # ONLY "ADD RACK" button
        add_btn = ctk.CTkButton(self, text="ADD RACK", 
                               height=50, width=200,
                               font=ctk.CTkFont(size=16, weight="bold"),
                               command=self.show_add_rack_dialog)
        add_btn.pack(pady=30)
        
        # List of added racks
        list_label = ctk.CTkLabel(self, text="Added Racks:", 
                                 font=ctk.CTkFont(size=14, weight="bold"))
        list_label.pack(anchor="w", padx=40, pady=(20,5))
        
        self.rack_list = ctk.CTkTextbox(self, height=300)
        self.rack_list.pack(fill="both", expand=True, padx=40, pady=5)
        
        self.refresh_rack_list()

    def show_add_rack_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Rack")
        dialog.geometry("420x280")
        dialog.grab_set()  # modal
        
        # Rack Type
        ctk.CTkLabel(dialog, text="Rack Type:", 
                    font=ctk.CTkFont(size=14)).pack(anchor="w", padx=40, pady=(30,5))
        
        type_var = ctk.StringVar(value="112")
        type_combo = ctk.CTkComboBox(dialog, values=["223", "117", "112", "112(AIS)"],
                                    variable=type_var, width=200)
        type_combo.pack(padx=40, pady=5)
        
        # Rack Number
        ctk.CTkLabel(dialog, text="Rack Number:", 
                    font=ctk.CTkFont(size=14)).pack(anchor="w", padx=40, pady=(15,5))
        
        num_entry = ctk.CTkEntry(dialog, width=200, placeholder_text="e.g. R01")
        num_entry.pack(padx=40, pady=5)
        
        def on_add():
            rtype = type_var.get()
            rnum = num_entry.get().strip()
            
            if not rnum:
                messagebox.showwarning("Missing Info", "Please enter a Rack Number")
                return
            
            # Create and add rack
            new_rack = create_amp_rack(
                rack_id=rnum,
                rack_type=rtype
            )
            self.project.racks.append(new_rack)
            
            messagebox.showinfo("Success", f"Rack Added → {rtype} - {rnum}")
            dialog.destroy()
            self.refresh_rack_list()
        
        ctk.CTkButton(dialog, text="ADD", command=on_add, 
                     height=40, width=120).pack(pady=25)

    def refresh_rack_list(self):
        self.rack_list.delete("0.0", "end")
        if not self.project.racks:
            self.rack_list.insert("0.0", "No racks added yet.")
            return
        
        text = ""
        for rack in self.project.racks:
            text += f"• Rack {rack.rack_id}  |  Type: {rack.rack_type}\n"
        self.rack_list.insert("0.0", text)