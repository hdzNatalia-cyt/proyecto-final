import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

lista_trabajadores_registrados = []

contadorun = 0
contadordo = 0
contadortr = 0
contadorcu = 0


boton_vacu = None
boton_vacd = None
boton_vact = None
boton_vacc = None

historial_actividades = []

class Trabajador:
    def __init__(self, nombre, edad, genero, curp, nss, horario):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.curp = curp
        self.nss = nss
        self.horario = horario
        self.vacaciones_solicitadas_individual = {
            "Enero-Febrero": 0,
            "Marzo-Abril": 0,
            "Junio-Julio": 0,
            "Nov-Dic": 0,
        }

    def obtener_texto_para_lista(self):
        return f"{self.nombre} (NSS: {self.nss})"

    def obtener_conteo_vacaciones_individual(self, periodo):
        return self.vacaciones_solicitadas_individual.get(periodo, 0)

    def registrar_vacaciones_individual(self, periodo):
        if self.vacaciones_solicitadas_individual.get(periodo, 0) < 3:
            self.vacaciones_solicitadas_individual[periodo] += 1
            return True
        return False

class ManejadorVacaciones:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_vacaciones = None
        self.combobox_trabajadores = None

    def vacaciones_uno(self):
        global contadorun, boton_vacu
        contadorun += 1
        if contadorun >= 3:
            if boton_vacu:
                boton_vacu.config(state=tk.DISABLED)
                messagebox.showinfo("Límite Alcanzado", "El período Enero-Febrero ha alcanzado el límite de solicitudes ")

    def vacaciones_dos(self):
        global contadordo, boton_vacd
        contadordo += 1
        if contadordo >= 3:
            if boton_vacd:
                boton_vacd.config(state=tk.DISABLED)
                messagebox.showinfo("Límite Alcanzado", "El período Marzo-Abril ha alcanzado el límite de solicitudes")

    def vacaciones_tres(self):
        global contadortr, boton_vact
        contadortr += 1
        if contadortr >= 3:
            if boton_vact:
                boton_vact.config(state=tk.DISABLED)
                messagebox.showinfo("Límite Alcanzado", "El período Junio-Julio ha alcanzado el límite de solicitudes ")

    def vacaciones_cuatro(self):
        global contadorcu, boton_vacc
        contadorcu += 1
        if contadorcu >= 3:
            if boton_vacc:
                boton_vacc.config(state=tk.DISABLED)
                messagebox.showinfo("Límite Alcanzado", "El período Nov-Dic ha alcanzado el límite de solicitudes")

    def _obtener_contador_global(self, periodo):
        global contadorun, contadordo, contadortr, contadorcu
        if periodo == "Enero-Febrero":
            return contadorun
        elif periodo == "Marzo-Abril":
            return contadordo
        elif periodo == "Junio-Julio":
            return contadortr
        elif periodo == "Nov-Dic":
            return contadorcu
        return 0

    def _actualizar_estado_botones_vacaciones(self):
        indice_seleccionado = self.combobox_trabajadores.current()
        trabajador_seleccionado = None
        global nombres_para_combobox_vacaciones
        if indice_seleccionado != -1 and lista_trabajadores_registrados and \
           (nombres_para_combobox_vacaciones[0] != "No hay trabajadores registrados aún"):
            trabajador_seleccionado = lista_trabajadores_registrados[indice_seleccionado]

        periodos_orden = ["Enero-Febrero", "Marzo-Abril", "Junio-Julio", "Nov-Dic"]
        global_buttons = [boton_vacu, boton_vacd, boton_vact, boton_vacc]

        for i, periodo in enumerate(periodos_orden):
            btn = global_buttons[i]
            if btn is None:
                continue

            contador_global_actual = self._obtener_contador_global(periodo)
            limite_global_alcanzado = (contador_global_actual >= 3)

            limite_individual_alcanzado = False
            if trabajador_seleccionado:
                limite_individual_alcanzado = (trabajador_seleccionado.obtener_conteo_vacaciones_individual(periodo) >= 3)

            if not trabajador_seleccionado or limite_global_alcanzado or limite_individual_alcanzado:
                btn.config(state=tk.DISABLED)
            else:
                btn.config(state=tk.NORMAL)

    def _accion_combinada_vacacion(self, periodo, tu_funcion_original):
        indice_seleccionado = self.combobox_trabajadores.current()

        if indice_seleccionado == -1 or not lista_trabajadores_registrados or \
           nombres_para_combobox_vacaciones[0] == "No hay trabajadores registrados aún":
            messagebox.showwarning("Error", "Por favor, seleccione un trabajador primero.")
            return

        trabajador_seleccionado = lista_trabajadores_registrados[indice_seleccionado]

        contador_global_antes = self._obtener_contador_global(periodo)

        tu_funcion_original()

        if self._obtener_contador_global(periodo) >= 3 and contador_global_antes < 3:
            self._actualizar_estado_botones_vacaciones()
            return

        if trabajador_seleccionado.registrar_vacaciones_individual(periodo):
            mensaje_historial_simple = f"Vacación de {periodo} registrada para {trabajador_seleccionado.nombre}."
            historial_actividades.append(mensaje_historial_simple)
            messagebox.showinfo("Vacaciones Registradas", f"Vacaciones para '{trabajador_seleccionado.nombre}' registradas en '{periodo}'.\n")
        else:
            messagebox.showwarning("Límite Individual Alcanzado",f"'{trabajador_seleccionado.nombre}' ya ha alcanzado su límite de 3 solicitudes para el período '{periodo}'.")

        self._actualizar_estado_botones_vacaciones()

    def abrir_ventana_vacaciones(self):
        global boton_vacu, boton_vacd, boton_vact, boton_vacc
        global nombres_para_combobox_vacaciones

        self.ventana_principal.withdraw()

        self.ventana_vacaciones = tk.Toplevel(self.ventana_principal)
        self.ventana_vacaciones.title("Vacaciones Disponibles")
        self.ventana_vacaciones.geometry("400x500")

        tk.Label(self.ventana_vacaciones, text="Fechas de Vacaciones", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.ventana_vacaciones, text="Seleccione un trabajador:").pack(pady=5)
        nombres_para_combobox_vacaciones = [t.obtener_texto_para_lista() for t in lista_trabajadores_registrados]
        if not nombres_para_combobox_vacaciones:
            nombres_para_combobox_vacaciones = ["No hay trabajadores registrados aún"]

        self.combobox_trabajadores = ttk.Combobox(self.ventana_vacaciones,values=nombres_para_combobox_vacaciones,state="readonly")
        self.combobox_trabajadores.pack(pady=5)

        if nombres_para_combobox_vacaciones and nombres_para_combobox_vacaciones[0] != "No hay trabajadores registrados aún":
            self.combobox_trabajadores.current(0)

        self.combobox_trabajadores.bind("<<ComboboxSelected>>", lambda event: self._actualizar_estado_botones_vacaciones())

        tk.Label(self.ventana_vacaciones, text="Períodos de Vacaciones:", font=("Arial", 12)).pack(pady=10)

        boton_vacu = tk.Button(self.ventana_vacaciones, text="Enero-Febrero", command=lambda: self._accion_combinada_vacacion("Enero-Febrero", self.vacaciones_uno))
        boton_vacu.pack(pady=5)

        boton_vacd = tk.Button(self.ventana_vacaciones, text="Marzo-Abril", command=lambda: self._accion_combinada_vacacion("Marzo-Abril", self.vacaciones_dos))
        boton_vacd.pack(pady=5)

        boton_vact = tk.Button(self.ventana_vacaciones, text="Junio-Julio", command=lambda: self._accion_combinada_vacacion("Junio-Julio", self.vacaciones_tres))
        boton_vact.pack(pady=5)

        boton_vacc = tk.Button(self.ventana_vacaciones, text="Nov-Dic", command=lambda: self._accion_combinada_vacacion("Nov-Dic", self.vacaciones_cuatro))
        boton_vacc.pack(pady=5)

        self._actualizar_estado_botones_vacaciones()

        def volver_a_principal():
            self.ventana_vacaciones.destroy()
            self.ventana_principal.deiconify()

        tk.Button(self.ventana_vacaciones, text="Volver al Menú Principal", command=volver_a_principal).pack(pady=20)
        self.ventana_vacaciones.protocol("WM_DELETE_WINDOW", volver_a_principal)

