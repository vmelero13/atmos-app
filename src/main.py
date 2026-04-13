import sys
import time
import ui
from utils import limpiar_pantalla, imprimir_encabezado_h2
from validation import validar_zona_registro, validar_duplicado
from alerts import evaluar_alerta
import io_manager as io

def ejecutar_registro() -> None:
    """
    Orquesta el flujo completo de creación de una nueva medición meteorológica.
    
    El proceso incluye:
    1. Captura de datos vía UI.
    2. Evaluación de alertas basadas en niveles críticos.
    3. Verificación de registros duplicados (misma fecha y zona).
    4. Persistencia de datos en el almacenamiento.
    
    Returns:
        None
    """
    registro = ui.solicitar_medicion()

    if registro is None:
        return 
    
    fecha = registro["fecha_registro"] 
    zona = registro["zona_registro"]

    ui.mostrar_resumen_registro(registro)

    # Evaluación de alertas
    alertas = evaluar_alerta(registro)
    for alerta in alertas["mensajes"]:
        print(f"⚠️  ALERTA: {alerta}")
    
    opcion = ui.mostrar_confirmacion()
    while True:
        try: 
            if opcion == "1":
                # Validar registros duplicados
                datos = io.cargar_datos()
                es_unico = validar_duplicado(fecha, zona, datos)
                
                if not es_unico:
                    print(f"\n⚠️  AVISO: Ya existe una medición para la zona '{zona}' en la fecha {fecha}.")
                    print("No se ha guardado el registro para evitar datos repetidos.")
                else:
                    # 4. Guardar registro (I/O)
                    del alertas["mensajes"]
                    registro.update(alertas)

                    print("\n💾 Guardando datos...")
                    time.sleep(0.5)

                    try:
                        io.guardar_registro(registro, datos)
                        print(f"\n✅ Registro guardado correctamente.")
                        break
                    except Exception as e:
                        print(f"\n🔥 Error crítico al guardar el registro: {e}")
            elif opcion == "2":
                limpiar_pantalla()
                imprimir_encabezado_h2("NUEVO REGISTRO ATMOSFÉRICO")
                ejecutar_registro()
            elif opcion == "X":
                iniciar_aplicacion()
        except KeyboardInterrupt:
            return


def consultar_por_zona() -> None:
    """
    Gestiona el submenú de consultas filtradas por zona geográfica.
    
    Carga los datos históricos y permite realizar búsquedas sucesivas. 
    Muestra los resultados formateados en consola y permite reintentar o volver.

    Returns:
        None
    """
    while True:
        try:
            limpiar_pantalla()
            imprimir_encabezado_h2("CONSULTA DE REGISTROS POR ZONA")
            
            datos = io.cargar_datos()
            zona_busqueda = ui.solicitar_zona("Zona/Distrito a consultar: ")
            
            # Filtramos los datos (convertimos a minúsculas para comparar sin errores)
            resultados = [r for r in datos if r["zona_registro"].lower() == zona_busqueda.lower()]

            if resultados:
                print(f"\n🔍 Se han encontrado {len(resultados)} registros en la zona {zona_busqueda.upper()}:")
                print("-" * 50)
                for r in resultados:
                    print(f"📅 {r['fecha_registro']} | 🌡️  {r['temperatura']}°C | 💧 {r['humedad_nivel']}% | 💨 {r['viento_velocidad']} km/h")
            else:
                print(f"\nℹ️  No se encontraron registros para la zona {zona_busqueda.upper()}")

            # Preguntar al usuario qué desea hacer a continuación
            opcion = ui.mostrar_submenu_consultas()
            
            if opcion == "2":
                break # Sale del bucle de consulta y vuelve al menú principal
            elif opcion != "1":
                #print("\n⚠️ Opción no reconocida. Volviendo al menú principal...")
                #break
                print(f"\n⚠️  {opcion} no es una opción válida.")
                input("\nPresione Enter para intentarlo de nuevo...")
        except KeyboardInterrupt:
            print("\n\n⚠️  Operación cancelada por el usuario.")
            return 

def iniciar_aplicacion() -> None:
    """
    Punto de entrada principal que mantiene el bucle de ejecución de la App.
    
    Gestiona la navegación entre el registro de datos, las consultas y la 
    salida controlada del sistema.

    Returns:
        None
    """
    while True:
        limpiar_pantalla()
        opcion = ui.mostrar_menu_principal()

        if opcion == "1":
            limpiar_pantalla()
            imprimir_encabezado_h2("NUEVO REGISTRO ATMOSFÉRICO")
            ejecutar_registro()
            input("\nPresione Enter para continuar...")
        
        elif opcion == "2":
            consultar_por_zona()
            input("\nPresione Enter para continuar...")

        elif opcion == "X":
            ui.transicion_despedida()
            sys.exit()

        else:
            print(f"\n⚠️  {opcion} no es una opción válida.")
            input("\nPresione Enter para intentarlo de nuevo...")

if __name__ == "__main__":
    try:
        ui.transicion_bienvenida()
        iniciar_aplicacion()
    except KeyboardInterrupt:
        ui.transicion_despedida()
        sys.exit()
    except EOFError:
        pass
    except Exception as e:
        print(f"\n❌ Error crítico inesperado: {e}")