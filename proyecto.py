import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from datetime import datetime

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

global_combobox_asistencia = None
global_label_trabajadores_listado = None
global_ventana_asistencia = None
global_entry_hora_entrada = None

COLOR_FONDO_CLARO = "#F0F8FF"
COLOR_FONDO_OSCURO = "#E0FFFF"
COLOR_BOTON_PRINCIPAL = "#1E90FF"
COLOR_TEXTO_BOTON = "white"
COLOR_BOTON_ACCION = "#32CD32"
COLOR_BOTON_VOLVER = "#696969"
COLOR_TEXTO_GENERAL = "#333333"
COLOR_BORDE_ENTRADA = "#B0C4DE"

FUENTE_TITULO = ("Arial", 20, "bold")
FUENTE_SUBTITULO = ("Helvetica", 16, "bold")
FUENTE_ETIQUETA = ("Verdana", 12)
FUENTE_ENTRADA = ("Consolas", 14)
FUENTE_BOTON_GRANDE = ("Arial", 16, "bold")
FUENTE_BOTON_NORMAL = ("Arial", 12, "bold")


class Trabajador:
    def __init__(self, nombre, edad, genero, curp, nss, puesto, horario):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.curp = curp
        self.nss = nss
        self.puesto = puesto
        self.horario = horario
        self.habilitado = True
        self.vacaciones_solicitadas_individual = {"Enero-Febrero": 0,"Marzo-Abril": 0,"Junio-Julio": 0,"Nov-Dic": 0,}

    def obtener_texto_para_lista(self):
        estado = " (Inhabilitado)" if not self.habilitado else ""
        return f"{self.nombre} (NSS: {self.nss}){estado}"

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
                messagebox.showinfo("Límite Alcanzado", "El período Enero-Febrero ha alcanzado el límite de solicitudes")

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
                messagebox.showinfo("Límite Alcanzado", "El período Junio-Julio ha alcanzado el límite de solicitudes")

    def vacaciones_cuatro(self):
        global contadorcu, boton_vacc
        contadorcu += 1
        if contadorcu >= 3:
            if boton_vacc:
                boton_vacc.config(state=tk.DISABLED)
                messagebox.showinfo("Límite Alcanzado", "El período Nov-Dic ha alcanzado el límite de solicitudes ")

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

        texto_seleccionado = self.combobox_trabajadores.get()
        if texto_seleccionado and texto_seleccionado != "No hay empleados registrados aún":
            for t in lista_trabajadores_registrados:
                if t.obtener_texto_para_lista() == texto_seleccionado:
                    trabajador_seleccionado = t
                    break

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
                limite_individual_alcanzado = (
                            trabajador_seleccionado.obtener_conteo_vacaciones_individual(periodo) >= 3)

            if not trabajador_seleccionado or not trabajador_seleccionado.habilitado or limite_global_alcanzado or limite_individual_alcanzado:
                btn.config(state=tk.DISABLED)
            else:
                btn.config(state=tk.NORMAL)

    def _accion_combinada_vacacion(self, periodo, tu_funcion_original):
        seleccion_combobox_texto = self.combobox_trabajadores.get()

        if not seleccion_combobox_texto or seleccion_combobox_texto == "No hay empleados registrados aún" or \
                seleccion_combobox_texto == "Seleccione un empleado...":
            messagebox.showwarning("Error", "Por favor, seleccione un empleado primero.")
            return

        trabajador_seleccionado = None
        for t in lista_trabajadores_registrados:
            if t.obtener_texto_para_lista() == seleccion_combobox_texto:
                trabajador_seleccionado = t
                break

        if not trabajador_seleccionado:
            messagebox.showerror("Error", "No se pudo encontrar el empleado seleccionado.")
            return

        if not trabajador_seleccionado.habilitado:
            messagebox.showwarning("Inhabilitado",f"'{trabajador_seleccionado.nombre}' está inhabilitado y no puede solicitar vacaciones.")
            return

        contador_global_antes = self._obtener_contador_global(periodo)

        tu_funcion_original()

        if self._obtener_contador_global(periodo) >= 3 and contador_global_antes < 3:
            self._actualizar_estado_botones_vacaciones()
            return

        if trabajador_seleccionado.registrar_vacaciones_individual(periodo):
            mensaje_historial_simple = f"Vacación de {periodo} registrada para {trabajador_seleccionado.nombre}."
            historial_actividades.append(mensaje_historial_simple)
            messagebox.showinfo("Vacaciones Registradas",f"Vacaciones para '{trabajador_seleccionado.nombre}' registradas en '{periodo}'.\n"f"Este empleado lleva {trabajador_seleccionado.obtener_conteo_vacaciones_individual(periodo)} solicitudes \n")
        else:
            messagebox.showwarning("Límite Individual Alcanzado",f"'{trabajador_seleccionado.nombre}' ya ha alcanzado su límite de 3 solicitudes para el período '{periodo}'.")

        self._actualizar_estado_botones_vacaciones()

    def abrir_ventana_vacaciones(self):
        global boton_vacu, boton_vacd, boton_vact, boton_vacc
        global nombres_para_combobox_vacaciones

        self.ventana_principal.withdraw()

        self.ventana_vacaciones = tk.Toplevel(self.ventana_principal)
        self.ventana_vacaciones.title("Gestión de Vacaciones - Hospital XYZ")
        self.ventana_vacaciones.state('zoomed')
        self.ventana_vacaciones.configure(bg=COLOR_FONDO_CLARO)

        tk.Label(self.ventana_vacaciones, text="Fechas de Vacaciones Disponibles", font=FUENTE_TITULO, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack(pady=20)

        tk.Label(self.ventana_vacaciones, text="Seleccione un Empleado:", font=FUENTE_SUBTITULO, bg=COLOR_FONDO_CLARO,fg=COLOR_TEXTO_GENERAL).pack(pady=10)

        nombres_para_combobox_vacaciones = [t.obtener_texto_para_lista() for t in lista_trabajadores_registrados]
        if not nombres_para_combobox_vacaciones:
            nombres_para_combobox_vacaciones = ["No hay empleados registrados aún"]

        self.combobox_trabajadores = ttk.Combobox(self.ventana_vacaciones, values=nombres_para_combobox_vacaciones,state="readonly", font=FUENTE_ETIQUETA, width=40)
        self.combobox_trabajadores.pack(pady=10, ipadx=5, ipady=5)

        if nombres_para_combobox_vacaciones and nombres_para_combobox_vacaciones[
            0] != "No hay empleados registrados aún":
            self.combobox_trabajadores.current(0)
        else:
            self.combobox_trabajadores.set("No hay empleados registrados aún")
            self.combobox_trabajadores.config(state="disabled")

        self.combobox_trabajadores.bind("<<ComboboxSelected>>", lambda event: self._actualizar_estado_botones_vacaciones())

        tk.Label(self.ventana_vacaciones, text="Períodos de Solicitud de Vacaciones:", font=FUENTE_SUBTITULO, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack(pady=15)

        global boton_vacu, boton_vacd, boton_vact, boton_vacc
        boton_vacu = tk.Button(self.ventana_vacaciones, text="Enero - Febrero",command=lambda: self._accion_combinada_vacacion("Enero-Febrero", self.vacaciones_uno),font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_ACCION, fg=COLOR_TEXTO_BOTON, width=25,height=1, relief="raised", bd=3)
        boton_vacu.pack(pady=7)

        boton_vacd = tk.Button(self.ventana_vacaciones, text="Marzo - Abril",command=lambda: self._accion_combinada_vacacion("Marzo-Abril", self.vacaciones_dos), font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_ACCION, fg=COLOR_TEXTO_BOTON, width=25, height=1, relief="raised", bd=3)
        boton_vacd.pack(pady=7)

        boton_vact = tk.Button(self.ventana_vacaciones, text="Junio - Julio",command=lambda: self._accion_combinada_vacacion("Junio-Julio", self.vacaciones_tres),font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_ACCION, fg=COLOR_TEXTO_BOTON, width=25,height=1, relief="raised", bd=3)
        boton_vact.pack(pady=7)

        boton_vacc = tk.Button(self.ventana_vacaciones, text="Noviembre - Diciembre",command=lambda: self._accion_combinada_vacacion("Nov-Dic", self.vacaciones_cuatro),font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_ACCION, fg=COLOR_TEXTO_BOTON, width=25,height=1, relief="raised", bd=3)
        boton_vacc.pack(pady=7)

        self._actualizar_estado_botones_vacaciones()

        def volver_a_principal():
            self.ventana_vacaciones.destroy()
            self.ventana_principal.deiconify()

        tk.Button(self.ventana_vacaciones, text="Volver al Menú Principal", command=volver_a_principal, font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_VOLVER, fg=COLOR_TEXTO_BOTON, width=20, height=1,relief="raised", bd=3).pack(pady=25)
        self.ventana_vacaciones.protocol("WM_DELETE_WINDOW", volver_a_principal)


def actualizar_combobox_para_turno(turno_seleccionado):
    global global_combobox_asistencia, global_label_trabajadores_listado

    nombres_trabajadores_turno = []
    for trabajador in lista_trabajadores_registrados:
        if trabajador.horario == turno_seleccionado and trabajador.habilitado:
            nombres_trabajadores_turno.append(trabajador.obtener_texto_para_lista())

    global_combobox_asistencia['values'] = nombres_trabajadores_turno

    if nombres_trabajadores_turno:
        global_combobox_asistencia.set("Seleccione un empleado...")
        global_combobox_asistencia.config(state="readonly")
        global_label_trabajadores_listado.config(text=f"Empleados en Turno {turno_seleccionado}:")
    else:
        global_combobox_asistencia.set("No hay empleados habilitados en este turno")
        global_combobox_asistencia.config(state="disabled")
        global_label_trabajadores_listado.config(text=f"No hay empleados habilitados en Turno {turno_seleccionado}")


def registrar_asistencia_seleccionada():
    global global_combobox_asistencia, global_entry_hora_entrada
    seleccion_combobox_texto = global_combobox_asistencia.get()

    if global_combobox_asistencia['state'] == 'disabled' or \
            seleccion_combobox_texto in ["Esperando selección de turno...","No hay empleados habilitados en este turno", "Seleccione un empleado..."] or \
            not seleccion_combobox_texto:
        messagebox.showwarning("Error de Asistencia", "Por favor, seleccione un turno y luego un empleado válido.")
        return

    hora_entrada_str = global_entry_hora_entrada.get()
    if not hora_entrada_str:
        messagebox.showwarning("Error de Entrada", "Por favor, ingrese la hora de entrada (ej. HH:MM).")
        return

    try:
        hora_ingresada = datetime.strptime(hora_entrada_str, "%H:%M").time()
    except ValueError:
        messagebox.showwarning("Error de Formato", "Formato de hora incorrecto. Use HH:MM (ej. 08:00, 15:30).")
        return

    trabajador_obj = None
    for t in lista_trabajadores_registrados:
        if t.obtener_texto_para_lista() == seleccion_combobox_texto:
            trabajador_obj = t
            break

    if trabajador_obj:
        if not trabajador_obj.habilitado:
            messagebox.showwarning("Inhabilitado",f"'{trabajador_obj.nombre}' está inhabilitado y no puede registrar asistencia.")
            return

        tipo_asistencia = "Desconocido"
        hora_limite_normal = None
        hora_limite_retardo_menor = None
        hora_limite_retardo_mayor = None

        if trabajador_obj.horario == "Matutino":
            hora_limite_normal = datetime.strptime("07:00", "%H:%M").time()
            hora_limite_retardo_menor = datetime.strptime("07:10", "%H:%M").time()
            hora_limite_retardo_mayor = datetime.strptime("07:30", "%H:%M").time()
        elif trabajador_obj.horario == "Vespertino":
            hora_limite_normal = datetime.strptime("14:00", "%H:%M").time()
            hora_limite_retardo_menor = datetime.strptime("14:10", "%H:%M").time()
            hora_limite_retardo_mayor = datetime.strptime("14:30", "%H:%M").time()
        elif trabajador_obj.horario == "Nocturno":
            hora_limite_normal = datetime.strptime("20:00", "%H:%M").time()
            hora_limite_retardo_menor = datetime.strptime("20:10", "%H:%M").time()
            hora_limite_retardo_mayor = datetime.strptime("20:30", "%H:%M").time()

        if hora_limite_normal and hora_limite_retardo_menor and hora_limite_retardo_mayor:
            if hora_ingresada <= hora_limite_normal:
                tipo_asistencia = "Asistencia Normal"
            elif hora_ingresada <= hora_limite_retardo_menor:
                tipo_asistencia = "Retardo menor"
            elif hora_ingresada <= hora_limite_retardo_mayor:
                tipo_asistencia = "Retardo mayor"
            else:
                tipo_asistencia = "Falta"
        else:
            tipo_asistencia = "Horario no definido para reglas de asistencia"

        mensaje_historial_completo = (
            f"Asistencia registrada para: {trabajador_obj.nombre}\n"
            f"Horario: {trabajador_obj.horario}\n"
            f"Hora de Entrada: {hora_ingresada.strftime('%H:%M')}\n"
            f"Estado: {tipo_asistencia}"
        )
        historial_actividades.append(mensaje_historial_completo)
        messagebox.showinfo("Asistencia Registrada", mensaje_historial_completo)
    else:
        messagebox.showerror("Error", "No se pudo encontrar el empleado seleccionado.")


def volver_desde_asistencia():
    global global_ventana_asistencia
    global_ventana_asistencia.destroy()
    ventana_menu.deiconify()


def pasar_asistencia_sencilla():
    global global_ventana_asistencia, global_combobox_asistencia, global_label_trabajadores_listado, global_entry_hora_entrada

    ventana_menu.withdraw()

    global_ventana_asistencia = tk.Toplevel(ventana_menu)
    global_ventana_asistencia.title("Registro de Asistencia - Hospital XYZ")
    global_ventana_asistencia.state('zoomed')
    global_ventana_asistencia.configure(bg=COLOR_FONDO_CLARO)

    tk.Label(global_ventana_asistencia, text="Registro de Asistencia de Personal", font=FUENTE_TITULO, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack(pady=20)

    tk.Label(global_ventana_asistencia, text="1. Seleccione el Turno:", font=FUENTE_SUBTITULO, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack(pady=15)

    frame_turnos = tk.Frame(global_ventana_asistencia, bg=COLOR_FONDO_CLARO)
    frame_turnos.pack(pady=10)

    tk.Button(frame_turnos, text="Turno Matutino", command=lambda: actualizar_combobox_para_turno("Matutino"), font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_PRINCIPAL, fg=COLOR_TEXTO_BOTON, padx=10, pady=5,relief="raised", bd=3).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_turnos, text="Turno Vespertino", command=lambda: actualizar_combobox_para_turno("Vespertino"), font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_PRINCIPAL, fg=COLOR_TEXTO_BOTON, padx=10, pady=5,relief="raised", bd=3).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_turnos, text="Turno Nocturno", command=lambda: actualizar_combobox_para_turno("Nocturno"), font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_PRINCIPAL, fg=COLOR_TEXTO_BOTON, padx=10, pady=5, relief="raised", bd=3).pack(side=tk.LEFT, padx=5)

    tk.Label(global_ventana_asistencia, text="2. Seleccione un Empleado:", font=FUENTE_SUBTITULO, bg=COLOR_FONDO_CLARO,fg=COLOR_TEXTO_GENERAL).pack(pady=15)

    global_label_trabajadores_listado = tk.Label(global_ventana_asistencia, text="Seleccione un turno primero",font=FUENTE_ETIQUETA, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL)
    global_label_trabajadores_listado.pack(pady=10)

    global_combobox_asistencia = ttk.Combobox(global_ventana_asistencia, values=[], state="disabled", width=40,font=FUENTE_ETIQUETA)
    global_combobox_asistencia.set("Esperando selección de turno...")
    global_combobox_asistencia.pack(pady=10, ipadx=5, ipady=5)

    tk.Label(global_ventana_asistencia, text="3. Ingrese la Hora de Entrada (HH:MM):", font=FUENTE_SUBTITULO,bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack(pady=15)
    global_entry_hora_entrada = tk.Entry(global_ventana_asistencia, width=15, justify='center', font=FUENTE_ENTRADA,relief="groove", bd=3, highlightbackground=COLOR_BORDE_ENTRADA,highlightthickness=2)
    global_entry_hora_entrada.pack(pady=10)
    global_entry_hora_entrada.insert(0, datetime.now().strftime("%H:%M"))

    tk.Button(global_ventana_asistencia, text="4. Registrar Asistencia", command=registrar_asistencia_seleccionada,font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_ACCION, fg=COLOR_TEXTO_BOTON, width=25, height=1, relief="raised", bd=4).pack(pady=25)

    tk.Button(global_ventana_asistencia, text="Volver al Menú Principal", command=volver_desde_asistencia,font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_VOLVER, fg=COLOR_TEXTO_BOTON, width=20, height=1,relief="raised", bd=3).pack(pady=15)

    global_ventana_asistencia.protocol("WM_DELETE_WINDOW", volver_desde_asistencia)


def agregar_trabajador_ven():
    ventana_menu.withdraw()

    ventana_menudos = tk.Toplevel(ventana_menu)
    ventana_menudos.title("Registro de Nuevo Empleado - Hospital XYZ")
    ventana_menudos.state('zoomed')
    ventana_menudos.configure(bg=COLOR_FONDO_CLARO)

    tk.Label(ventana_menudos, text="Registro de Nuevo Empleado", font=FUENTE_TITULO, bg=COLOR_FONDO_CLARO,fg=COLOR_TEXTO_GENERAL).pack(pady=5)

    mensaje_registro_label = tk.Label(ventana_menudos, text="", fg=COLOR_BOTON_ACCION, bg=COLOR_FONDO_CLARO,font=FUENTE_ETIQUETA)
    mensaje_registro_label.pack(pady=5)

    def registrar_trabajador():
        nombre = entry_nombre.get()
        edad_str = entry_edad.get()
        genero2 = combo_genero.get()
        curp = entry_curp.get()
        nss = entry_nss.get()
        puesto = combo_puesto.get()
        horario = combo_horario.get()

        if not all([nombre, edad_str, genero2, curp, nss, puesto, horario]):
            messagebox.showerror("Error de Registro", "Todos los campos son obligatorios.")
            return

        if horario == "Seleccione Horario":
            messagebox.showwarning("Error de Registro", "Por favor, seleccione un horario para el empleado.")
            return

        if puesto == "Seleccione el puesto":
            messagebox.showwarning("Error de Registro", "Por favor, seleccione un puesto para el empleado.")
            return

        if genero2 == "Seleccione el genero":
            messagebox.showwarning("Error de Registro", "Por favor, seleccione un género para el empleado.")
            return

        try:
            edad = int(edad_str)
            if not (18 <= edad <= 65):
                messagebox.showwarning("Edad Inválida", "La edad debe estar entre 18 y 65 años.")
                return
        except ValueError:
            messagebox.showwarning("Edad Inválida", "Por favor, ingrese una edad válida (número entero).")
            return

        nuevo_trabajador = Trabajador(nombre, edad_str, genero2, curp, nss, puesto, horario)
        lista_trabajadores_registrados.append(nuevo_trabajador)

        mensaje_historial_simple = f"Nuevo empleado registrado: {nuevo_trabajador.nombre} (NSS: {nuevo_trabajador.nss}, Horario: {nuevo_trabajador.horario})"
        historial_actividades.append(mensaje_historial_simple)

        mensaje_registro_label.config(text=mensaje_historial_simple)
        messagebox.showinfo("Registro Exitoso", mensaje_historial_simple)

        entry_nombre.delete(0, tk.END)
        entry_edad.delete(0, tk.END)
        entry_curp.delete(0, tk.END)
        entry_nss.delete(0, tk.END)
        combo_genero.set("Seleccione el genero")
        combo_puesto.set("Seleccione el puesto")
        combo_horario.set("Seleccione Horario")

    labels_entries_info = [("Nombre:", "entry_nombre"),("Edad:", "entry_edad"),("CURP:", "entry_curp"),("NSS:", "entry_nss"),]

    for text, entry_name in labels_entries_info:
        tk.Label(ventana_menudos, text=text, font=FUENTE_ETIQUETA, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack( pady=5)
        entry_widget = tk.Entry(ventana_menudos, font=FUENTE_ENTRADA, width=40, relief="groove", bd=3, highlightbackground=COLOR_BORDE_ENTRADA, highlightthickness=2)
        setattr(ventana_menudos, entry_name, entry_widget)
        entry_widget.pack(pady=5, ipadx=8, ipady=5)

    entry_nombre = getattr(ventana_menudos, "entry_nombre")
    entry_edad = getattr(ventana_menudos, "entry_edad")
    entry_curp = getattr(ventana_menudos, "entry_curp")
    entry_nss = getattr(ventana_menudos, "entry_nss")

    tk.Label(ventana_menudos, text="genero", font=FUENTE_ETIQUETA, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack(pady=5)
    opciones_genero = ["Masculino", "femenino", "prefiero no decirlo"]
    combo_genero = ttk.Combobox(ventana_menudos, values=opciones_genero, state="readonly", font=FUENTE_ETIQUETA, width=37)
    combo_genero.set("Seleccione el genero")
    combo_genero.pack(pady=5, ipadx=8, ipady=5)

    tk.Label(ventana_menudos, text="puesto", font=FUENTE_ETIQUETA, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack( pady=5)
    opciones_puesto = ["Basificado", "Homologado", "Regularizado", "Contrato"]
    combo_puesto = ttk.Combobox(ventana_menudos, values=opciones_puesto, state="readonly", font=FUENTE_ETIQUETA, width=37)
    combo_puesto.set("Seleccione el puesto")
    combo_puesto.pack(pady=5, ipadx=8, ipady=5)

    tk.Label(ventana_menudos, text="Horario de Trabajo:", font=FUENTE_ETIQUETA, bg=COLOR_FONDO_CLARO,fg=COLOR_TEXTO_GENERAL).pack(pady=5)
    opciones_horario = ["Matutino", "Vespertino", "Nocturno"]
    combo_horario = ttk.Combobox(ventana_menudos, values=opciones_horario, state="readonly", font=FUENTE_ETIQUETA, width=37)
    combo_horario.set("Seleccione Horario")
    combo_horario.pack(pady=5, ipadx=8, ipady=5)

    frame_botones_registro = tk.Frame(ventana_menudos, bg=COLOR_FONDO_CLARO)
    frame_botones_registro.pack(pady=30)

    btn_registrar = tk.Button(frame_botones_registro, text="Registrar Empleado", command=registrar_trabajador, font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_ACCION, fg=COLOR_TEXTO_BOTON, width=25, height=1,relief="raised", bd=4)
    btn_registrar.pack(side=tk.LEFT, padx=10)

    def volver_menudos():
        ventana_menudos.destroy()
        ventana_menu.deiconify()

    btn_volver = tk.Button(frame_botones_registro, text="Volver al Menú", command=volver_menudos,font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_VOLVER, fg=COLOR_TEXTO_BOTON, width=20, height=1, relief="raised", bd=3)
    btn_volver.pack(side=tk.LEFT, padx=10)

    ventana_menudos.protocol("WM_DELETE_WINDOW", volver_menudos)

def mostrar_historial_simple():
    ventana_menu.withdraw()

    ventana_historial = tk.Toplevel(ventana_menu)
    ventana_historial.title("Historial de Actividades - Hospital XYZ")
    ventana_historial.state('zoomed')
    ventana_historial.configure(bg=COLOR_FONDO_CLARO)

    tk.Label(ventana_historial, text="Registro de Actividades del Hospital", font=FUENTE_TITULO, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack(pady=20)

    historial_listbox = tk.Listbox(ventana_historial, width=70, height=15, font=FUENTE_ETIQUETA, bg="white",fg=COLOR_TEXTO_GENERAL, selectbackground=COLOR_BOTON_PRINCIPAL,selectforeground="white", relief="sunken", bd=3)
    historial_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    if not historial_actividades:
        historial_listbox.insert(tk.END, "No hay actividades registradas aún.")
    else:
        for actividad in historial_actividades:
            historial_listbox.insert(tk.END, actividad)

    scrollbar = ttk.Scrollbar(ventana_historial, command=historial_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    historial_listbox.config(yscrollcommand=scrollbar.set)

    def volver_desde_historial():
        ventana_historial.destroy()
        ventana_menu.deiconify()

    btn_volver = tk.Button(ventana_historial, text="Volver al Menú Principal", command=volver_desde_historial,font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_VOLVER, fg=COLOR_TEXTO_BOTON, width=20, height=1,relief="raised", bd=3)
    btn_volver.pack(pady=25)

    ventana_historial.protocol("WM_DELETE_WINDOW", volver_desde_historial)



def abrir_ventana_eliminar_suplente():
    ventana_menu.withdraw()

    ventana_gestion_empleados = tk.Toplevel(ventana_menu)
    ventana_gestion_empleados.title("Gestión de Empleados - Hospital XYZ")
    ventana_gestion_empleados.state('zoomed')
    ventana_gestion_empleados.configure(bg=COLOR_FONDO_CLARO)

    tk.Label(ventana_gestion_empleados, text="Eliminar o Asignar Suplente", font=FUENTE_TITULO, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack(pady=20)

    tk.Label(ventana_gestion_empleados, text="Seleccione un Empleado:", font=FUENTE_SUBTITULO, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack(pady=10)

    def actualizar_lista_empleados_gestion():
        nombres_empleados = [t.obtener_texto_para_lista() for t in lista_trabajadores_registrados]
        if not nombres_empleados:
            nombres_empleados = ["No hay empleados registrados aún"]
            combobox_empleados.config(state="disabled")
        else:
            combobox_empleados.config(state="readonly")
        combobox_empleados['values'] = nombres_empleados
        if nombres_empleados and nombres_empleados[0] != "No hay empleados registrados aún":
            combobox_empleados.current(0)
        else:
            combobox_empleados.set(nombres_empleados[0])

    combobox_empleados = ttk.Combobox(ventana_gestion_empleados, values=[],state="readonly", font=FUENTE_ETIQUETA, width=40)
    combobox_empleados.pack(pady=10, ipadx=5, ipady=5)
    actualizar_lista_empleados_gestion()

    def eliminar_trabajador():
        seleccion_combobox_texto = combobox_empleados.get()
        if not seleccion_combobox_texto or seleccion_combobox_texto == "No hay empleados registrados aún":
            messagebox.showwarning("Error", "Por favor, seleccione un empleado para eliminar.")
            return

        trabajador_a_eliminar = None
        for t in lista_trabajadores_registrados:
            if t.obtener_texto_para_lista() == seleccion_combobox_texto:
                trabajador_a_eliminar = t
                break

        if trabajador_a_eliminar:
            confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar a '{trabajador_a_eliminar.nombre}' del sistema?\nEsta acción es irreversible.")
            if confirmar:
                lista_trabajadores_registrados.remove(trabajador_a_eliminar)
                historial_actividades.append(f"Empleado '{trabajador_a_eliminar.nombre}' ELIMINADO del sistema.")
                messagebox.showinfo("Eliminado", f"'{trabajador_a_eliminar.nombre}' ha sido eliminado correctamente.")
                actualizar_lista_empleados_gestion()
            else:
                messagebox.showinfo("Cancelado", "La eliminación ha sido cancelada.")
        else:
            messagebox.showerror("Error", "No se pudo encontrar el empleado seleccionado.")

    def asignar_suplente_a_trabajador():
        seleccion_combobox_texto = combobox_empleados.get()
        if not seleccion_combobox_texto or seleccion_combobox_texto == "No hay empleados registrados aún":
            messagebox.showwarning("Error", "Por favor, seleccione un empleado para asignarle suplente.")
            return

        trabajador_a_inhabilitar = None
        for t in lista_trabajadores_registrados:
            if t.obtener_texto_para_lista() == seleccion_combobox_texto:
                trabajador_a_inhabilitar = t
                break

        if trabajador_a_inhabilitar:
            if trabajador_a_inhabilitar.habilitado:
                confirmar = messagebox.askyesno("Asignar Suplente",f"¿Desea asignar un suplente a '{trabajador_a_inhabilitar.nombre}'? Esto lo inhabilitará para asistencia y vacaciones.")
                if confirmar:
                    trabajador_a_inhabilitar.habilitado = False
                    historial_actividades.append(
                        f"Suplente asignado a '{trabajador_a_inhabilitar.nombre}'. Empleado INHABILITADO.")
                    messagebox.showinfo("Suplente Asignado", f"'{trabajador_a_inhabilitar.nombre}' ha sido inhabilitado (suplente asignado).")
                    actualizar_lista_empleados_gestion()
                else:
                    messagebox.showinfo("Cancelado", "Asignación de suplente cancelada.")
            else:
                messagebox.showwarning("Ya Inhabilitado", f"'{trabajador_a_inhabilitar.nombre}' ya está inhabilitado.")
        else:
            messagebox.showerror("Error", "No se pudo encontrar el empleado seleccionado.")

    frame_acciones = tk.Frame(ventana_gestion_empleados, bg=COLOR_FONDO_CLARO)
    frame_acciones.pack(pady=20)

    tk.Button(frame_acciones, text="Eliminar Empleado", command=eliminar_trabajador,font=FUENTE_BOTON_NORMAL, bg="red", fg=COLOR_TEXTO_BOTON,width=25, height=1, relief="raised", bd=3).pack(side=tk.LEFT, padx=10)

    tk.Button(frame_acciones, text="Asignar Suplente (Inhabilitar)", command=asignar_suplente_a_trabajador, font=FUENTE_BOTON_NORMAL, bg="orange", fg=COLOR_TEXTO_BOTON, width=25, height=1, relief="raised", bd=3).pack(side=tk.RIGHT, padx=10)

    def volver_desde_gestion():
        ventana_gestion_empleados.destroy()
        ventana_menu.deiconify()

    tk.Button(ventana_gestion_empleados, text="Volver al Menú Principal", command=volver_desde_gestion, font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_VOLVER, fg=COLOR_TEXTO_BOTON, width=20, height=1, relief="raised", bd=3).pack(pady=25)

    ventana_gestion_empleados.protocol("WM_DELETE_WINDOW", volver_desde_gestion)



def abrir_ventana_habilitar_trabajador():
    ventana_menu.withdraw()

    ventana_habilitar_empleado = tk.Toplevel(ventana_menu)
    ventana_habilitar_empleado.title("Habilitar Empleado - Hospital XYZ")
    ventana_habilitar_empleado.state('zoomed')
    ventana_habilitar_empleado.configure(bg=COLOR_FONDO_CLARO)

    tk.Label(ventana_habilitar_empleado, text="Habilitar Empleado (Sin Suplente)",
             font=FUENTE_TITULO, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack(pady=20)

    tk.Label(ventana_habilitar_empleado, text="Seleccione un Empleado Inhabilitado:",
             font=FUENTE_SUBTITULO, bg=COLOR_FONDO_CLARO, fg=COLOR_TEXTO_GENERAL).pack(pady=10)

    def actualizar_lista_empleados_inhabilitados():
        nombres_inhabilitados = [t.obtener_texto_para_lista() for t in lista_trabajadores_registrados if
                                 not t.habilitado]
        if not nombres_inhabilitados:
            nombres_inhabilitados = ["No hay empleados inhabilitados"]
            combobox_inhabilitados.config(state="disabled")
        else:
            combobox_inhabilitados.config(state="readonly")
        combobox_inhabilitados['values'] = nombres_inhabilitados
        if nombres_inhabilitados and nombres_inhabilitados[0] != "No hay empleados inhabilitados":
            combobox_inhabilitados.current(0)
        else:
            combobox_inhabilitados.set(nombres_inhabilitados[0])

    combobox_inhabilitados = ttk.Combobox(ventana_habilitar_empleado, values=[],
                                          state="readonly", font=FUENTE_ETIQUETA, width=40)
    combobox_inhabilitados.pack(pady=10, ipadx=5, ipady=5)
    actualizar_lista_empleados_inhabilitados()

    def habilitar_trabajador_seleccionado():
        seleccion_combobox_texto = combobox_inhabilitados.get()
        if not seleccion_combobox_texto or seleccion_combobox_texto == "No hay empleados inhabilitados":
            messagebox.showwarning("Error", "Por favor, seleccione un empleado para habilitar.")
            return

        trabajador_a_habilitar = None
        for t in lista_trabajadores_registrados:
            if t.obtener_texto_para_lista() == seleccion_combobox_texto:
                trabajador_a_habilitar = t
                break

        if trabajador_a_habilitar:
            if not trabajador_a_habilitar.habilitado:
                confirmar = messagebox.askyesno("Confirmar Habilitación",
                                                f"¿Está seguro de habilitar a '{trabajador_a_habilitar.nombre}' (quitar suplente)?")
                if confirmar:
                    trabajador_a_habilitar.habilitado = True
                    historial_actividades.append(
                        f"Empleado '{trabajador_a_habilitar.nombre}' HABILITADO. Suplente retirado.")
                    messagebox.showinfo("Habilitado", f"'{trabajador_a_habilitar.nombre}' ha sido habilitado de nuevo.")
                    actualizar_lista_empleados_inhabilitados()
                else:
                    messagebox.showinfo("Cancelado", "Habilitación cancelada.")
            else:
                messagebox.showwarning("Ya Habilitado", f"'{trabajador_a_habilitar.nombre}' ya está habilitado.")
        else:
            messagebox.showerror("Error", "No se pudo encontrar el empleado seleccionado.")

    tk.Button(ventana_habilitar_empleado, text="Habilitar Empleado", command=habilitar_trabajador_seleccionado,
              font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_ACCION, fg=COLOR_TEXTO_BOTON,
              width=25, height=1, relief="raised", bd=4).pack(pady=25)

    def volver_desde_habilitar():
        ventana_habilitar_empleado.destroy()
        ventana_menu.deiconify()

    tk.Button(ventana_habilitar_empleado, text="Volver al Menú Principal", command=volver_desde_habilitar,
              font=FUENTE_BOTON_NORMAL, bg=COLOR_BOTON_VOLVER, fg=COLOR_TEXTO_BOTON,
              width=20, height=1, relief="raised", bd=3).pack(pady=15)

    ventana_habilitar_empleado.protocol("WM_DELETE_WINDOW", volver_desde_habilitar)


ventana_menu = tk.Tk()
ventana_menu.title("Sistema de Gestión de Personal Hospitalario")
ventana_menu.state('zoomed')
ventana_menu.configure(bg=COLOR_FONDO_OSCURO)

tk.Label(ventana_menu, text="Bienvenido al Sistema de Gestión del Hospital",font=FUENTE_TITULO, fg=COLOR_TEXTO_GENERAL, bg=COLOR_FONDO_OSCURO).pack(pady=40)

boton_opc1re = tk.Button(ventana_menu, text="Registrar Nuevo Empleado", command=agregar_trabajador_ven, font=FUENTE_BOTON_GRANDE, bg=COLOR_BOTON_PRINCIPAL, fg=COLOR_TEXTO_BOTON,width=35, height=2, relief="raised", bd=5)
boton_opc1re.pack(pady=15)

boton_asis = tk.Button(ventana_menu, text="Registrar Asistencia de Personal", command=pasar_asistencia_sencilla,font=FUENTE_BOTON_GRANDE, bg=COLOR_BOTON_PRINCIPAL, fg=COLOR_TEXTO_BOTON, width=35, height=2, relief="raised", bd=5)
boton_asis.pack(pady=15)

manejador_vacaciones_instancia = ManejadorVacaciones(ventana_menu)
btn_vacaciones = tk.Button(ventana_menu, text="Gestionar Vacaciones del Personal",command=manejador_vacaciones_instancia.abrir_ventana_vacaciones,font=FUENTE_BOTON_GRANDE, bg=COLOR_BOTON_PRINCIPAL, fg=COLOR_TEXTO_BOTON, width=35, height=2, relief="raised", bd=5)
btn_vacaciones.pack(pady=15)


btn_gestionar_empleados = tk.Button(ventana_menu, text="Eliminar / Asignar Suplente",command=abrir_ventana_eliminar_suplente, font=FUENTE_BOTON_GRANDE, bg="red", fg=COLOR_TEXTO_BOTON,
                                    width=35, height=2, relief="raised", bd=5)
btn_gestionar_empleados.pack(pady=15)

btn_habilitar_empleado = tk.Button(ventana_menu, text="Habilitar Empleado", command=abrir_ventana_habilitar_trabajador,font=FUENTE_BOTON_GRANDE, bg="green", fg=COLOR_TEXTO_BOTON, width=35, height=2, relief="raised", bd=5)
btn_habilitar_empleado.pack(pady=15)

btn_ver_historial = tk.Button(ventana_menu, text="Ver Historial de Actividades", command=mostrar_historial_simple,font=FUENTE_BOTON_GRANDE, bg=COLOR_BOTON_PRINCIPAL, fg=COLOR_TEXTO_BOTON,width=35, height=2, relief="raised", bd=5)
btn_ver_historial.pack(pady=15)

ventana_menu.mainloop()
