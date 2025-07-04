import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
from functools import partial
from reportesBD import reportes

# Determinar el color segun el estado de la tarea
status_colors = {
    "Enviado": "#00BFB3",
    "Pendiente": "#E6007E",
    "Aceptado": "#003865",
}
font_SUL = "Segoe UI Light"
font_SU = "Segoe UI"

class CalendarioView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.reportes = reportes
        self.agenda_frame = None
        self.grid_columnconfigure(0, weight=18)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.crear_calendario()
        self.crear_detalles()

    def crear_calendario(self):
        self.center_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#FFFFFF")
        self.center_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=20)

        titulo = ctk.CTkLabel(self.center_frame, text="Calendario de Reportes", font=(font_SUL, 18, "normal"), text_color="#003865")
        titulo.pack(pady=10)

        self.cal = Calendar(self.center_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.cal.pack(pady=10)

        btn_ver = ctk.CTkButton(self.center_frame, text="Ver Semana", command=self.mostrar_semana, fg_color="#0072CE", hover_color="#47ACF1", text_color="white")
        btn_ver.pack(pady=5)

    def crear_detalles(self):
        self.right_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#FFFFFF")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)

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
        self.dia_a_fecha = {}

        for i in range(7):
            fecha = monday + timedelta(days=i)
            clave = fecha.strftime("%Y-%m-%d")
            nombre_dia = dias[i]
            self.dia_a_fecha[nombre_dia] = clave
            for reporte_id, rep in self.reportes.items():
                if rep["fecha"] == clave:
                    if rep["hora"] not in tareas[nombre_dia]:
                        tareas[nombre_dia][rep["hora"]] = []
                    tareas[nombre_dia][rep["hora"]].append({
                        "id": reporte_id,
                        "titulo": rep["titulo"],
                        "estado": rep["estado"],
                    })

        if self.agenda_frame:
            self.agenda_frame.destroy()

        self.agenda_frame = AgendaSemanal(self.center_frame, tareas, lambda f, h: self.actualizar_detalles_dia(f, h), self.dia_a_fecha)
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
                    sombra = ctk.CTkFrame(self.cards_frame, border_width=0, corner_radius=12, fg_color="#D3D3D3")
                    sombra.pack(pady=(14, 0), padx=(14, 0), fill="x")
                    sombra.lower()
                    card_color = "#F5F7FA"
                    card = ctk.CTkFrame(self.cards_frame, border_width=1, corner_radius=10, fg_color=card_color)
                    card.place(in_=sombra, relx=0, rely=0, x=-8, y=-8, relwidth=1, relheight=1)
                    lbl_fecha = ctk.CTkLabel(card, text=fecha.strftime("%A %d/%m"), font=(font_SUL, 12, "italic"), text_color="#003865")
                    lbl_fecha.pack(anchor="w", padx=10, pady=(5, 0))
                    lbl_titulo = ctk.CTkLabel(card, text=rep["titulo"], font=(font_SU, 14, "bold"), text_color="#003865")
                    lbl_titulo.pack(anchor="w", padx=10)
                    lbl_hora = ctk.CTkLabel(card, text=rep["hora"], font=(font_SUL, 12), text_color="#003865")
                    lbl_hora.pack(anchor="w", padx=10)
                    estado_color = status_colors.get(rep["estado"], "#817CA5")
                    lbl_estado = ctk.CTkLabel(card, text=f"Estado: {rep['estado']}", font=(font_SUL, 12), text_color=estado_color)
                    lbl_estado.pack(anchor="w", padx=10, pady=(0, 5))

    def actualizar_detalles_dia(self, fecha_str, hora_str):
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        self.detalle_titulo.configure(text=f"Reportes del día {fecha.strftime('%A %d/%m')}")
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        for rep_id, rep in self.reportes.items():
            if rep["fecha"] == fecha_str and rep["hora"] == hora_str:
                self.detalle_titulo.configure(text=f"Reportes del {fecha.strftime('%A %d/%m')} a las {hora_str}")
                sombra = ctk.CTkFrame(self.cards_frame, border_width=0, corner_radius=12, fg_color="#D3D3D3")
                sombra.pack(pady=(14, 0), padx=(14, 0), fill="x")
                sombra.lower()
                card_color = "#F5F7FA"
                card = ctk.CTkFrame(self.cards_frame, border_width=1, corner_radius=10, fg_color=card_color)
                card.place(in_=sombra, relx=0, rely=0, x=-8, y=-8, relwidth=1, relheight=1)
                lbl_fecha = ctk.CTkLabel(card, text=fecha.strftime("%A %d/%m"), font=(font_SUL, 12, "italic"), text_color="#003865")
                lbl_fecha.pack(anchor="w", padx=10, pady=(5, 0))
                lbl_titulo = ctk.CTkLabel(card, text=rep["titulo"], font=(font_SU, 14, "bold"), text_color="#003865")
                lbl_titulo.pack(anchor="w", padx=10)
                lbl_hora = ctk.CTkLabel(card, text=rep["hora"], font=(font_SUL, 12), text_color="#003865")
                lbl_hora.pack(anchor="w", padx=10)
                estado_color = status_colors.get(rep["estado"], "#817CA5")
                lbl_estado = ctk.CTkLabel(card, text=f"Estado: {rep['estado']}", font=(font_SUL, 12), text_color=estado_color)
                lbl_estado.pack(anchor="w", padx=10, pady=(0, 5))

class AgendaSemanal(ctk.CTkFrame):
    def __init__(self, parent, tareas_dict, callback_click, dia_a_fecha_dict):
        super().__init__(parent)
        self.dia_a_fecha = dia_a_fecha_dict
        self.dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.horas = [f"{h:02d}:00" for h in range(1, 24)]
        self.tareas = tareas_dict
        self.callback_click = callback_click
        self.celda_activa = None

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#F5F7FA", corner_radius=20, border_color="#003865")
        self.scroll.pack(fill="both", expand=True)
        self.center_frame = ctk.CTkFrame(self.scroll, fg_color="#F5F7FA")
        self.center_frame.pack(expand=True, anchor="center", pady=20)
        self.crear_grilla()

    def crear_grilla(self):
        ctk.CTkLabel(self.center_frame, text="", width=5).grid(row=0, column=0)
        for col, dia in enumerate(self.dias, start=1):
            ctk.CTkLabel(self.center_frame, text=dia, font=(font_SU, 12), width=15, text_color="#003865").grid(row=0, column=col, padx=2, pady=2)
        def crear_bind(widget, dia_local, hora_local):
            widget.bind("<Button-1>", partial(self.on_celda_click, dia=dia_local, hora=hora_local))
        for row, hora in enumerate(self.horas, start=1):
            ctk.CTkLabel(self.center_frame, text=hora, font=(font_SU, 12), width=12, text_color="#003865").grid(row=row, column=0, padx=2, pady=2)
            for col, dia in enumerate(self.dias, start=1):
                celda = ctk.CTkFrame(self.center_frame, width=200, height=100, border_width=1, border_color="#003865", fg_color='transparent')
                celda.grid(row=row, column=col)
                celda.grid_propagate(False)
                celda.pack_propagate(False)
                crear_bind(celda, dia, hora)
                tareas_celda = self.tareas.get(dia, {}).get(hora, [])
                num_tareas = len(tareas_celda)
                max_tareas_visibles = 2
                tareas_a_mostrar = tareas_celda[:max_tareas_visibles]
                mostrar_mas = num_tareas > max_tareas_visibles
                altura_tarea_fija = 33 if num_tareas >= 2 else 100
                for tarea in tareas_a_mostrar:
                    fecha_real = None
                    for rep_id, rep in reportes.items():
                        if rep["titulo"] == tarea["titulo"] and rep["hora"] == hora:
                            fecha_real = rep["fecha"]
                            break
                    tarea["fecha_real"] = fecha_real
                    color = status_colors.get(tarea["estado"], "#817CA5")
                    frame_con_borde = ctk.CTkFrame(master=celda, fg_color="#003865", corner_radius=5, height=altura_tarea_fija)
                    frame_con_borde.pack(fill="both", padx=2, pady=1)
                    label_tarea = ctk.CTkLabel(master=frame_con_borde, text=tarea["titulo"], text_color="white", fg_color=color, corner_radius=5, height=altura_tarea_fija)
                    label_tarea.pack(fill="both", padx=2, pady=1)
                    crear_bind(frame_con_borde, dia, hora)
                    crear_bind(label_tarea, dia, hora)
                if mostrar_mas:
                    ctk.CTkLabel(master=celda, text=f"+{num_tareas - max_tareas_visibles}", text_color="#003865", font=(font_SUL, 12, "bold"), height=33).pack(fill="x", padx=2, pady=1)

    def on_celda_click(self, event, dia, hora):
        widget = event.widget
        while widget and not isinstance(widget, ctk.CTkFrame):
            widget = widget.master
        if widget:
            if self.celda_activa:
                self.celda_activa.configure(fg_color='transparent')
            widget.configure(fg_color="#D6EAF8")
            self.celda_activa = widget
        fecha = self.dia_a_fecha.get(dia)
        if fecha:
            self.callback_click(fecha, hora)
        else:
            messagebox.showinfo("Sin tareas", f"No hay tareas para {dia} a las {hora}")