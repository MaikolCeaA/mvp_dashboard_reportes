import customtkinter as ctk
from PIL import Image
import tkinter.messagebox as messagebox
from dashboard_page import DashboardApp
from cred import usuarios

# Configuración visual
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Monitoreo Reportes Regulatorios")
        try:
            self.iconbitmap("images/images.ico")
        except Exception as e:
            print(f"Error al cargar el icono: {e}")
            
        # Obtener resolución de pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Tamaño ventana: 50% ancho, 35% alto
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.35)
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        self.crear_panel_izquierdo(window_width, window_height)
        self.crear_panel_derecho()

    def crear_panel_izquierdo(self, width, height):
          # Frame izquierdo
        left_frame = ctk.CTkFrame(self) 
        left_frame.grid(row=0, column=0)
        try:
            img_path = "images/BANNER_QIK.png"  # Cambia esto a tu imagen real
            image = ctk.CTkImage(light_image=Image.open(img_path), size=(int(width * 0.50), int(height)), )
            img_label = ctk.CTkLabel(left_frame, image=image, text="")
            img_label.pack(expand=True, fill="both")  # Ajusta el relleno vertical según sea necesario
        except Exception as e:
            fallback = ctk.CTkLabel(left_frame, text="(Imagen no encontrada)", font=("Arial", 16))
            fallback.pack(expand=True)    

    def crear_panel_derecho(self):
        right_frame = ctk.CTkFrame(self, corner_radius=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        user_label = ctk.CTkLabel(right_frame, text="Username:")
        user_label.pack(pady=(40, 5))
        self.username_entry = ctk.CTkEntry(right_frame, width=250)
        self.username_entry.pack(pady=(0, 15))

        pass_label = ctk.CTkLabel(right_frame, text="Password:")
        pass_label.pack(pady=(10, 5))
        self.password_entry = ctk.CTkEntry(right_frame, show="*", width=250)
        self.password_entry.pack(pady=(0, 25))

        login_button = ctk.CTkButton(right_frame, text="Login", command=self.login)
        login_button.pack(pady=10)

        forgot_label = ctk.CTkLabel(right_frame, text="Forgot Password", text_color="blue", cursor="hand2")
        forgot_label.pack(pady=5)
        create_label = ctk.CTkLabel(right_frame, text="Create an Account", text_color="blue", cursor="hand2")
        create_label.pack()

    def login(self):
        user = self.username_entry.get()
        password = self.password_entry.get()
        if user in usuarios and usuarios[user] == password:
            self.destroy()
            dashboard = DashboardApp()
            dashboard.mainloop() 
        else:
             messagebox.showerror("Error", "Usuario o contraseña incorrectos")

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
