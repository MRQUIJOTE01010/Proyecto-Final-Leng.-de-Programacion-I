import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class ModuloPacientes:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Módulo de Pacientes")
        self.ventana.geometry("600x420")
        self.ventana.configure(bg="#FFF9C4")

        self.db = sqlite3.connect("clinica.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cedula TEXT NOT NULL,
                telefono TEXT
            )
        """)
        self.db.commit()

        style = ttk.Style()
        style.configure("Treeview",
                        background="#FFFFFF",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#FFFFFF",
                        font=("Times New Roman", 11))
        style.configure("Treeview.Heading",
                        font=("Times New Roman", 12, "bold"))

        frame_form = tk.Frame(self.ventana, bg="#FFFDE7", bd=2, relief="groove")
        frame_form.place(x=10, y=10, width=570, height=170)

        tk.Label(frame_form, text="Nombre:", bg="#FFFDE7", font=("Times New Roman", 12)).place(x=20, y=20)
        tk.Label(frame_form, text="DNI/Cédula:", bg="#FFFDE7", font=("Times New Roman", 12)).place(x=20, y=60)
        tk.Label(frame_form, text="Teléfono:", bg="#FFFDE7", font=("Times New Roman", 12)).place(x=20, y=100)

        validar_letras_cmd = self.ventana.register(self.validar_letras)
        validar_numeros_cmd = self.ventana.register(self.validar_numeros)

        self.entry_nombre = tk.Entry(frame_form, width=30, font=("Times New Roman", 11),
                                     validate="key",
                                     validatecommand=(validar_letras_cmd, "%d", "%S"))
        self.entry_nombre.place(x=140, y=20)

        self.entry_cedula = tk.Entry(frame_form, width=30, font=("Times New Roman", 11),
                                     validate="key",
                                     validatecommand=(validar_numeros_cmd, "%d", "%S"))
        self.entry_cedula.place(x=140, y=60)

        self.entry_telefono = tk.Entry(frame_form, width=30, font=("Times New Roman", 11),
                                       validate="key",
                                       validatecommand=(validar_numeros_cmd, "%d", "%S"))
        self.entry_telefono.place(x=140, y=100)

        tk.Button(frame_form, text="Agregar",
                  width=12, command=self.agregar,
                  bg="#4CAF50", fg="white", font=("Times New Roman", 11, "bold")).place(x=420, y=15)

        tk.Button(frame_form, text="Modificar",
                  width=12, command=self.modificar,
                  bg="#2196F3", fg="white", font=("Times New Roman", 11, "bold")).place(x=420, y=55)

        tk.Button(frame_form, text="Eliminar",
                  width=12, command=self.eliminar,
                  bg="#F44336", fg="white", font=("Times New Roman", 11, "bold")).place(x=420, y=95)

        tk.Label(self.ventana, text="Lista de Pacientes",
                 bg="#FFF9C4", font=("Times New Roman", 14, "bold")).place(x=20, y=190)

        self.tree = ttk.Treeview(self.ventana,
                                 columns=("id", "nombre", "cedula", "telefono"),
                                 show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("cedula", text="Cédula")
        self.tree.heading("telefono", text="Teléfono")

        self.tree.column("id", width=50)
        self.tree.column("nombre", width=150)
        self.tree.column("cedula", width=120)
        self.tree.column("telefono", width=120)

        self.tree.place(x=20, y=220)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

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

        self.cursor.execute(
            "INSERT INTO pacientes(nombre, cedula, telefono) VALUES (?, ?, ?)",
            (self.entry_nombre.get(), self.entry_cedula.get(), self.entry_telefono.get()))
        self.db.commit()

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
            UPDATE pacientes SET nombre=?, cedula=?, telefono=? WHERE id=?
        """, (self.entry_nombre.get(), self.entry_cedula.get(),
              self.entry_telefono.get(), id_paciente))

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
        id, nombre, cedula, telefono = item["values"]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, nombre)

        self.entry_cedula.delete(0, tk.END)
        self.entry_cedula.insert(0, cedula)

        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono.insert(0, telefono)

    def limpiar(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_cedula.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    ModuloPacientes(root)
    root.mainloop()