import customtkinter as ctk
from tkinter import messagebox
from .project_tab import NewProjectTab
from models.rack_table import RackTable

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AMP PATCH Generator")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.rack_table = RackTable()          # Shared instance
        
        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nswe")

        ctk.CTkLabel(sidebar, text="MENU", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=30)

        ctk.CTkButton(sidebar, text="New Project", height=45, command=self.new_project).pack(pady=8, padx=20, fill="x")
        ctk.CTkButton(sidebar, text="Load Project", height=45, command=self.show_load).pack(pady=8, padx=20, fill="x")
        ctk.CTkButton(sidebar, text="Save Project", height=45, command=self.show_save).pack(pady=8, padx=20, fill="x")
        ctk.CTkButton(sidebar, text="Generate Paperwork", height=45, command=self.show_generate).pack(pady=8, padx=20, fill="x")

    def create_main_content(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.current_tab = None
        self.show_new_project()

    def new_project(self):
        if messagebox.askyesno("New Project", "Clear all racks and start a fresh project?"):
            self.rack_table.reset()
            if self.current_tab:
                self.current_tab.destroy()
            self.current_tab = NewProjectTab(self.main_frame, rack_table=self.rack_table)
            self.current_tab.pack(fill="both", expand=True)
            messagebox.showinfo("New Project", "Fresh project started — table cleared.")

    def show_new_project(self):
        """Called on startup"""
        if self.current_tab:
            self.current_tab.destroy()
        self.current_tab = NewProjectTab(self.main_frame, rack_table=self.rack_table)
        self.current_tab.pack(fill="both", expand=True)

    # ... rest of your load/save/generate methods stay the same
    def show_save(self):
        if hasattr(self, 'current_tab') and isinstance(self.current_tab, NewProjectTab):
            from modules.input_handler import save_current_project
            save_current_project(self.current_tab)
        else:
            messagebox.showwarning("Save", "No project tab open.")

    def show_load(self):
        if hasattr(self, 'current_tab') and isinstance(self.current_tab, NewProjectTab):
            from modules.input_handler import load_current_project
            try:
                load_current_project(self.current_tab)
                self.current_tab.load_data_into_grid()   # ← Changed this line
                messagebox.showinfo("Loaded", "Project loaded successfully.")
            except Exception as e:
                messagebox.showerror("Load Error", str(e))
        else:
            messagebox.showwarning("Load", "No project tab open.")

    def show_generate(self):
        messagebox.showinfo("Generate", "Paperwork generation coming soon")