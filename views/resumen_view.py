import customtkinter as ctk
from reportesBD import reportes

font_SUL = "Segoe UI Light"

class ResumenView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=18)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.crear_stats()
        self.crear_detalles()

    def crear_stats(self):
        self.center_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#FFFFFF")
        self.center_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=20)
        titulo = ctk.CTkLabel(self.center_frame, text="Estadísticas de Reportes", font=(font_SUL, 18, "normal"), text_color="#003865")
        titulo.pack(pady=10)

    def crear_detalles(self):
        self.right_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#FFFFFF")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)
        self.detalle_titulo = ctk.CTkLabel(self.right_frame, text="Detalles de la Semana", font=(font_SUL, 18, "normal"), text_color="#003865")
        self.detalle_titulo.pack(pady=15)
        self.cards_frame = ctk.CTkScrollableFrame(self.right_frame, width=300, height=500, fg_color="#FFFFFF")
        self.cards_frame.pack(padx=10, pady=10, fill="both", expand=True)
