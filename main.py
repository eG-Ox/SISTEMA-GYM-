from datetime import date
from src.miproyecto.services.gestion_socios import GestionSocios
from src.miproyecto.services.gestion_membresias import GestionMembresias
from src.miproyecto.services.gestion_clases import GestionClases
from src.miproyecto.services.gestion_asistencias import GestionAsistencias
from src.miproyecto.services.reportes import GeneradorReportes
from src.miproyecto.models.instructor import Instructor
from src.miproyecto.utils.validadores import Validadores
from src.miproyecto.utils.formatters import Formateadores

# UTILIDADES GENERALES

def pausar():
    input("\nPresione ENTER para continuar...")


def pedir_input(mensaje, validador=None):
    while True:
        valor = input(mensaje).strip()
        try:
            if validador:
                validador(valor)
            return valor
        except Exception as e:
            print(e)


def seleccionar_opcion(opciones: dict):
    opcion = input("Seleccione una opción: ").strip()
    accion = opciones.get(opcion)
    if accion:
        accion()
    else:
        print("Opción inválida.")
        pausar()


# MENÚ PRINCIPAL

def menu_principal():
    socios_srv = GestionSocios()
    membresias_srv = GestionMembresias()
    clases_srv = GestionClases()
    asistencias_srv = GestionAsistencias()
    reportes_srv = GeneradorReportes(
        socios_srv.repo, asistencias_srv.repo, clases_srv.repo, membresias_srv
    )

    instructores = [
        Instructor(1, "Ana Torres", "Spinning"),
        Instructor(2, "Luis Díaz", "Zumba"),
        Instructor(3, "María Gómez", "Yoga"),
        Instructor(4, "Carlos Ruiz", "Pilates"),
        Instructor(5, "Pedro López", "Boxeo"),
        Instructor(6, "Laura Sánchez", "Baile"),
    ]

    for inst in instructores:
        clases_srv.registrar_tipo_clase(inst.especialidad)

    while True:
        print("""
=============================================
      SISTEMA DE GESTIÓN DE GIMNASIO
=============================================
1. Gestión de miembros
2. Gestión de membresías
3. Registro de asistencias
4. Gestión de clases
5. Reportes
6. Salir
=============================================
""")
        seleccionar_opcion({
            "1": lambda: menu_miembros(socios_srv),
            "2": lambda: menu_membresias(socios_srv, membresias_srv),
            "3": lambda: menu_asistencias(socios_srv, asistencias_srv),
            "4": lambda: menu_clases(socios_srv, clases_srv, instructores),
            "5": lambda: menu_reportes(reportes_srv),
            "6": exit,
        })


# MENÚ MIEMBROS

