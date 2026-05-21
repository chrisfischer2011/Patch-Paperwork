import customtkinter as ctk
from .project_tab import NewProjectTab

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AMP PATCH Generator")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nswe")

        ctk.CTkLabel(sidebar, text="MENU", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=30)

        ctk.CTkButton(sidebar, text="New Project", height=45, command=self.show_new_project).pack(pady=8, padx=20, fill="x")
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

    def show_new_project(self):
        if self.current_tab: self.current_tab.destroy()
        self.current_tab = NewProjectTab(self.main_frame)
        self.current_tab.pack(fill="both", expand=True)

    def show_load(self):
        """Sidebar Load button - reuses the same function"""
        if self.current_tab and isinstance(self.current_tab, NewProjectTab):
            from modules.input_handler import load_current_project
            load_current_project(self.current_tab)
        else:
            from tkinter import messagebox
            messagebox.showwarning("Load", "Please open a project tab first.")

    def show_save(self):
        if self.current_tab and isinstance(self.current_tab, NewProjectTab):
            from modules.input_handler import save_current_project
            save_current_project(self.current_tab)

    def show_generate(self):
        from tkinter import messagebox
        messagebox.showinfo("Generate", "Paperwork generation coming soon")
