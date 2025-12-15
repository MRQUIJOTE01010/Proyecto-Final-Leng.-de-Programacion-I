import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

def crear_bd():
    conn = sqlite3.connect("clinica_responsive.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente TEXT NOT NULL,
            doctor TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            motivo TEXT
        )
    """)
    conn.commit()
    conn.close()

class AgendaResponsive:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Médica - Responsive")
        self.root.state("zoomed")

        self.color_azul = "#A7C7E7"
        self.color_amarillo = "#FFF7AE"

        for i in range(3):
            root.grid_rowconfigure(i, weight=1)
        for i in range(3):
            root.grid_columnconfigure(i, weight=1)

        self.crear_interfaz()
        self.cargar_citas()

    def crear_interfaz(self):
        self.frame_form = tk.Frame(self.root, bg=self.color_azul, bd=4, relief="ridge")
        self.frame_form.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        for i in range(4):
            self.frame_form.grid_columnconfigure(i, weight=1)

        ttk.Label(self.frame_form, text="Paciente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_paciente = ttk.Entry(self.frame_form)
        self.entry_paciente.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_form, text="Doctor:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_doctor = ttk.Entry(self.frame_form)
        self.entry_doctor.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_form, text="Fecha:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_fecha = DateEntry(self.frame_form, date_pattern="yyyy-mm-dd")
        self.entry_fecha.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_form, text="Hora:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_hora = ttk.Entry(self.frame_form)
        self.entry_hora.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_form, text="Motivo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_motivo = ttk.Entry(self.frame_form)
        self.entry_motivo.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        btn_guardar = ttk.Button(self.frame_form, text="Guardar Cita", command=self.guardar_cita)
        btn_guardar.grid(row=3, column=0, columnspan=4, pady=10, sticky="ew")

        self.frame_tabla = tk.Frame(self.root, bg=self.color_amarillo, bd=4, relief="ridge")
        self.frame_tabla.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.frame_tabla.grid_rowconfigure(0, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        columnas = ("id", "paciente", "doctor", "fecha", "hora", "motivo")
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=150)

        self.tabla.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.frame_botones = tk.Frame(self.root, bg=self.color_azul)
        self.frame_botones.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        for i in range(3):
            self.frame_botones.grid_columnconfigure(i, weight=1)

        ttk.Button(self.frame_botones, text="Editar", command=self.editar_cita).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Button(self.frame_botones, text="Eliminar", command=self.eliminar_cita).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ttk.Button(self.frame_botones, text="Actualizar", command=self.cargar_citas).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    def guardar_cita(self):
        paciente = self.entry_paciente.get()
        doctor = self.entry_doctor.get()
        fecha = self.entry_fecha.get()
        hora = self.entry_hora.get()
        motivo = self.entry_motivo.get()

        if not (paciente and doctor and fecha and hora):
            messagebox.showwarning("Error", "Todos los campos excepto 'motivo' son obligatorios.")
            return

        conn = sqlite3.connect("clinica_responsive.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO citas (paciente, doctor, fecha, hora, motivo) VALUES (?, ?, ?, ?, ?)",
                       (paciente, doctor, fecha, hora, motivo))

        conn.commit()
        conn.close()

        self.cargar_citas()
        messagebox.showinfo("Éxito", "Cita guardada correctamente.")

    def cargar_citas(self):
        conn = sqlite3.connect("clinica_responsive.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM citas")
        filas = cursor.fetchall()

        conn.close()

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for fila in filas:
            self.tabla.insert("", "end", values=fila)

    def eliminar_cita(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return messagebox.showwarning("Error", "Seleccione una cita primero.")

        cita_id = self.tabla.item(seleccion[0], "values")[0]

        conn = sqlite3.connect("clinica_responsive.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM citas WHERE id=?", (cita_id,))
        conn.commit()
        conn.close()

        self.cargar_citas()
        messagebox.showinfo("Éxito", "Cita eliminada correctamente.")

    def editar_cita(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return messagebox.showwarning("Error", "Seleccione una cita para editar.")

        datos = self.tabla.item(seleccion[0], "values")
        self.entry_paciente.delete(0, tk.END)
        self.entry_doctor.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.entry_motivo.delete(0, tk.END)

        self.entry_paciente.insert(0, datos[1])
        self.entry_doctor.insert(0, datos[2])
        self.entry_fecha.set_date(datos[3])
        self.entry_hora.insert(0, datos[4])
        self.entry_motivo.insert(0, datos[5])

if __name__ == "__main__":
    crear_bd()
    root = tk.Tk()
    app = AgendaResponsive(root)
    root.mainloop()
