import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta

# Reportes simulados
reportes = {
    "2025-06-23-Reunión Clientes": {"hora": "01:00", "fecha": "2025-06-23", "titulo": "Reunión Clientes", "estado": "Enviado"}, 
    "2025-06-24-Reporte Diario SB": {"hora": "01:00", "fecha": "2025-06-23", "titulo": "Reporte Diario SB", "estado": "Aceptado"}, 
    "2025-06-25-Control Legal": {"hora": "01:00", "fecha": "2025-06-23", "titulo": "Control Legal", "estado": "Pendiente"}, 
    "2025-06-26-Reunión Clientes": {"hora": "01:00","fecha": "2025-06-24",  "titulo": "Reunión Clientes", "estado": "Aceptado"}, 
    "2025-06-27-Reunión Clientes": {"hora": "03:00","fecha": "2025-06-27",  "titulo": "Reunión Clientes", "estado": "Aceptado"}, 
    "2025-06-01-Reporte Semanal": {"hora": "01:00", "fecha": "2025-06-24", "titulo": "Reporte Semanal", "estado": "Pendiente"},
    "2025-06-28-Reporte Semanal": {"hora": "01:00", "fecha": "2025-06-25", "titulo": "Reporte Semanal", "estado": "Pendiente"},
    "2025-06-04-Reporte Semanal": {"hora": "01:00", "fecha": "2025-06-24", "titulo": "Reporte Semanal", "estado": "Pendiente"},
    "2025-06-08-Reporte Semanal": {"hora": "01:00", "fecha": "2025-06-24", "titulo": "Reporte Semanal", "estado": "Pendiente"} ,
    "2025-06-15-Reporte Semanal": {"hora": "01:00", "fecha": "2025-06-24", "titulo": "Reporte Semanal", "estado": "Pendiente"} ,
    "2025-06-21-Reporte Semanal": {"hora": "01:00", "fecha": "2025-06-26", "titulo": "Reporte Semanal", "estado": "Pendiente"} ,
    "2025-06-20-Reporte Semanal": {"hora": "01:00", "fecha": "2025-06-24", "titulo": "Reporte Semanal", "estado": "Pendiente"} , 
}
# Determinar el color según el estado de la tarea
status_colors = {
    "Enviado": "#00BFB3",
    "Pendiente": "#E6007E",
    "Aceptado": "#003865",
}
font_SUL = "Segoe UI Light"
font_SU = "Segoe UI"
class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard - Monitoreo de Reportes")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        self.reportes = reportes
        self.agenda_frame = None

        self.configure_layout()
        self.crear_navbar()
        self.crear_calendario()
        self.crear_detalles()

    def configure_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=18)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def crear_navbar(self):
        navbar = ctk.CTkFrame(self, corner_radius=0, fg_color="#003865")

        navbar.grid(row=0, column=0, sticky="nsew")

        titulo = ctk.CTkLabel(navbar, text="MyTask", font=(font_SU, 20, "bold"), text_color="#ffffff")
        titulo.pack(pady=(20, 30))

        btn_calendario = ctk.CTkButton(navbar, text="📅 Calendario", anchor="w", fg_color="#0072CE", hover_color="#47ACF1", text_color="white")
        btn_calendario.pack(fill="x", padx=20, pady=10)

        btn_resumen = ctk.CTkButton(navbar, text="📊 Resumen", anchor="w", fg_color="#0072CE", hover_color="#47ACF1", text_color="white")
        btn_resumen.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(navbar, text="", fg_color="#F1E7DB").pack(expand=True)

        btn_logout = ctk.CTkButton(navbar, text="Cerrar Sesión", fg_color="#E6007E", hover_color="#B80064", text_color="white", command=self.logout)
        btn_logout.pack(fill="x", padx=20, pady=20)

    def crear_calendario(self):
        self.center_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#FFFFFF")
        self.center_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)

        titulo = ctk.CTkLabel(self.center_frame, text="Calendario de Reportes", font=(font_SUL, 18, "normal"), text_color="#003865")
        titulo.pack(pady=10)

        self.cal = Calendar(self.center_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.cal.pack(pady=10)

        btn_ver = ctk.CTkButton(self.center_frame, text="Ver Semana", command=self.mostrar_semana, fg_color="#0072CE", hover_color="#47ACF1", text_color="white")
        btn_ver.pack(pady=5)

    def crear_detalles(self):
        self.right_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#FFFFFF")
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=20)

        self.detalle_titulo = ctk.CTkLabel(self.right_frame, text="Detalles de la Semana", font=(font_SUL, 18, "normal"), text_color="#003865")
        self.detalle_titulo.pack(pady=15)

        self.cards_frame = ctk.CTkScrollableFrame(self.right_frame, width=300, height=500, fg_color="#FFFFFF")
        self.cards_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def mostrar_semana(self):
        fecha_str = self.cal.get_date()
        base_date = datetime.strptime(fecha_str, "%Y-%m-%d")
        monday = base_date - timedelta(days=base_date.weekday())

        dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        tareas = {d: {} for d in dias}

        for i in range(7):
            fecha = monday + timedelta(days=i)
            clave = fecha.strftime("%Y-%m-%d")
            nombre_dia = dias[i]

            for reporte_id, rep in self.reportes.items():
                print(f'{rep["fecha"]} == {clave}')
                if rep["fecha"] == clave:
                    
                    if rep["hora"] not in tareas[nombre_dia]:
                        tareas[nombre_dia][rep["hora"]] = []
                    tareas[nombre_dia][rep["hora"]].append({
                        "id": reporte_id,  # útil para acciones futuras
                        "titulo": rep["titulo"],
                        "estado": rep["estado"]
                    })

        if self.agenda_frame:
            self.agenda_frame.destroy()

        self.agenda_frame = AgendaSemanal(self.center_frame, tareas)
        self.agenda_frame.pack(fill="both", expand=True)

        self.actualizar_detalles_semana(monday)

    def actualizar_detalles_semana(self, monday):
        self.detalle_titulo.configure(
            text=f"Reportes del {monday.strftime('%d/%m')} al {(monday + timedelta(days=6)).strftime('%d/%m')}"
        )

        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        for i in range(7):
            fecha = monday + timedelta(days=i)
            clave = fecha.strftime("%Y-%m-%d")

            for rep_id, rep in self.reportes.items():
                if rep["fecha"] == clave:
                    sombra = ctk.CTkFrame(
                        self.cards_frame,
                        border_width=0,
                        corner_radius=12,
                        fg_color="#D3D3D3"
                    )
                    sombra.pack(pady=(14, 0), padx=(14, 0), fill="x")
                    sombra.lower()

                    card_color = "#F5F7FA"
                    card = ctk.CTkFrame(
                        self.cards_frame,
                        border_width=1,
                        corner_radius=10,
                        fg_color=card_color
                    )
                    card.place(in_=sombra, relx=0, rely=0, x=-8, y=-8, relwidth=1, relheight=1)

                    lbl_fecha = ctk.CTkLabel(card, text=fecha.strftime("%A %d/%m"), font=(font_SUL, 12, "italic"), text_color="#003865")
                    lbl_fecha.pack(anchor="w", padx=10, pady=(5, 0))

                    lbl_titulo = ctk.CTkLabel(card, text=rep["titulo"], font=(font_SU, 14, "bold"), text_color="#003865")
                    lbl_titulo.pack(anchor="w", padx=10)

                    lbl_hora = ctk.CTkLabel(card, text=rep["hora"], font=(font_SUL, 12), text_color="#003865")
                    lbl_hora.pack(anchor="w", padx=10)

                    estado_color = status_colors.get(rep["estado"], "#817CA5")
                    lbl_estado = ctk.CTkLabel(
                        card,
                        text=f"Estado: {rep['estado']}",
                        font=(font_SUL, 12),
                        text_color=estado_color
                    )
                    lbl_estado.pack(anchor="w", padx=10, pady=(0, 5))

    def logout(self):
        confirm = messagebox.askyesno("Cerrar Sesión", "¿Deseas cerrar la sesión?")
        if confirm:
            self.destroy()