class ManejadorAsistencia:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_asistencia = None
        self.combobox_asistencia = None
        self.label_trabajadores_listado = None

    def _actualizar_combobox_para_turno(self, turno):
        nombres_trabajadores_turno = []
        for trabajador in lista_trabajadores_registrados:
            if trabajador.horario == turno:
                nombres_trabajadores_turno.append(trabajador.obtener_texto_para_lista())

        self.combobox_asistencia['values'] = nombres_trabajadores_turno

        if nombres_trabajadores_turno:
            self.combobox_asistencia.set("Seleccione un trabajador...")
            self.combobox_asistencia.config(state="readonly")
            self.label_trabajadores_listado.config(text=f"Trabajadores en Turno {turno}:")
        else:
            self.combobox_asistencia.set("No hay trabajadores en este turno")
            self.combobox_asistencia.config(state="disabled")
            self.label_trabajadores_listado.config(text=f"No hay trabajadores en Turno {turno}")


    def abrir_ventana_asistencia(self):
        self.ventana_principal.withdraw()

        self.ventana_asistencia = tk.Toplevel(self.ventana_principal)
        self.ventana_asistencia.title("Pasar Asistencia")
        self.ventana_asistencia.geometry("450x380")

        tk.Label(self.ventana_asistencia, text="1. Seleccione el Turno:", font=("Arial", 12)).pack(pady=10)


        frame_turnos = tk.Frame(self.ventana_asistencia)
        frame_turnos.pack(pady=5)

        tk.Button(frame_turnos, text="Turno Matutino", command=lambda: self._actualizar_combobox_para_turno("Matutino")).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_turnos, text="Turno Vespertino", command=lambda: self._actualizar_combobox_para_turno("Vespertino")).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_turnos, text="Turno Nocturno", command=lambda: self._actualizar_combobox_para_turno("Nocturno")).pack(side=tk.LEFT, padx=5)

        tk.Label(self.ventana_asistencia, text="2. Seleccione un trabajador:", font=("Arial", 12)).pack(pady=10)

        self.label_trabajadores_listado = tk.Label(self.ventana_asistencia, text="Seleccione un turno primero", font=("Arial", 10))
        self.label_trabajadores_listado.pack(pady=5)
        self.combobox_asistencia = ttk.Combobox(self.ventana_asistencia, values=[], state="disabled", width=45)
        self.combobox_asistencia.set("Esperando selección de turno...") # Texto por defecto
        self.combobox_asistencia.pack(pady=5)


        def registrar_asistencia_seleccionada():
            seleccion_combobox = self.combobox_asistencia.get()
            if self.combobox_asistencia['state'] == 'disabled' or seleccion_combobox == "Esperando selección de turno..." or seleccion_combobox == "No hay trabajadores en este turno" or not seleccion_combobox:
                messagebox.showwarning("Error", "Por favor, seleccione un turno y luego un trabajador válido.")
                return

            trabajador_obj = None
            for t in lista_trabajadores_registrados:
                if t.obtener_texto_para_lista() == seleccion_combobox:
                    trabajador_obj = t
                    break

            if trabajador_obj:
                mensaje_historial_simple = f"Asistencia registrada para: {trabajador_obj.nombre} (Horario: {trabajador_obj.horario})"
                historial_actividades.append(mensaje_historial_simple)
                messagebox.showinfo("Asistencia Registrada", mensaje_historial_simple)
            else:
                messagebox.showerror("Error", "No se pudo encontrar el trabajador seleccionado.")


        tk.Button(self.ventana_asistencia, text="3. Registrar Asistencia", command=registrar_asistencia_seleccionada).pack(pady=15)

        def volver_desde_asistencia():
             self.ventana_asistencia.destroy()
             self.ventana_principal.deiconify()

        tk.Button(self.ventana_asistencia, text="Volver al Menú Principal", command=volver_desde_asistencia).pack(pady=10)

        self.ventana_asistencia.protocol("WM_DELETE_WINDOW", volver_desde_asistencia)


