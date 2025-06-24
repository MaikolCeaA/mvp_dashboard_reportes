import customtkinter as ctk

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard Qik")
        self.geometry("600x400")
        label = ctk.CTkLabel(self, text="¡Bienvenido al Dashboard!", font=("Arial", 24))
        label.pack(pady=50)