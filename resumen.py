import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from PIL import Image
from datetime import datetime, timedelta
from functools import partial

# Reportes simulados

# Determinar el color según el estado de la tarea
status_colors = {
    "Enviado": "#00BFB3",
    "Pendiente": "#E6007E",
    "Aceptado": "#003865",
}
font_SUL = "Segoe UI Light"
font_SU = "Segoe UI"
class ResumenPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Resumen - Monitoreo de Reportes")
        try:
            self.iconbitmap("images/images.ico")
        except Exception as e:
            print(f"Error al cargar el icono: {e}")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        self.configure_layout()
        self.crear_navbar()
        self.crear_stats()
        self.crear_detalles()

    def configure_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=18)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def crear_navbar(self):
        navbar = ctk.CTkFrame(self, fg_color="#003865")

        navbar.grid(row=0, column=0, sticky="nsew")

        try:
            img_path = "images\BANNER_QIK.png"  # Cambia esto a tu imagen real
            image = ctk.CTkImage(light_image=Image.open(img_path), size=(100, 100))
            img_label = ctk.CTkLabel(navbar, image=image, text="")
            img_label.pack(expand=True, fill="both")  # Ajusta el relleno vertical según sea necesario
        except Exception as e:
            fallback = ctk.CTkLabel(navbar, text="(Imagen no encontrada)", font=("Arial", 16))
            fallback.pack(expand=True)


        btn_calendario = ctk.CTkButton(navbar, text="📅 Calendario", anchor="w", fg_color="#0072CE", hover_color="#47ACF1", text_color="white", command=self.abrir_calendario)
        btn_calendario.pack(fill="x", padx=20, pady=10)

        btn_resumen = ctk.CTkButton(navbar, text="📊 Resumen", anchor="w", fg_color="#0072CE", hover_color="#47ACF1", text_color="white", command=self.abrir_resumen)
        btn_resumen.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(navbar, text="", fg_color="#F1E7DB").pack(expand=True)

        btn_logout = ctk.CTkButton(navbar, text="Cerrar Sesión", fg_color="#E6007E", hover_color="#B80064", text_color="white", command=self.logout)
        btn_logout.pack(fill="x", padx=20, pady=20)
    def crear_stats(self):
        self.center_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#FFFFFF")
        self.center_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)

        titulo = ctk.CTkLabel(self.center_frame, text="Estadísticas de Reportes", font=(font_SUL, 18, "normal"), text_color="#003865")
        titulo.pack(pady=10)

       

    def crear_detalles(self):
        self.right_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#FFFFFF")
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=20)

        self.detalle_titulo = ctk.CTkLabel(self.right_frame, text="Detalles de la Semana", font=(font_SUL, 18, "normal"), text_color="#003865")
        self.detalle_titulo.pack(pady=15)

        self.cards_frame = ctk.CTkScrollableFrame(self.right_frame, width=300, height=500, fg_color="#FFFFFF")
        self.cards_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        
    def abrir_calendario(self):
        self.destroy()
        dashboard = __import__("dashboard_page").DashboardApp
        dashboard().mainloop()
    
    def abrir_resumen(self):
        pass
    
    
    def logout(self):
        confirm = messagebox.askyesno("Cerrar Sesión", "¿Deseas cerrar la sesión?")
        if confirm:
            self.destroy()
            main_app = __import__("login_page").LoginApp
            main_app().mainloop()
        
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = ResumenPage()
    app.mainloop()