def agregar_trabajador_ven():
    ventana_menu.withdraw()

    ventana_menudos = tk.Toplevel(ventana_menu)
    ventana_menudos.title("Nuevo Trabajador")
    ventana_menudos.geometry("400x580")

    mensaje_registro_label = tk.Label(ventana_menudos, text="", fg="green")
    mensaje_registro_label.pack(pady=5)

    def registrar_trabajador():
        nombre = entry_nombre.get()
        edad = entry_edad.get()
        genero = entry_genero.get()
        curp = entry_curp.get()
        nss = entry_nss.get()
        horario = combo_horario.get()

        if not all([nombre, edad, genero, curp, nss, horario]):
            messagebox.showerror("Error de Registro", "Todos los campos son obligatorios.")
            return

        if horario == "Seleccione Horario":
            messagebox.showwarning("Error de Registro", "Por favor, seleccione un horario para el trabajador.")
            return

        nuevo_trabajador = Trabajador(nombre, edad, genero, curp, nss, horario)
        lista_trabajadores_registrados.append(nuevo_trabajador)

        mensaje_historial_simple = f"Nuevo trabajador registrado: {nuevo_trabajador.nombre} (NSS: {nuevo_trabajador.nss}, Horario: {nuevo_trabajador.horario})"
        historial_actividades.append(mensaje_historial_simple)

        mensaje_registro_label.config(text=mensaje_historial_simple)
        messagebox.showinfo("Registro Exitoso", mensaje_historial_simple)

        entry_nombre.delete(0, tk.END)
        entry_edad.delete(0, tk.END)
        entry_genero.delete(0, tk.END)
        entry_curp.delete(0, tk.END)
        entry_nss.delete(0, tk.END)
        combo_horario.set("Seleccione Horario")

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

    tk.Label(ventana_menudos, text="Horario:").pack(pady=2)
    opciones_horario = ["Matutino", "Vespertino", "Nocturno"]
    combo_horario = ttk.Combobox(ventana_menudos, values=opciones_horario, state="readonly")
    combo_horario.set("Seleccione Horario")
    combo_horario.pack(pady=2)

    btn_registrar = tk.Button(ventana_menudos, text="Registrar trabajador", command=registrar_trabajador)
    btn_registrar.pack(pady=15)

    def volver_menudos():
        ventana_menudos.destroy()
        ventana_menu.deiconify()

    btn_volver = tk.Button(ventana_menudos, text="Volver al Menú Principal", command=volver_menudos)
    btn_volver.pack(pady=10)

    ventana_menudos.protocol("WM_DELETE_WINDOW", volver_menudos)

