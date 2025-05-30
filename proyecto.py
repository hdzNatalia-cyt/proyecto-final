import tkinter as tk

contadorun = 0
contadordo = 0
contadortr = 0
contadorcu = 0

boton_vacu = None
boton_vacd = None
boton_vact = None
boton_vacc = None

class ManejadorVacaciones:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_vacaciones = None

    def vacaciones_uno(self):
        global contadorun, boton_vacu
        contadorun += 1
        if contadorun >= 3:
            if boton_vacu:
                boton_vacu.config(state=tk.DISABLED)

    def vacaciones_dos(self):
        global contadordo, boton_vacd
        contadordo += 1
        if contadordo >= 3:
            if boton_vacd:
                boton_vacd.config(state=tk.DISABLED)

    def vacaciones_tres(self):
        global contadortr, boton_vact
        contadortr += 1
        if contadortr >= 3:
            if boton_vact:
                boton_vact.config(state=tk.DISABLED)

    def vacaciones_cuatro(self):
        global contadorcu, boton_vacc
        contadorcu += 1
        if contadorcu >= 3:
            if boton_vacc:
                boton_vacc.config(state=tk.DISABLED)

    def abrir_ventana_vacaciones(self):
        global boton_vacu, boton_vacd, boton_vact, boton_vacc

        self.ventana_principal.withdraw()

        self.ventana_vacaciones = tk.Toplevel(self.ventana_principal)
        self.ventana_vacaciones.title("Vacaciones Disponibles")
        self.ventana_vacaciones.geometry("400x400")

        tk.Label(self.ventana_vacaciones, text="Fechas de Vacaciones", font=("Arial", 14)).pack(pady=10)

        boton_vacu = tk.Button(self.ventana_vacaciones, text="Enero-Febrero", command=self.vacaciones_uno)
        boton_vacu.pack(pady=5)
        if contadorun >= 3:
            boton_vacu.config(state=tk.DISABLED)

        boton_vacd = tk.Button(self.ventana_vacaciones, text="Marzo-Abril", command=self.vacaciones_dos)
        boton_vacd.pack(pady=5)
        if contadordo >= 3:
            boton_vacd.config(state=tk.DISABLED)

        boton_vact = tk.Button(self.ventana_vacaciones, text="Junio-Julio", command=self.vacaciones_tres)
        boton_vact.pack(pady=5)
        if contadortr >= 3:
            boton_vact.config(state=tk.DISABLED)

        boton_vacc = tk.Button(self.ventana_vacaciones, text="Nov-Dic", command=self.vacaciones_cuatro)
        boton_vacc.pack(pady=5)
        if contadorcu >= 3:
            boton_vacc.config(state=tk.DISABLED)

        def volver_a_principal():
            self.ventana_vacaciones.destroy()
            self.ventana_principal.deiconify()

        tk.Button(self.ventana_vacaciones, text="Volver al Menú Principal", command=volver_a_principal).pack(pady=20)

        self.ventana_vacaciones.protocol("WM_DELETE_WINDOW", volver_a_principal)

def pasar_asistencia():
    ventana_menu.withdraw()

    ventana_asistencia = tk.Toplevel(ventana_menu)
    ventana_asistencia.title("Pasar Asistencia")
    ventana_asistencia.geometry("400x550")

    def volver_desde_asistencia():
         ventana_asistencia.destroy()
         ventana_menu.deiconify()

    btn_volver = tk.Button(ventana_asistencia, text="Volver al Menú Principal", command=volver_desde_asistencia)
    btn_volver.pack(pady=10)

    ventana_asistencia.protocol("WM_DELETE_WINDOW", volver_desde_asistencia)

def agregar_trabajador_ven():
    ventana_menu.withdraw()

    ventana_menudos = tk.Toplevel(ventana_menu)
    ventana_menudos.title("Nuevo Trabajador")
    ventana_menudos.geometry("400x550")

    mensaje_registro_label = tk.Label(ventana_menudos, text="", fg="green")
    mensaje_registro_label.pack(pady=5)


    class Registro:
        def __init__(self, nombre, edad, genero, curp, nss):
            self.nombre = nombre
            self.edad = edad
            self.genero = genero
            self.curp = curp
            self.nss = nss

        def obtener_texto_registro(self):
            return f"'{self.nombre}' registrado con el NSS: {self.nss}"

    def registrar_trabajador():
        nombre = entry_nombre.get()
        edad = entry_edad.get()
        genero = entry_genero.get()
        curp = entry_curp.get()
        nss = entry_nss.get()

        nuevo_trabajador = Registro(nombre, edad, genero, curp, nss)

        mensaje_registro_label.config(text=nuevo_trabajador.obtener_texto_registro())

        # Limpia los campos de entrada
        entry_nombre.delete(0, tk.END)
        entry_edad.delete(0, tk.END)
        entry_genero.delete(0, tk.END)
        entry_curp.delete(0, tk.END)
        entry_nss.delete(0, tk.END)

    tk.Label(ventana_menudos, text="Nombre:").pack(pady=2)
    entry_nombre = tk.Entry(ventana_menudos)
    entry_nombre.pack(pady=2)

    tk.Label(ventana_menudos, text="Edad:").pack(pady=2)
    entry_edad = tk.Entry(ventana_menudos)
    entry_edad.pack(pady=2)

    tk.Label(ventana_menudos, text="Género:").pack(pady=2)
    entry_genero = tk.Entry(ventana_menudos)
    entry_genero.pack(pady=2)

    tk.Label(ventana_menudos, text="CURP:").pack(pady=2)
    entry_curp = tk.Entry(ventana_menudos)
    entry_curp.pack(pady=2)

    tk.Label(ventana_menudos, text="NSS:").pack(pady=2)
    entry_nss = tk.Entry(ventana_menudos)
    entry_nss.pack(pady=2)

    btn_registrar = tk.Button(ventana_menudos, text="Registrar trabajador", command=registrar_trabajador)
    btn_registrar.pack(pady=15)

    def volver_menudos():
        ventana_menudos.destroy()
        ventana_menu.deiconify()

    btn_volver = tk.Button(ventana_menudos, text="Volver al Menú Principal", command=volver_menudos)
    btn_volver.pack(pady=10)

    ventana_menudos.protocol("WM_DELETE_WINDOW", volver_menudos)


ventana_menu = tk.Tk()
ventana_menu.title("Menú Inicial")
ventana_menu.geometry("500x300")

tk.Label(ventana_menu, text="Bienvenido, escoja qué desea realizar").pack(pady=20)

boton_opc1re = tk.Button(ventana_menu, text="Agregar nuevo trabajador", command=agregar_trabajador_ven)
boton_opc1re.pack(pady=10)

boton_asis = tk.Button(ventana_menu, text="Pasar asistencia a trabajador", command=pasar_asistencia)
boton_asis.pack(pady=10)

manejador_vacaciones_instancia = ManejadorVacaciones(ventana_menu)

btn_vacaciones = tk.Button(ventana_menu, text="Ver Vacaciones Disponibles", command=manejador_vacaciones_instancia.abrir_ventana_vacaciones)
btn_vacaciones.pack(pady=10)

ventana_menu.mainloop()
