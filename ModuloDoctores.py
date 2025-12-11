import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class ModuloDoctores:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal  #JM: guardo la ventana principal
        self.ventana = tk.Toplevel(ventana_principal) 
        self.ventana.title("Gestión de Doctores")
        self.ventana.geometry("900x600")
        self.ventana.configure(bg='#f0f8ff')
        self.ventana.resizable(True, True)
        
        self.conexion = sqlite3.connect('doctores.db')
        self.crear_tabla()
        
        self.especialidades = [
            "Alergología", "Anestesiología", "Angiología", "Cardiología",
            "Cirugía Cardiovascular", "Cirugía General", "Cirugía Maxilofacial",
            "Cirugía Pediátrica", "Cirugía Plástica", "Cirugía Torácica",
            "Dermatología", "Endocrinología", "Gastroenterología",
            "Genética Médica", "Geriatría", "Ginecología y Obstetricia",
            "Hematología", "Hematología Pediátrica", "Hepatología",
            "Infectología", "Inmunología", "Medicina Aeroespacial",
            "Medicina del Deporte", "Medicina del Trabajo", "Medicina de Urgencias",
            "Medicina Familiar", "Medicina Física y Rehabilitación",
            "Medicina Interna", "Medicina Intensiva", "Medicina Legal",
            "Medicina Nuclear", "Medicina Preventiva", "Medicina del Sueño",
            "Nefrología", "Neonatología", "Neumología", "Neurocirugía",
            "Neurofisiología Clínica", "Neurología", "Nutriología Clínica",
            "Oftalmología", "Oncología Médica", "Oncología Radioterápica",
            "Ortopedia y Traumatología", "Otorrinolaringología", "Patología",
            "Pediatría", "Psiquiatría", "Psiquiatría Infantil",
            "Radiología", "Radioterapia", "Reumatología", "Toxicología",
            "Urología", "Venereología", "Anatomía Patológica",
            "Bioquímica Clínica", "Epidemiología", "Farmacología Clínica",
            "Medicina Forense", "Medicina Tropical", "Salud Pública",
            "Cirugía Oncológica", "Cirugía Vascular", "Dermatopatología",
            "Endoscopia", "Fertología", "Hematopatología",
            "Hemoterapia", "Inmunopatología", "Micología",
            "Nefropatología", "Neuropatología", "Oncopatología",
            "Ortoptía", "Osteopatía", "Parasitología",
            "Patología Molecular", "Proctología", "Reumatología Pediátrica",
            "Sexología", "Terapia Intensiva Pediátrica", "Vascularología"
        ]
        
        self.horarios = [
            "07:00 - 11:00", "08:00 - 12:00", "09:00 - 13:00",
            "10:00 - 14:00", "11:00 - 15:00", "12:00 - 16:00",
            "13:00 - 17:00", "14:00 - 18:00", "15:00 - 19:00",
            "16:00 - 20:00", "17:00 - 21:00", "18:00 - 22:00",
            "Turno de noche", "Turno de madrugada", "Horario flexible",
            "Solo citas", "Guardia 24/7"
        ]
        
        self.crear_widgets()
        self.cargar_doctores()
    
    def crear_tabla(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especialidad TEXT NOT NULL,
                horario TEXT NOT NULL
            )
        ''')
        self.conexion.commit()
    
    def crear_widgets(self):
        #JM: Titulo
        self.frame_title = tk.Frame(self.ventana, background="#000A91", width=100, height=30)
        self.frame_title.pack(fill="x")
        
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
        
        #JM: Cree el frame de la barra de navegacion y los botones
        self.frame_navbar = tk.Frame(self.ventana, background="#7C7C7C", width=100, height=40)
        self.frame_navbar.pack(fill="x")
        self.frame_navbar.pack_propagate(False)
        self.frame_navbar.columnconfigure(0, weight=1)
        self.frame_navbar.columnconfigure(4, weight=1)
        
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
        
        # Frame principal
        frame_principal = tk.Frame(self.ventana, bg='#f0f8ff')
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configuracion de grid 
        frame_principal.grid_rowconfigure(0, weight=1)
        frame_principal.grid_rowconfigure(1, weight=2)
        frame_principal.grid_columnconfigure(0, weight=1)
        
        # Frame superior - Formulario
        frame_formulario = tk.LabelFrame(frame_principal, text="Formulario de Doctor", 
                                        font=("Arial", 12, "bold"),
                                        bg='#e6f2ff', fg='#003366',
                                        relief=tk.RIDGE, bd=2)
        frame_formulario.grid(row=0, column=0, sticky="nsew", padx=5, pady=(0, 10))
        
        # Frame 
        frame_tabla = tk.LabelFrame(frame_principal, text="Lista de Doctores", 
                                   font=("Arial", 12, "bold"),
                                   bg='#e6f2ff', fg='#003366',
                                   relief=tk.RIDGE, bd=2)
        frame_tabla.grid(row=1, column=0, sticky="nsew", padx=5)
        
        # Configuracion de grid del formulario
        for i in range(3):
            frame_formulario.grid_columnconfigure(i, weight=1)
        
        # Formulario de Nombre
        tk.Label(frame_formulario, text="Nombre:", 
                font=("Arial", 10, "bold"),
                bg='#e6f2ff', fg='#003366').grid(row=0, column=0, sticky=tk.W, padx=15, pady=12)
        
        self.entry_nombre = tk.Entry(frame_formulario, font=("Arial", 10),
                                    relief=tk.SOLID, bd=1)
        self.entry_nombre.grid(row=0, column=1, padx=15, pady=12, sticky="ew")
        
        # Formulario de Especialidad
        tk.Label(frame_formulario, text="Especialidad:", 
                font=("Arial", 10, "bold"),
                bg='#e6f2ff', fg='#003366').grid(row=0, column=2, sticky=tk.W, padx=15, pady=12)
        
        self.combo_especialidad = ttk.Combobox(frame_formulario, 
                                              values=self.especialidades,
                                              font=("Arial", 10),
                                              state="readonly")
        self.combo_especialidad.grid(row=0, column=3, padx=15, pady=12, sticky="ew")
        self.combo_especialidad.current(0)
        
        # Formulario de Horario
        tk.Label(frame_formulario, text="Horario:", 
                font=("Arial", 10, "bold"),
                bg='#e6f2ff', fg='#003366').grid(row=1, column=0, sticky=tk.W, padx=15, pady=12)
        
        self.combo_horario = ttk.Combobox(frame_formulario, 
                                         values=self.horarios,
                                         font=("Arial", 10),
                                         state="readonly")
        self.combo_horario.grid(row=1, column=1, padx=15, pady=12, sticky="ew")
        self.combo_horario.current(0)
        
        # Frame para botones del formulario
        frame_botones_form = tk.Frame(frame_formulario, bg='#e6f2ff')
        frame_botones_form.grid(row=1, column=2, columnspan=2, padx=15, pady=12)
        
        # Botones CRUD
        tk.Button(frame_botones_form, text="Agregar", 
                 command=self.agregar_doctor,
                 font=("Arial", 10, "bold"),
                 bg='#4CAF50', fg='white',
                 width=12, relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones_form, text="Actualizar", 
                 command=self.actualizar_doctor,
                 font=("Arial", 10, "bold"),
                 bg="#1D71B6", fg='white',
                 width=12, relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones_form, text="Eliminar", 
                 command=self.eliminar_doctor,
                 font=("Arial", 10, "bold"),
                 bg='#f44336', fg='white',
                 width=12, relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones_form, text="Limpiar", 
                 command=self.limpiar_formulario,
                 font=("Arial", 10, "bold"),
                 bg='#FF9800', fg='white',
                 width=12, relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
        
        # Tabla Treeview en la parte baja
        frame_tabla_interna = tk.Frame(frame_tabla, bg='#e6f2ff')
        frame_tabla_interna.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        scroll_y = tk.Scrollbar(frame_tabla_interna)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = tk.Scrollbar(frame_tabla_interna, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.tabla_doctores = ttk.Treeview(frame_tabla_interna,
                                          columns=('ID', 'Nombre', 'Especialidad', 'Horario'),
                                          show='headings',
                                          yscrollcommand=scroll_y.set,
                                          xscrollcommand=scroll_x.set)
        
        # Configurar columnas
        self.tabla_doctores.column('ID', width=60, anchor=tk.CENTER)
        self.tabla_doctores.column('Nombre', width=250, anchor=tk.W)
        self.tabla_doctores.column('Especialidad', width=200, anchor=tk.W)
        self.tabla_doctores.column('Horario', width=150, anchor=tk.W)
        
        # Configurar encabezados
        self.tabla_doctores.heading('ID', text='ID')
        self.tabla_doctores.heading('Nombre', text='Nombre')
        self.tabla_doctores.heading('Especialidad', text='Especialidad')
        self.tabla_doctores.heading('Horario', text='Horario')
        
        self.tabla_doctores.pack(fill=tk.BOTH, expand=True)
        
        scroll_y.config(command=self.tabla_doctores.yview)
        scroll_x.config(command=self.tabla_doctores.xview)
        
        # Bind para selección
        self.tabla_doctores.bind('<<TreeviewSelect>>', self.seleccionar_doctor)
    
    def agregar_doctor(self):
        nombre = self.entry_nombre.get().strip()
        especialidad = self.combo_especialidad.get()
        horario = self.combo_horario.get()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre es requerido")
            return
        
        cursor = self.conexion.cursor()
        cursor.execute('''
            INSERT INTO doctores (nombre, especialidad, horario)
            VALUES (?, ?, ?)
        ''', (nombre, especialidad, horario))
        self.conexion.commit()
        
        messagebox.showinfo("Éxito", "Doctor agregado correctamente")
        self.limpiar_formulario()
        self.cargar_doctores()
    
    def cargar_doctores(self):
        # Limpiar tabla
        for item in self.tabla_doctores.get_children():
            self.tabla_doctores.delete(item)
        
        cursor = self.conexion.cursor()
        cursor.execute('SELECT * FROM doctores ORDER BY nombre')
        doctores = cursor.fetchall()
        
        for doctor in doctores:
            self.tabla_doctores.insert('', tk.END, values=doctor)
    
    def seleccionar_doctor(self, event):
        seleccion = self.tabla_doctores.selection()
        if seleccion:
            item = self.tabla_doctores.item(seleccion[0])
            valores = item['values']
            
            if valores:
                self.entry_nombre.delete(0, tk.END)
                self.entry_nombre.insert(0, valores[1])
                self.combo_especialidad.set(valores[2])
                self.combo_horario.set(valores[3])
    
    def actualizar_doctor(self):
        seleccion = self.tabla_doctores.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un doctor para actualizar")
            return
        
        item = self.tabla_doctores.item(seleccion[0])
        id_doctor = item['values'][0]
        
        nombre = self.entry_nombre.get().strip()
        especialidad = self.combo_especialidad.get()
        horario = self.combo_horario.get()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre es requerido")
            return
        
        cursor = self.conexion.cursor()
        cursor.execute('''
            UPDATE doctores 
            SET nombre = ?, especialidad = ?, horario = ?
            WHERE id = ?
        ''', (nombre, especialidad, horario, id_doctor))
        self.conexion.commit()
        
        messagebox.showinfo("Éxito", "Doctor actualizado correctamente")
        self.cargar_doctores()
    
    def eliminar_doctor(self):
        seleccion = self.tabla_doctores.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un doctor para eliminar")
            return
        
        confirmacion = messagebox.askyesno("Confirmar", 
                                          "¿Está seguro de eliminar este doctor?")
        if confirmacion:
            item = self.tabla_doctores.item(seleccion[0])
            id_doctor = item['values'][0]
            
            cursor = self.conexion.cursor()
            cursor.execute('DELETE FROM doctores WHERE id = ?', (id_doctor,))
            self.conexion.commit()
            
            messagebox.showinfo("Éxito", "Doctor eliminado correctamente")
            self.limpiar_formulario()
            self.cargar_doctores()
    
    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.combo_especialidad.current(0)
        self.combo_horario.current(0)
        self.tabla_doctores.selection_remove(self.tabla_doctores.selection())
    
    def cerrar(self):
        self.conexion.close()
        self.ventana.destroy()
        
    #JM: funciones para navegar entre secciones
    def ir_inicio(self):
        self.ventana.destroy()
        self.ventana_principal.deiconify()
       
    def abrir_pacientes(self):
        self.ventana_principal.abrir_pacientes()

    def abri_doctores(self):
        self.ventana_principal.abrir_doctores()

    def abrir_citas(self):
        self.ventana_principal.abrir_citas()