def mostrar_historial_simple():
    ventana_menu.withdraw()

    ventana_historial = tk.Toplevel(ventana_menu)
    ventana_historial.title("Historial de Actividades")
    ventana_historial.geometry("500x350")

    tk.Label(ventana_historial, text="Registro de Actividades:", font=("Arial", 14)).pack(pady=10)

    historial_listbox = tk.Listbox(ventana_historial, width=60, height=12)
    historial_listbox.pack(pady=10)

    if not historial_actividades:
        historial_listbox.insert(tk.END, "No hay actividades registradas aún.")
    else:
        for actividad in historial_actividades:
            historial_listbox.insert(tk.END, actividad)

    scrollbar = tk.Scrollbar(ventana_historial, command=historial_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    historial_listbox.config(yscrollcommand=scrollbar.set)

    def volver_desde_historial():
        ventana_historial.destroy()
        ventana_menu.deiconify()

    btn_volver = tk.Button(ventana_historial, text="Volver al Menú Principal", command=volver_desde_historial)
    btn_volver.pack(pady=20)

    ventana_historial.protocol("WM_DELETE_WINDOW", volver_desde_historial)

ventana_menu = tk.Tk()
ventana_menu.title("Menú Inicial")
ventana_menu.geometry("500x350")

tk.Label(ventana_menu, text="Bienvenido, escoja qué desea realizar").pack(pady=20)

boton_opc1re = tk.Button(ventana_menu, text="Agregar nuevo trabajador", command=agregar_trabajador_ven)
boton_opc1re.pack(pady=10)

manejador_asistencia_instancia = ManejadorAsistencia(ventana_menu)
boton_asis = tk.Button(ventana_menu, text="Pasar asistencia a trabajador", command=manejador_asistencia_instancia.abrir_ventana_asistencia)
boton_asis.pack(pady=10)

manejador_vacaciones_instancia = ManejadorVacaciones(ventana_menu)

btn_vacaciones = tk.Button(ventana_menu, text="Ver Vacaciones Disponibles", command=manejador_vacaciones_instancia.abrir_ventana_vacaciones)
btn_vacaciones.pack(pady=10)

btn_ver_historial = tk.Button(ventana_menu, text="Ver Historial de Actividades", command=mostrar_historial_simple)
btn_ver_historial.pack(pady=10)

ventana_menu.mainloop()
