import tkinter as tk
import os
from CRUD_Pacientes import ModuloPacientes
from ModuloDoctores import ModuloDoctores
from AgendarCitas import ModuloCitasApp

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Citas Medicas")
        self.geometry("800x500")

        # Imagen de fondo
        self.bg_label = tk.Label(self)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        ruta_imagen = os.path.join(os.path.dirname(__file__), "img","Red de Salud y medicina.png")
        self.original_img = tk.PhotoImage(file=ruta_imagen)
        self.bg_label.config(image=self.original_img)      

        # Variables para controlar los toplevel
        self.ventana_pacientes = None
        self.ventana_doctores = None
        self.ventana_citas = None

        self.create_widgets()

    # crea los widgets 
    def create_widgets(self):
        # Titulo
        self.frame_titulo = tk.Frame(self, background="#000A91", width=100, height=30)
        self.frame_titulo.pack(fill="x")
        self.frame_titulo.pack_propagate(False)
        self.label_titulo = tk.Label(self.frame_titulo, text="CITAS MEDICAS", font=("Arial", 12, "bold"), background="#000A91", foreground="#FFFFFF")
        self.label_titulo.pack()

        # navbar
        self.frame_navbar = tk.Frame(self, background="#7C7C7C", width=100, height=30)
        self.frame_navbar.pack(fill="x")
        self.frame_navbar.pack_propagate(False)
        self.frame_navbar.columnconfigure(0, weight=1)
        self.frame_navbar.columnconfigure(4, weight=1)

        # botones
        self.pacientes_btn = tk.Button(
            self.frame_navbar,
            text="Pacientes",
            height=1,
            width=10,
            font=("Arial", 12),
            background="#4A90E2",
            foreground="#FFFFFF",
            activebackground="#28507E",
            activeforeground="#FFFFFF",
            borderwidth=2,
            relief="solid",
            cursor="hand2",
            command=self.abrir_pacientes
        )
        self.pacientes_btn.grid(row=0, column=1, padx=10)

        self.doctores_btn = tk.Button(
            self.frame_navbar,
            text="Doctores",
            height=1,
            width=10,
            font=("Arial", 12),
            background="#4A90E2",
            foreground="#FFFFFF",
            activebackground= "#28507E",
            activeforeground="#FFFFFF",
            borderwidth=2,
            relief="solid",
            cursor="hand2",
            command=self.abrir_doctores
        )
        self.doctores_btn.grid(row=0, column=2, padx=10)

        self.citas_btn = tk.Button(
            self.frame_navbar,
            text="Citas",
            height=1,
            width=10,
            font=("Arial", 12),
            background="#4A90E2",
            foreground="#FFFFFF",
            activebackground= "#28507E",
            activeforeground="#FFFFFF",
            borderwidth=2,
            relief="solid",
            cursor="hand2",
            command=self.abrir_citas
        )
        self.citas_btn.grid(row=0, column=3, padx=10)

    #  funcion para abrir los toplevel
    def abrir_pacientes(self):
        if self.ventana_pacientes and tk.Toplevel.winfo_exists(self.ventana_pacientes.ventana):
            self.ventana_pacientes.ventana.lift()
            return
        self.withdraw()
        self.ventana_pacientes = ModuloPacientes(self)
        self.ventana_pacientes.ventana.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.cerrar_ventana("pacientes")
        )

    def abrir_doctores(self):
        if self.ventana_doctores and tk.Toplevel.winfo_exists(self.ventana_doctores.ventana):
            self.ventana_doctores.ventana.lift()
            return
        self.withdraw()
        self.ventana_doctores = ModuloDoctores(self)
        self.ventana_doctores.ventana.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.cerrar_ventana("doctores")
        )

    def abrir_citas(self):
        if self.ventana_citas and tk.Toplevel.winfo_exists(self.ventana_citas.root):
            self.ventana_citas.root.lift()
            return
        self.withdraw()
        self.ventana_citas = ModuloCitasApp(self)
        self.ventana_citas.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.cerrar_ventana("citas")
        )



    # funcion para cuando se cierre un top level
    def cerrar_ventana(self, tipo):
        if tipo == "pacientes" and self.ventana_pacientes:
            self.ventana_pacientes.ventana.destroy()
            self.ventana_pacientes = None
        elif tipo == "doctores" and self.ventana_doctores:
            self.ventana_doctores.ventana.destroy()
            self.ventana_doctores = None
        elif tipo == "citas" and self.ventana_citas:
            self.ventana_citas.root.destroy()
            self.ventana_citas = None
        self.deiconify()

if __name__ == "__main__":
    app = Root()
    app.mainloop()
