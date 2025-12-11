import os
import sqlite3
import csv
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


try:
    from tkcalendar import DateEntry
    TKCALENDAR_AVAILABLE = True
except Exception:
    TKCALENDAR_AVAILABLE = False

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

DB_PATH = "clinica.db"
IMAGE_DIR = "images"  

os.makedirs(IMAGE_DIR, exist_ok=True)


class ModuloCitasApp:
    def __init__(self, ventana_principal): #JM: Referencia a la ventana principal
        self.ventana_principal = ventana_principal
        self.root = tk.Toplevel(ventana_principal) #JM: combierto root en un vantana hija de ventana_principal
        self.root.title("Sistema de Citas - Módulo Completo")
        self.root.geometry("1000x640")
        self.root.configure(bg="#57717b")
        
        self.db = sqlite3.connect(DB_PATH)
        self.cursor = self.db.cursor()
        self.verificar_tablas() #JM: verificar tabla en vez de crear tablas 
      
        self.var_paciente = tk.StringVar()
        self.var_doctor = tk.StringVar()
        self.var_fecha = tk.StringVar()
        self.var_hora = tk.StringVar()
        
        self.filter_doctor = tk.StringVar()
        self.filter_paciente = tk.StringVar()
        self.filter_fecha = tk.StringVar()
       
        self.preview_img = None
        
        self.crear_frames()
        self.crear_formulario()
        self.crear_treeview()
        self.cargar_comboboxes()
        self.mostrar_citas()

    def verificar_tablas(self):
        """Verifica que las tablas del DBManager existan, si no las crea"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                motivo TEXT,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES doctores(id) ON DELETE CASCADE
            )
        """)
        self.db.commit()

    def crear_frames(self):
        #JM: El título y la barra de navegación, se ubican en la parte superior
        
        # JM: Titulo
        self.frame_title = tk.Frame(self.root, background="#000A91", height=30)
        self.frame_title.pack(fill="x")
        self.frame_title.pack_propagate(False)
        
        self.boton_title = tk.Button(
            self.frame_title,
            text="Citas Medicas",
            font=("Arial", 14, "bold"),
            background="#000A91",
            foreground="#FFFFFF",
            borderwidth=0,
            relief="flat",
            command=self.ir_inicio
        )
        self.boton_title.pack()
        
        # JM: Frame de la barra de navegacion
        self.frame_navbar = tk.Frame(self.root, background="#7C7C7C", height=20)
        self.frame_navbar.pack(fill="x")
        self.frame_navbar.pack_propagate(False)
        self.frame_navbar.columnconfigure(0, weight=1)
        self.frame_navbar.columnconfigure(4, weight=1)
        
        #JM: Botones de la barra de navegación
        self.paciente_btn = tk.Button(
            self.frame_navbar, 
            text="Pacientes",
            height=1,
            width=10,
            font=("Arial", 12),  
            background="#4A90E2", 
            foreground="#F0F0F0",
            borderwidth=2,
            relief="solid", 
            activebackground="#1557A3",
            activeforeground="#F0F0F0",
            cursor="hand2",
            command=self.abrir_pacientes
        )
        self.paciente_btn.grid(row=0, column=1, padx=10)
        
        self.doctores_btn = tk.Button(
            self.frame_navbar, 
            text="Doctores",
            height=1,
            width=10,
            font=("Arial", 12),  
            background="#4A90E2", 
            foreground="#F0F0F0",
            borderwidth=2,
            relief="solid", 
            activebackground="#1557A3",
            activeforeground="#F0F0F0",
            cursor="hand2",
            command=self.abri_doctores
        )
        self.doctores_btn.grid(row=0, column=2, padx=10)
        
        self.citas_btn = tk.Button(
            self.frame_navbar, 
            text="Citas",
            height=1,
            width=10,
            font=("Arial", 12),  
            background="#4A90E2", 
            foreground="#F0F0F0",
            borderwidth=2,
            relief="solid", 
            activebackground="#1557A3",
            activeforeground="#F0F0F0",
            cursor="hand2",
            command=self.abrir_citas
        )
        self.citas_btn.grid(row=0, column=3, padx=10)
    
        
        self.frame_left = tk.Frame(self.root, bg="#50416E", bd=1, relief="solid")
        self.frame_left.place(x=10, y=70, width=360, height=600) 
     
        self.frame_center = tk.Frame(self.root, bg="#cccccc", bd=1, relief="solid")
        self.frame_center.place(x=380, y=70, width=610, height=490)
     
        self.frame_right = tk.Frame(self.root, bg="#f8f8f8", bd=1, relief="solid")
        self.frame_right.place(x=380, y=550, width=610, height=120) 
    
    def crear_formulario(self):
        padx = 12
        pady = 8
        
        title = tk.Label(self.frame_left, text="AGENDAR / EDITAR CITA", font=("Arial", 12, "bold"), bg="#ffffff")
        title.place(x=12, y=10)
        tk.Label(self.frame_left, text="Paciente:", bg="#ffffff").place(x=12, y=50)
        self.cmb_paciente = ttk.Combobox(self.frame_left, textvariable=self.var_paciente, width=30)
        self.cmb_paciente.place(x=12, y=72)
        
        btn_add_p = tk.Button(self.frame_left, text="Agregar Paciente", command=self.abrir_popup_paciente)
        btn_add_p.place(x=12, y=102)
        
        tk.Label(self.frame_left, text="Doctor:", bg="#ffffff").place(x=12, y=140)
        self.cmb_doctor = ttk.Combobox(self.frame_left, textvariable=self.var_doctor, width=30)
        self.cmb_doctor.place(x=12, y=162)
        
        btn_add_d = tk.Button(self.frame_left, text="Agregar Doctor", command=self.abrir_popup_doctor)
        btn_add_d.place(x=12, y=192)
      
        tk.Label(self.frame_left, text="Fecha:", bg="#ffffff").place(x=12, y=230)
        if TKCALENDAR_AVAILABLE:
            self.date_entry = DateEntry(self.frame_left, width=27, date_pattern="yyyy-mm-dd",
                                        textvariable=self.var_fecha)
            self.date_entry.place(x=12, y=252)
        else:
            self.entry_fecha = tk.Entry(self.frame_left, textvariable=self.var_fecha, width=30)
            self.entry_fecha.place(x=12, y=252)
            tk.Label(self.frame_left, text="(Instala tkcalendar para calendario)", fg="gray", bg="#ffffff").place(x=12, y=280)
       
        tk.Label(self.frame_left, text="Hora (HH:MM, 24h):", bg="#ffffff").place(x=12, y=300)
        self.entry_hora = tk.Entry(self.frame_left, textvariable=self.var_hora, width=30)
        self.entry_hora.place(x=12, y=322)
        tk.Label(self.frame_left, text="Ejemplo: 14:30", fg="gray", bg="#ffffff").place(x=12, y=349)
        
        self.btn_guardar = tk.Button(self.frame_left, text="Guardar Cita", bg="#4CAF50", fg="white",
                                     command=self.guardar_cita, width=16)
        self.btn_guardar.place(x=12, y=380)
        
        self.btn_actualizar = tk.Button(self.frame_left, text="Actualizar Cita", bg="#2196F3", fg="white",
                                        command=self.actualizar_cita, width=16, state="disabled")
        self.btn_actualizar.place(x=200, y=380)
        
        
    def crear_treeview(self):
        tk.Label(self.frame_center, text="CITAS AGENDADAS", font=("Segoe UI", 12, "bold"), bg="#cccccc").place(x=12, y=8)
        tk.Label(self.frame_center, text="Filtrar por Doctor:", bg="#cccccc").place(x=12, y=40)
        self.cmb_filter_doctor = ttk.Combobox(self.frame_center, textvariable=self.filter_doctor, width=20)
        self.cmb_filter_doctor.place(x=125, y=40)
        tk.Label(self.frame_center, text="Paciente:", bg="#cccccc").place(x=330, y=40)
        self.cmb_filter_paciente = ttk.Combobox(self.frame_center, textvariable=self.filter_paciente, width=20)
        self.cmb_filter_paciente.place(x=395, y=40)
        tk.Label(self.frame_center, text="Fecha:", bg="#cccccc").place(x=12, y=70)
        if TKCALENDAR_AVAILABLE:
            self.filter_fecha_widget = DateEntry(self.frame_center, textvariable=self.filter_fecha, date_pattern="yyyy-mm-dd", width=18)
            self.filter_fecha_widget.place(x=60, y=70)
        else:
            self.entry_filter_fecha = tk.Entry(self.frame_center, textvariable=self.filter_fecha, width=22)
            self.entry_filter_fecha.place(x=60, y=70)
            tk.Label(self.frame_center, text="(yyyy-mm-dd)", fg="gray", bg="#cccccc").place(x=200, y=70)
        tk.Button(self.frame_center, text="Aplicar filtros", command=self.mostrar_citas).place(x=330, y=70)
        tk.Button(self.frame_center, text="Limpiar filtros", command=self.limpiar_filtros).place(x=430, y=70)
        
        cols = ("ID", "Paciente", "Doctor", "Fecha", "Hora")
        self.tree = ttk.Treeview(self.frame_center, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=110, anchor="center")
            
        TREE_HEIGHT = 330
        self.tree.place(x=12, y=110, width=580, height=330)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        vsb = ttk.Scrollbar(self.frame_center, orient="vertical", command=self.tree.yview)
        vsb.place(x=592, y=110, height=330)
        self.tree.configure(yscrollcommand=vsb.set)
        

        tk.Button(self.frame_center, text="Eliminar cita", bg="#f44336", fg="white", command=self.eliminar_cita).place(x=12, y=450)
        tk.Button(self.frame_center, text="Editar cita", bg="#ff9800", fg="white", command=self.cargar_cita_para_editar).place(x=120, y=450)
        tk.Button(self.frame_center, text="Exportar a CSV", command=self.exportar_csv).place(x=220, y=450)
        tk.Button(self.frame_center, text="Exportar a PDF", command=self.exportar_pdf).place(x=340, y=450)

    # JM: Funciones de navegación
    def ir_inicio(self):
        self.root.destroy()
        self.ventana_principal.deiconify()
       
    def abrir_pacientes(self):
        self.ventana_principal.abrir_pacientes()
        
    def abri_doctores(self):
        self.ventana_principal.abrir_doctores()
        
    def abrir_citas(self):
        self.ventana_principal.abrir_citas()
    


    def crear_controles_extra(self):
        pass 
        
    def cargar_comboboxes(self):
        # Usar nombre + apellido para pacientes
        self.cursor.execute("SELECT nombre, apellido FROM pacientes ORDER BY nombre, apellido")
        pacientes = [f"{r[0]} {r[1]}" for r in self.cursor.fetchall()]
        self.cmb_paciente["values"] = pacientes
        self.cmb_filter_paciente["values"] = [""] + pacientes
        
        # Usar nombre + apellido + especialidad para doctores
        self.cursor.execute("SELECT nombre, apellido, especialidad FROM doctores ORDER BY nombre, apellido")
        doctores = [f"{r[0]} {r[1]} - {r[2]}" for r in self.cursor.fetchall()]
        self.cmb_doctor["values"] = doctores
        self.cmb_filter_doctor["values"] = [""] + doctores

    def abrir_popup_paciente(self):
        # Ya no manejamos pacientes aquí, usar módulo de pacientes
        messagebox.showinfo("Información", "Use el módulo de Pacientes para agregar nuevos pacientes")
        self.ventana_principal.abrir_pacientes()

    def abrir_popup_doctor(self):
        # Ya no manejamos doctores aquí, usar módulo de doctores
        messagebox.showinfo("Información", "Use el módulo de Doctores para agregar nuevos doctores")
        self.ventana_principal.abri_doctores()

    def guardar_cita(self):
        paciente_text = self.var_paciente.get().strip()
        doctor_text = self.var_doctor.get().strip()
        fecha = self.var_fecha.get().strip()
        hora = self.var_hora.get().strip()
        
        if not paciente_text or not doctor_text or not fecha or not hora:
            messagebox.showwarning("Campos incompletos", "Complete todos los campos antes de guardar.")
            return
        
        try:
            datetime.datetime.strptime(fecha, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Formato fecha", "La fecha debe tener formato YYYY-MM-DD.")
            return
        
        try:
            datetime.datetime.strptime(hora, "%H:%M")
        except Exception:
            messagebox.showerror("Formato hora", "La hora debe tener formato HH:MM (24h).")
            return
        
        partes_doctor = doctor_text.split(" - ")
        if len(partes_doctor) < 2:
            messagebox.showerror("Doctor no válido", "Formato: Nombre Apellido - Especialidad")
            return
        
        nombre_apellido = partes_doctor[0].strip()
        especialidad = partes_doctor[1].strip()
        nombres = nombre_apellido.split()
        
        if len(nombres) < 2:
            messagebox.showerror("Doctor no válido", "Formato: Nombre Apellido - Especialidad")
            return
        
        nombre_doc = nombres[0]
        apellido_doc = nombres[1]
        
        self.cursor.execute("SELECT id FROM doctores WHERE nombre = ? AND apellido = ? AND especialidad = ?", 
                          (nombre_doc, apellido_doc, especialidad))
        doctor = self.cursor.fetchone()
        if not doctor:
            messagebox.showerror("Doctor no existe", "Seleccione un doctor válido.")
            return
        id_doctor = doctor[0]
        
        nombres_pac = paciente_text.split()
        if len(nombres_pac) < 2:
            messagebox.showerror("Paciente no válido", "Formato: Nombre Apellido")
            return
        
        nombre_pac = nombres_pac[0]
        apellido_pac = nombres_pac[1]
        
        self.cursor.execute("SELECT id FROM pacientes WHERE nombre = ? AND apellido = ?", 
                          (nombre_pac, apellido_pac))
        paciente = self.cursor.fetchone()
        if not paciente:
            messagebox.showerror("Paciente no existe", "Seleccione un paciente válido.")
            return
        id_paciente = paciente[0]
        
        self.cursor.execute("""
            SELECT COUNT(*) FROM citas WHERE doctor_id=? AND fecha=? AND hora=?
        """, (id_doctor, fecha, hora))
        
        if self.cursor.fetchone()[0] > 0:
            messagebox.showerror("Conflicto de horario", f"El doctor ya tiene una cita el {fecha} a las {hora}.")
            return
        
        self.cursor.execute("""
            INSERT INTO citas (paciente_id, doctor_id, fecha, hora) VALUES (?, ?, ?, ?)
        """, (id_paciente, id_doctor, fecha, hora))
        
        self.db.commit()
        messagebox.showinfo("Cita guardada", "La cita se ha guardado correctamente.")
        self.limpiar_campos_cita()
        self.cargar_comboboxes()
        self.mostrar_citas()

    def mostrar_citas(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        sql = """
            SELECT citas.id, 
                   pacientes.nombre || ' ' || pacientes.apellido as paciente,
                   doctores.nombre || ' ' || doctores.apellido || ' - ' || doctores.especialidad as doctor,
                   citas.fecha, citas.hora
            FROM citas
            JOIN pacientes ON citas.paciente_id = pacientes.id
            JOIN doctores ON citas.doctor_id = doctores.id
        """
        
        filtros = []
        params = []
        
        if self.filter_doctor.get():
            filtros.append("doctores.nombre || ' ' || doctores.apellido || ' - ' || doctores.especialidad = ?")
            params.append(self.filter_doctor.get())
        
        if self.filter_paciente.get():
            filtros.append("pacientes.nombre || ' ' || pacientes.apellido = ?")
            params.append(self.filter_paciente.get())
        
        if self.filter_fecha.get():
            filtros.append("citas.fecha = ?")
            params.append(self.filter_fecha.get())
        
        if filtros:
            sql += " WHERE " + " AND ".join(filtros)
        
        sql += " ORDER BY citas.fecha, citas.hora"
        
        self.cursor.execute(sql, tuple(params))
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def limpiar_filtros(self):
        self.filter_doctor.set("")
        self.filter_paciente.set("")
        self.filter_fecha.set("")
        self.mostrar_citas()

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel)
        valores = item["values"]
        if not valores:
            return

    def eliminar_cita(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Seleccionar cita", "Seleccione una cita para eliminar.")
            return
        item = self.tree.item(sel)
        cita_id = item["values"][0]
        
        if messagebox.askyesno("Confirmar", "¿Eliminar la cita seleccionada?"):
            self.cursor.execute("DELETE FROM citas WHERE id = ?", (cita_id,))
            self.db.commit()
            messagebox.showinfo("Eliminada", "Cita eliminada correctamente.")
            self.mostrar_citas()
            self.limpiar_campos_cita()

    def cargar_cita_para_editar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Seleccionar cita", "Seleccione una cita para editar.")
            return
        
        item = self.tree.item(sel)
        id_cita, paciente, doctor, fecha, hora = item["values"]
        self.editing_id = id_cita
        self.var_paciente.set(paciente)
        self.var_doctor.set(doctor)
        self.var_fecha.set(fecha)
        self.var_hora.set(hora)
        self.btn_guardar.config(state="disabled")
        self.btn_actualizar.config(state="normal")

    def actualizar_cita(self):
        if not hasattr(self, "editing_id") or not self.editing_id:
            messagebox.showwarning("Editar", "No hay cita en edición.")
            return
        
        paciente_text = self.var_paciente.get().strip()
        doctor_text = self.var_doctor.get().strip()
        fecha = self.var_fecha.get().strip()
        hora = self.var_hora.get().strip()
        
        if not paciente_text or not doctor_text or not fecha or not hora:
            messagebox.showwarning("Campos incompletos", "Complete todos los campos antes de actualizar.")
            return
        
        try:
            datetime.datetime.strptime(fecha, "%Y-%m-%d")
            datetime.datetime.strptime(hora, "%H:%M")
        except Exception:
            messagebox.showerror("Formato incorrecto", "Fecha (YYYY-MM-DD) o Hora (HH:MM) no válidos.")
            return
        
        # Obtener ID del doctor
        partes_doctor = doctor_text.split(" - ")
        if len(partes_doctor) < 2:
            messagebox.showerror("Doctor no válido", "Formato: Nombre Apellido - Especialidad")
            return
        
        nombre_apellido = partes_doctor[0].strip()
        especialidad = partes_doctor[1].strip()
        nombres = nombre_apellido.split()
        
        if len(nombres) < 2:
            messagebox.showerror("Doctor no válido", "Formato: Nombre Apellido - Especialidad")
            return
        
        nombre_doc = nombres[0]
        apellido_doc = nombres[1]
        
        self.cursor.execute("SELECT id FROM doctores WHERE nombre = ? AND apellido = ? AND especialidad = ?", 
                          (nombre_doc, apellido_doc, especialidad))
        doctor = self.cursor.fetchone()
        if not doctor:
            messagebox.showerror("Doctor no existe", "Seleccione un doctor válido.")
            return
        id_doctor = doctor[0]
        
        # Obtener ID del paciente
        nombres_pac = paciente_text.split()
        if len(nombres_pac) < 2:
            messagebox.showerror("Paciente no válido", "Formato: Nombre Apellido")
            return
        
        nombre_pac = nombres_pac[0]
        apellido_pac = nombres_pac[1]
        
        self.cursor.execute("SELECT id FROM pacientes WHERE nombre = ? AND apellido = ?", 
                          (nombre_pac, apellido_pac))
        paciente = self.cursor.fetchone()
        if not paciente:
            messagebox.showerror("Paciente no existe", "Seleccione un paciente válido.")
            return
        id_paciente = paciente[0]
        
        # Verificar conflicto de horario (excluyendo la cita actual)
        self.cursor.execute("""
            SELECT COUNT(*) FROM citas WHERE doctor_id=? AND fecha=? AND hora=? AND id != ?
        """, (id_doctor, fecha, hora, self.editing_id))
        
        if self.cursor.fetchone()[0] > 0:
            messagebox.showerror("Conflicto de horario", "Ya existe otra cita para ese doctor en el mismo horario.")
            return
        
        # Actualizar cita
        self.cursor.execute("""
            UPDATE citas SET paciente_id=?, doctor_id=?, fecha=?, hora=? WHERE id=?
        """, (id_paciente, id_doctor, fecha, hora, self.editing_id))
        
        self.db.commit()
        messagebox.showinfo("Actualizado", "Cita actualizada correctamente.")
        self.editing_id = None
        self.btn_guardar.config(state="normal")
        self.btn_actualizar.config(state="disabled")
        self.limpiar_campos_cita()
        self.mostrar_citas()

    def limpiar_campos_cita(self):
        self.var_paciente.set("")
        self.var_doctor.set("")
        self.var_fecha.set("")
        self.var_hora.set("")

    def exportar_csv(self):
        fpath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")],
                                             initialfile=f"citas_{datetime.date.today().isoformat()}.csv")
        if not fpath:
            return
        
        sql = """
            SELECT citas.id, 
                   pacientes.nombre || ' ' || pacientes.apellido as paciente,
                   doctores.nombre || ' ' || doctores.apellido || ' - ' || doctores.especialidad as doctor,
                   citas.fecha, citas.hora
            FROM citas
            JOIN pacientes ON citas.paciente_id = pacientes.id
            JOIN doctores ON citas.doctor_id = doctores.id
        """
        
        filtros = []
        params = []
        
        if self.filter_doctor.get():
            filtros.append("doctores.nombre || ' ' || doctores.apellido || ' - ' || doctores.especialidad = ?")
            params.append(self.filter_doctor.get())
        
        if self.filter_paciente.get():
            filtros.append("pacientes.nombre || ' ' || pacientes.apellido = ?")
            params.append(self.filter_paciente.get())
        
        if self.filter_fecha.get():
            filtros.append("citas.fecha = ?")
            params.append(self.filter_fecha.get())
        
        if filtros:
            sql += " WHERE " + " AND ".join(filtros)
        
        sql += " ORDER BY citas.fecha, citas.hora"
        
        self.cursor.execute(sql, tuple(params))
        rows = self.cursor.fetchall()
        
        with open(fpath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Paciente", "Doctor", "Fecha", "Hora"])
            writer.writerows(rows)
        
        messagebox.showinfo("Exportado", f"Exportado a CSV: {fpath}")

    def exportar_pdf(self):
        if not REPORTLAB_AVAILABLE:
            messagebox.showwarning("Reportlab no instalado", 
                                 "Instala 'reportlab' para exportar PDF (pip install reportlab).\nSe exportará a CSV en su lugar.")
            self.exportar_csv()
            return
        
        fpath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")],
                                             initialfile=f"citas_{datetime.date.today().isoformat()}.pdf")
        if not fpath:
            return
        
        sql = """
            SELECT pacientes.nombre || ' ' || pacientes.apellido as paciente,
                   doctores.nombre || ' ' || doctores.apellido || ' - ' || doctores.especialidad as doctor,
                   citas.fecha, citas.hora
            FROM citas
            JOIN pacientes ON citas.paciente_id = pacientes.id
            JOIN doctores ON citas.doctor_id = doctores.id
        """
        
        filtros = []
        params = []
        
        if self.filter_doctor.get():
            filtros.append("doctores.nombre || ' ' || doctores.apellido || ' - ' || doctores.especialidad = ?")
            params.append(self.filter_doctor.get())
        
        if self.filter_paciente.get():
            filtros.append("pacientes.nombre || ' ' || pacientes.apellido = ?")
            params.append(self.filter_paciente.get())
        
        if self.filter_fecha.get():
            filtros.append("citas.fecha = ?")
            params.append(self.filter_fecha.get())
        
        if filtros:
            sql += " WHERE " + " AND ".join(filtros)
        
        sql += " ORDER BY citas.fecha, citas.hora"
        
        self.cursor.execute(sql, tuple(params))
        rows = self.cursor.fetchall()
        
        c = canvas.Canvas(fpath, pagesize=letter)
        w, h = letter
        y = h - 72
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y, "Listado de Citas")
        y -= 24
        
        c.setFont("Helvetica", 10)
        c.drawString(72, y, f"Generado: {datetime.datetime.now().isoformat(' ', 'seconds')}")
        y -= 24
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(72, y, "Paciente")
        c.drawString(250, y, "Doctor")
        c.drawString(420, y, "Fecha")
        c.drawString(490, y, "Hora")
        y -= 16
        
        c.setFont("Helvetica", 9)
        for row in rows:
            if y < 72:
                c.showPage()
                y = h - 72
            paciente, doctor, fecha, hora = row
            c.drawString(72, y, str(paciente))
            c.drawString(250, y, str(doctor))
            c.drawString(420, y, str(fecha))
            c.drawString(490, y, str(hora))
            y -= 16
        
        c.save()
        messagebox.showinfo("PDF generado", f"Archivo PDF guardado en: {fpath}")
