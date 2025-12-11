import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

#JM: todas las fuentes Times New Roman fueron cambiaros por Arial

class ModuloPacientes:

    def __init__(self, ventana_principal): #JM: ventana_principal es el main
        self.ventana_principal = ventana_principal
        self.ventana = tk.Toplevel(ventana_principal) #JM: combierto ventana en un vantana hija de ventana_principal
        self.ventana.title("Módulo de Pacientes")
        self.ventana.geometry("800x600") #JM: aumente el tamaño de "600x420" a "800x600"
        self.ventana.configure(bg="#FFF9C4")

        self.db = sqlite3.connect("clinica.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT UNIQUE NOT NULL,
                telefono TEXT,
                email TEXT
            )
        """)
        self.db.commit()

        #JM: Titulo
        self.frame_title = tk.Frame(self.ventana, background="#000A91", width=100, height=30)
        self.frame_title.pack(fill="x")
        self.boton_title = tk.Button(
            self.frame_title,
            text="Citas Médicas",
            font=("Arial", 14, "bold"),
            background="#000A91",
            foreground="#FFFFFF",
            borderwidth=0,
            relief="flat",
            command=self.ir_inicio
        )
        self.boton_title.pack()

        #JM: Barra navegación
        self.frame_navbar = tk.Frame(self.ventana, background="#7E7D7D", width=100, height=40)
        self.frame_navbar.pack(fill="x")
        self.frame_navbar.pack_propagate(False)
        self.frame_navbar.columnconfigure(0, weight=1)
        self.frame_navbar.columnconfigure(4, weight=1)

        self.paciente_btn = tk.Button(
            self.frame_navbar, text="Pacientes",
            height=1, width=10, font=("Arial", 12),
            background="#4A90E2", foreground="#F0F0F0",
            borderwidth=2, relief="solid",
            activebackground="#1557A3", activeforeground="#F0F0F0",
            cursor="hand2", command=self.abrir_pacientes
        )
        self.paciente_btn.grid(row=0, column=1, padx=10)

        self.doctores_btn = tk.Button(
            self.frame_navbar, text="Doctores",
            height=1, width=10, font=("Arial", 12),
            background="#4A90E2", foreground="#F0F0F0",
            borderwidth=2, relief="solid",
            activebackground="#1557A3", activeforeground="#F0F0F0",
            cursor="hand2", command=self.abri_doctores
        )
        self.doctores_btn.grid(row=0, column=2, padx=10)

        self.citas_btn = tk.Button(
            self.frame_navbar, text="Citas",
            height=1, width=10, font=("Arial", 12),
            background="#4A90E2", foreground="#F0F0F0",
            borderwidth=2, relief="solid",
            activebackground="#1557A3", activeforeground="#F0F0F0",
            cursor="hand2", command=self.abrir_citas
        )
        self.citas_btn.grid(row=0, column=3, padx=10)

        style = ttk.Style()
        style.configure("Treeview",
                        background="#FFFFFF",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#FFFFFF",
                        font=("Arial", 11))
        style.configure("Treeview.Heading",
                        font=("Arial", 12, "bold"))
        
        frame_form = tk.Frame(self.ventana, bg="#FFFDE7", bd=2, relief="groove")
        frame_form.place(x=10, y=80, width=780, height=150) #JM: aumente Y que era 10, aumente width que era 570 y reduje height que era 170

        tk.Label(frame_form, text="Nombre:", bg="#FFFDE7", font=("Arial", 12)).place(x=20, y=20)
        tk.Label(frame_form, text="Apellido:", bg="#FFFDE7", font=("Arial", 12)).place(x=20, y=60) #JM: Cree la etiqueta para apellido
        tk.Label(frame_form, text="DNI/Cédula:", bg="#FFFDE7", font=("Arial", 12)).place(x=20, y=100)
        tk.Label(frame_form, text="Teléfono:", bg="#FFFDE7", font=("Arial", 12)).place(x=330, y=20) 
        tk.Label(frame_form, text="Email:", bg="#FFFDE7", font=("Arial", 12)).place(x=330, y=60) #JM: Cree la etiqueta para Email

        validar_letras_cmd = self.ventana.register(self.validar_letras)
        validar_numeros_cmd = self.ventana.register(self.validar_numeros)

        self.entry_nombre = tk.Entry(frame_form, width=25, font=("Arial", 11), borderwidth=1, relief="solid",
                                     validate="key",
                                     validatecommand=(validar_letras_cmd, "%d", "%S"))
        self.entry_nombre.place(x=110, y=20) #JM reduje x que ante era de 140

        self.entry_apellido = tk.Entry(frame_form, width=25, font=("Arial", 11), borderwidth=1, relief="solid",
                                       validate="key",
                                       validatecommand=(validar_letras_cmd, "%d", "%S"))
        self.entry_apellido.place(x=110, y=60) #JM cree la entrada para el apellido

        self.entry_cedula = tk.Entry(frame_form, width=25, font=("Arial", 11), borderwidth=1, relief="solid",
                                  validate="key", validatecommand=(validar_numeros_cmd, "%d", "%S"))
        self.entry_cedula.place(x=110, y=100) #JM reduje x que ante era de 140

        self.entry_telefono = tk.Entry(frame_form, width=25, font=("Arial", 11), borderwidth=1, relief="solid",
                                       validate="key", validatecommand=(validar_numeros_cmd, "%d", "%S"))
        self.entry_telefono.place(x=420, y=20) #JM: aumente x ante era 140

        self.entry_email = tk.Entry(frame_form, width=25, font=("Arial", 11), borderwidth=1, relief="solid")
        self.entry_email.place(x=420, y=60) #JM cree la entrada para el apellido

        tk.Button(frame_form, text="Agregar",
                  width=12, command=self.agregar,
                  bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).place(x=650, y=15) #JM: x aumento de 420, para los 3 botones
        tk.Button(frame_form, text="Modificar",
                  width=12, command=self.modificar,
                  bg="#2196F3", fg="white", font=("Arial", 11, "bold")).place(x=650, y=55)
        tk.Button(frame_form, text="Eliminar",
                  width=12, command=self.eliminar,
                  bg="#F44336", fg="white", font=("Arial", 11, "bold")).place(x=650, y=95)

        tk.Label(self.ventana, text="Lista de Pacientes",
                 bg="#FFF9C4",  font=("Arial", 14, "bold")).pack(pady=(240, 0), anchor="w", padx=10) #JM: cambien place por pac

        #JM: cree un frame para posicionar dentro los widgets de la info de los pacientes 
        self.frame_tree = tk.Frame(self.ventana)
        self.frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

        #JM: agregue la barrita para baja y subir si hay muchos pacientes
        scroll_y = tk.Scrollbar(self.frame_tree, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        self.tree = ttk.Treeview(self.frame_tree, #JM: el frame del que  te conte
            columns=("id", "nombre", "apellido", "dni", "telefono", "email"), #JM: agregue apellido y email
            show="headings",
            yscrollcommand=scroll_y.set #JM: vincule el scrol_y con el treeview
        )
        scroll_y.config(command=self.tree.yview) #JM: desplaza el contenido del treeview dependiendo de como lo desplaze el usuario

        self.tree.heading("id", text="ID", anchor="center")
        self.tree.column("id", width=120, stretch=True, anchor="center")

        self.tree.heading("nombre", text="Nombre", anchor="center")
        self.tree.column("nombre", width=120, stretch=True, anchor="center")

        self.tree.heading("apellido", text="Apellido", anchor="center")
        self.tree.column("apellido", width=120, stretch=True, anchor="center")

        self.tree.heading("dni", text="Cedula", anchor="center")
        self.tree.column("dni", width=120, stretch=True, anchor="center")

        self.tree.heading("telefono", text="Teléfono", anchor="center")
        self.tree.column("telefono", width=120, stretch=True, anchor="center")

        self.tree.heading("email", text="Email", anchor="center")
        self.tree.column("email", width=120, stretch=True, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

        self.ventana.update_idletasks()
        self.cargar()

    def validar_letras(self, action, char):
        if action == "1":
            return char.isalpha() or char.isspace()
        return True

    def validar_numeros(self, action, char):
        if action == "1":
            return char.isdigit()
        return True

    def agregar(self):
        if not self.entry_nombre.get() or not self.entry_cedula.get():
            messagebox.showwarning("Error", "Nombre y Cédula son obligatorios")
            return
        try:
            self.cursor.execute(
                "INSERT INTO pacientes(nombre, apellido, dni, telefono, email) VALUES (?, ?, ?, ?, ?)",
                (self.entry_nombre.get(), self.entry_apellido.get(), self.entry_cedula.get(),
                 self.entry_telefono.get(), self.entry_email.get())
            )
            self.db.commit()
        except sqlite3.IntegrityError: #JM:  mensaje si la cedula coincide con otro paciente
            messagebox.showerror("Error", "El DNI/Cedula ya existe")
            return
        self.cargar()
        self.limpiar()

    def modificar(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Error", "Seleccione un paciente")
            return
        item = self.tree.item(seleccionado)
        id_paciente = item["values"][0]

        self.cursor.execute("""
            UPDATE pacientes SET nombre=?, apellido=?, dni=?, telefono=?, email=? WHERE id=?
        """, (self.entry_nombre.get(), self.entry_apellido.get(), self.entry_cedula.get(),
              self.entry_telefono.get(), self.entry_email.get(), id_paciente))
        self.db.commit()
        self.cargar()
        self.limpiar()

    def eliminar(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Error", "Seleccione un paciente")
            return
        item = self.tree.item(seleccionado)
        id_paciente = item["values"][0]

        self.cursor.execute("DELETE FROM pacientes WHERE id=?", (id_paciente,))
        self.db.commit()
        self.cargar()
        self.limpiar()

    def cargar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT * FROM pacientes")
        for paciente in self.cursor.fetchall():
            self.tree.insert("", "end", values=paciente)

    def seleccionar(self, event):
        seleccionado = self.tree.selection()
        if not seleccionado:
            return
        item = self.tree.item(seleccionado)
        id, nombre, apellido, dni, telefono, email = item["values"]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, nombre)
        self.entry_apellido.delete(0, tk.END)
        self.entry_apellido.insert(0, apellido)
        self.entry_cedula.delete(0, tk.END)
        self.entry_cedula.insert(0, dni)
        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono.insert(0, telefono)
        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, email)

    def limpiar(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_cedula.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

    #JM: funciones para la navegacion
    def ir_inicio(self):
        self.ventana.destroy()
        self.ventana_principal.deiconify()

    def abrir_pacientes(self):
        self.ventana_principal.abrir_pacientes()

    def abri_doctores(self):
        self.ventana_principal.abrir_doctores()

    def abrir_citas(self):
        self.ventana_principal.abrir_citas()