def menu_miembros(socios_srv):
    while True:
        print("""
------------- GESTIÓN DE MIEMBROS -------------
1. Registrar nuevo miembro
2. Editar datos de miembro
3. Buscar miembro por DNI
4. Listar miembros activos
5. Activar / desactivar miembro
6. Volver
----------------------------------------------
""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            socio = socios_srv.registrar(
                pedir_input("DNI: ", Validadores.validar_dni),
                pedir_input("Nombres: ", Validadores.validar_nombre),
                pedir_input("Apellidos: ", Validadores.validar_apellido),
                pedir_input("Teléfono: ", Validadores.validar_telefono),
                pedir_input("Correo: ", Validadores.validar_correo),
            )
            print(f"Miembro registrado: {socio}")
            pausar()

        elif opcion == "2":
            dni = pedir_input("DNI: ", Validadores.validar_dni)
            socio = socios_srv.buscar_por_dni(dni)
            if not socio:
                print("Miembro no encontrado.")
            else:
                socios_srv.editar(
                    dni,
                    nombres=input("Nuevos nombres: ").strip() or None,
                    apellidos=input("Nuevos apellidos: ").strip() or None,
                    telefono=input("Nuevo teléfono: ").strip() or None,
                    correo=input("Nuevo correo: ").strip() or None,
                )
                print("Datos actualizados.")
            pausar()

        elif opcion == "3":
            socio = socios_srv.buscar_por_dni(pedir_input("DNI: ", Validadores.validar_dni))
            print(socio if socio else "Miembro no encontrado.")
            pausar()

        elif opcion == "4":
            activos = socios_srv.listar_activos()
            print(Formateadores.formatear_lista_simples([str(s) for s in activos]) if activos else "Sin miembros activos.")
            pausar()

        elif opcion == "5":
            dni = pedir_input("DNI: ", Validadores.validar_dni)
            socio = socios_srv.buscar_por_dni(dni)
            if socio:
                socios_srv.activar(dni) if not socio.estado_activo else socios_srv.desactivar(dni)
                print("Estado actualizado.")
            else:
                print("Miembro no encontrado.")
            pausar()

        elif opcion == "6":
            break


# MENÚ MEMBRESÍAS

def menu_membresias(socios_srv, membresias_srv):
    while True:
        print("""
----------- GESTIÓN DE MEMBRESÍAS -----------
1. Asignar membresía
2. Renovar membresía
3. Ver estado
4. Volver
--------------------------------------------
""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "4":
            break

        dni = pedir_input("DNI: ", Validadores.validar_dni)
        socio = socios_srv.buscar_por_dni(dni)
        if not socio:
            print("Miembro no encontrado.")
            pausar()
            continue

        if opcion == "1":
            dias = {"1": 90, "2": 180, "3": 365}.get(input("1)90 2)180 3)365: "))
            if not dias:
                print("Opción inválida.")
            else:
                m = membresias_srv.crear(f"{dias} días", dias)
                socios_srv.asignar_membresia(dni, m)
                print(f"Membresía asignada hasta {m.fecha_fin}")
            pausar()

        elif opcion == "2" and socio.membresia:
            membresias_srv.renovar(socio.membresia)
            print("Membresía renovada.")
            pausar()

        elif opcion == "3":
            print(socio.membresia if socio.membresia else "Sin membresía.")
            pausar()


# MENÚ ASISTENCIAS

def menu_asistencias(socios_srv, asistencias_srv):
    while True:
        print("""
----------- REGISTRO DE ASISTENCIAS -----------
1. Registrar asistencia
2. Historial por miembro
3. Asistencias de hoy
4. Volver
----------------------------------------------
""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "4":
            break

        if opcion == "3":
            hoy = date.today()
            asistencias = asistencias_srv.asistencias_del_dia(hoy)
            print(Formateadores.formatear_lista_simples([
                f"{a.socio.nombres} {a.socio.apellidos} {a.hora}" for a in asistencias
            ]) if asistencias else "Sin asistencias hoy.")
            pausar()
            continue

        dni = pedir_input("DNI: ", Validadores.validar_dni)
        socio = socios_srv.buscar_por_dni(dni)
        if not socio:
            print("Miembro no encontrado.")
            pausar()
            continue

        if opcion == "1":
            asistencias_srv.registrar_asistencia(socio)
            print("Asistencia registrada.")
        elif opcion == "2":
            historial = asistencias_srv.historial_por_socio(socio)
            print(Formateadores.formatear_lista_simples([
                f"{a.fecha} {a.hora}" for a in historial
            ]) if historial else "Sin asistencias.")
        pausar()


# MENÚ CLASES

def menu_clases(socios_srv, clases_srv, instructores):
    while True:
        print("""
-------------- GESTIÓN DE CLASES --------------
1. Crear clase
2. Clases de hoy
3. Inscribir miembro
4. Ver inscritos
5. Volver
----------------------------------------------
""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "5":
            break

        if opcion == "1":
            tipos = clases_srv.obtener_tipos_clase()
            for i, t in enumerate(tipos, 1):
                print(f"{i}) {t}")
            tipo = tipos[int(input("Seleccione: ")) - 1]
            fecha = date.fromisoformat(input("Fecha YYYY-MM-DD: "))
            hora = input("Hora HH:MM: ")
            cupo = int(input("Cupo: "))
            instructor = next((i for i in instructores if i.especialidad == tipo), Instructor(0, "Genérico", tipo))
            clases_srv.crear(tipo, instructor, cupo, fecha, hora)
            print("Clase creada.")

        elif opcion == "2":
            clases = clases_srv.clases_de_hoy(date.today())
            print(Formateadores.formatear_lista_simples([str(c) for c in clases]) if clases else "Sin clases hoy.")

        elif opcion == "3":
            clases_srv.inscribir_socio(int(input("ID clase: ")),
                                       socios_srv.buscar_por_dni(pedir_input("DNI: ", Validadores.validar_dni)))
            print("Inscrito correctamente.")

        elif opcion == "4":
            clase = clases_srv.buscar_por_id(int(input("ID clase: ")))
            print(Formateadores.formatear_lista_simples([
                f"{s.nombres} {s.apellidos}" for s in clase.inscritos
            ]) if clase and clase.inscritos else "Sin inscritos.")
        pausar()


# MENÚ REPORTES

def menu_reportes(reportes_srv):
    while True:
        print("""
-------------- REPORTES --------------
1. Ver resumen general
2. Volver
-------------------------------------
""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "2":
            break

        if opcion == "1":
            try:
                resumen = reportes_srv.reporte_resumen()
                print("\n=== RESUMEN DEL GIMNASIO ===")
                print(f"Fecha: {resumen['fecha_consulta']}")
                print(f"Total miembros: {resumen['total_socios']}")
                print(f"  - Activos:    {resumen['socios_activos']}")
                print(f"  - Inactivos:  {resumen['socios_inactivos']}")
                print(f"Asistencias hoy: {resumen['asistencias_hoy']}")
                print(f"Clases hoy:      {resumen['clases_hoy']}")
                
                if "total_membresias" in resumen:
                    print(f"Total membresías: {resumen['total_membresias']}")
                    print(f"  - Activas:      {resumen['membresias_activas']}")
                
                print("============================")
            except Exception as e:
                print(f"Error generando reporte: {e}")
            
            pausar()


if __name__ == "__main__":
    menu_principal()