class AgendaSemanal(ctk.CTkFrame):
    def __init__(self, parent, tareas_dict):
        super().__init__(parent)
        self.dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.horas = [f"{h:02d}:00" for h in range(1, 24)]
        self.tareas = tareas_dict

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#F5F7FA", corner_radius=20, border_color="#003865")
        self.scroll.pack(fill="both", expand=True)
        self.center_frame = ctk.CTkFrame(self.scroll, fg_color="#F5F7FA")
        self.center_frame.pack(expand=True, anchor="center", pady=20)
        
        self.crear_grilla()

    def crear_grilla(self):   ##Calendario semanal
        ctk.CTkLabel(self.center_frame, text="", width=5).grid(row=0, column=0) 
        for col, dia in enumerate(self.dias, start=1):
            ctk.CTkLabel(self.center_frame, text=dia, font=(font_SU, 12), width=15, text_color="#003865").grid(row=0, column=col, padx=2, pady=2)

        for row, hora in enumerate(self.horas, start=1):
            ctk.CTkLabel(self.center_frame, text=hora, font=(font_SU, 12), width=12, text_color="#003865").grid(row=row, column=0, padx=2, pady=2)
            for col, dia in enumerate(self.dias, start=1):
                celda = ctk.CTkFrame(self.center_frame, width=200, height=100, border_width=1, border_color="#003865", fg_color='transparent')
                celda.grid(row=row, column=col)
                celda.grid_propagate(False)
                celda.pack_propagate(False) 

                tareas_celda = self.tareas.get(dia, {}).get(hora, [])
                
                num_tareas = len(tareas_celda)
                max_tareas_visibles = 2
                tareas_a_mostrar = tareas_celda[:max_tareas_visibles]
                mostrar_mas = num_tareas > max_tareas_visibles

                # Altura fija para tareas visibles
                if num_tareas >= 2:
                    altura_tarea_fija = 33
                else:
                    altura_tarea_fija = 100
                    
                for tarea in tareas_a_mostrar:
                    color = status_colors.get(tarea["estado"], "#817CA5")
                    
                    frame_con_borde = ctk.CTkFrame(
                        master=celda,
                        fg_color="#003865",
                        corner_radius=5,
                        height=altura_tarea_fija,
                    )
                    frame_con_borde.pack(fill="both", padx=2, pady=1)
                    
                    ctk.CTkLabel(
                        master=frame_con_borde,
                        text=tarea["titulo"],
                        text_color="white",
                        fg_color=color,
                        corner_radius=5,
                        height=altura_tarea_fija,
                    ).pack(fill="both", padx=2, pady=1)
                    
                if mostrar_mas:
                    ctk.CTkLabel(
                        master=celda,
                        text=f"+{num_tareas - max_tareas_visibles + 1}",
                        text_color="#003865",
                        font=(font_SUL, 12, "bold"),
                        height=33
                    ).pack( fill="x", padx=2, pady=1)                    


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = DashboardApp()
    app.mainloop()
