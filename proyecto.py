import tkinter as tk

contadorun = 0
contadordo = 0
contadortr = 0
contadorcu = 0

boton_vacu = None
boton_vacd = None
boton_vact = None
boton_vacc = None

def vacaciones_uno():
    global contadorun
    global boton_vacu
    contadorun += 1
    if contadorun >= 3:
        if boton_vacu:
            boton_vacu.config(state=tk.DISABLED)

def vacaciones_dos():
    global contadordo
    global boton_vacd
    contadordo += 1
    if contadordo >= 3:
        if boton_vacd:
            boton_vacd.config(state=tk.DISABLED)

def vacaciones_tres():
    global contadortr
    global boton_vact
    contadortr += 1
    if contadortr >= 3:
        if boton_vact:
            boton_vact.config(state=tk.DISABLED)

def vacaciones_cuatro():
    global contadorcu
    global boton_vacc
    contadorcu += 1
    if contadorcu >= 3:
        if boton_vacc:
            boton_vacc.config(state=tk.DISABLED)

def abrir_ventana_vacaciones():
    ventana_principal.withdraw()

    ventana_vacaciones = tk.Toplevel(ventana_principal)
    ventana_vacaciones.title("Vacaciones Disponibles")
    ventana_vacaciones.geometry("400x400")

    tk.Label(ventana_vacaciones, text="Fechas de Vacaciones", font=("Arial", 14)).pack(pady=10)

    global boton_vacu, boton_vacd, boton_vact, boton_vacc

    boton_vacu = tk.Button(ventana_vacaciones, text="Enero-Febrero", command=vacaciones_uno)
    boton_vacu.pack(pady=5)

    boton_vacd = tk.Button(ventana_vacaciones, text="Marzo-Abril", command=vacaciones_dos)
    boton_vacd.pack(pady=5)

    boton_vact = tk.Button(ventana_vacaciones, text="Junio-Julio", command=vacaciones_tres)
    boton_vact.pack(pady=5)

    boton_vacc = tk.Button(ventana_vacaciones, text="Nov-Dic", command=vacaciones_cuatro)
    boton_vacc.pack(pady=5)

    def volver_a_principal():
        ventana_vacaciones.destroy()
        ventana_principal.deiconify()

    tk.Button(ventana_vacaciones, text="Volver a Ingreso de Estudiantes", command=volver_a_principal).pack(pady=20)

class registro:
    def __init__(self, nombre, edad, genero, curp, nss):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.curp = curp
        self.nss = nss

    def obtener_texto_registro(self):
        return f"{self.nombre} registrado con el número {self.nss}"

def registrar_estudiante_desde_gui():
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    genero = entry_genero.get()
    curp = entry_curp.get()
    nss = entry_nss.get()

    nuevo_estudiante = registro(nombre, edad, genero, curp, nss)

    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_genero.delete(0, tk.END)
    entry_curp.delete(0, tk.END)
    entry_nss.delete(0, tk.END)

    tk.Label(ventana_principal, text=nuevo_estudiante.obtener_texto_registro(), background="lightgreen").pack(pady=5)


ventana_principal = tk.Tk()
ventana_principal.title("Ingreso de Estudiantes")
ventana_principal.geometry("500x550")

tk.Label(ventana_principal, text="Nombre:").pack(pady=2)
entry_nombre = tk.Entry(ventana_principal)
entry_nombre.pack(pady=2)

tk.Label(ventana_principal, text="Edad:").pack(pady=2)
entry_edad = tk.Entry(ventana_principal)
entry_edad.pack(pady=2)

tk.Label(ventana_principal, text="Género:").pack(pady=2)
entry_genero = tk.Entry(ventana_principal)
entry_genero.pack(pady=2)

tk.Label(ventana_principal, text="CURP:").pack(pady=2)
entry_curp = tk.Entry(ventana_principal)
entry_curp.pack(pady=2)

tk.Label(ventana_principal, text="NSS:").pack(pady=2)
entry_nss = tk.Entry(ventana_principal)
entry_nss.pack(pady=2)


btn_registrar = tk.Button(ventana_principal, text="Registrar Estudiante", command=registrar_estudiante_desde_gui)
btn_registrar.pack(pady=15)

tk.Frame(ventana_principal, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=10, pady=10)

boton_abrir_vacaciones = tk.Button(ventana_principal, text="Ver Vacaciones", command=abrir_ventana_vacaciones)
boton_abrir_vacaciones.pack(pady=20)

ventana_principal.mainloop()
