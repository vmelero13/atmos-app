from src.validation import (
    validar_fecha_registro,
    validar_zona_registro,
    validar_temperatura,
    validar_humedad_nivel,
    validar_viento_velocidad,
    validar_duplicado
)
# Registros de prueba para comprobar duplicados
registros_existentes = [
    {
        "fecha_registro": "2026-04-07",
        "zona_registro": "centro",
        "temperatura": 23.5,
        "humedad_nivel": 60,
        "viento_velocidad": 20
    },
    {
        "fecha_registro": "2026-04-07",
        "zona_registro": "norte",
        "temperatura": 19.0,
        "humedad_nivel": 55,
        "viento_velocidad": 30
    }
]
print("========== PRUEBAS DE VALIDATION.PY ==========")

print("\n--- FECHA ---")
print("2026-04-07  ->", validar_fecha_registro("2026-04-07"))   # True
print("07/04/2026  ->", validar_fecha_registro("07/04/2026"))   # False
print("2026/04/07  ->", validar_fecha_registro("2026/04/07"))   # False
print("2026-15-40  ->", validar_fecha_registro("2026-15-40"))   # False

print("\n--- ZONA ---")
print("centro      ->", validar_zona_registro("centro"))        # True
print("Centro      ->", validar_zona_registro("Centro"))        # True
print("' norte '   ->", validar_zona_registro(" norte "))       # True
print("oeste       ->", validar_zona_registro("oeste"))         # False

print("\n--- TEMPERATURA ---")
print("25          ->", validar_temperatura(25))                # True
print("-15         ->", validar_temperatura(-15))               # True
print("50          ->", validar_temperatura(50))                # True
print("-16         ->", validar_temperatura(-16))               # False
print("51          ->", validar_temperatura(51))                # False

print("\n--- HUMEDAD ---")
print("0           ->", validar_humedad_nivel(0))               # True
print("50          ->", validar_humedad_nivel(50))              # True
print("100         ->", validar_humedad_nivel(100))             # True
print("-1          ->", validar_humedad_nivel(-1))              # False
print("101         ->", validar_humedad_nivel(101))             # False

print("\n--- VIENTO ---")
print("1           ->", validar_viento_velocidad(1))            # True
print("80          ->", validar_viento_velocidad(80))           # True
print("130         ->", validar_viento_velocidad(130))          # True
print("0           ->", validar_viento_velocidad(0))            # False
print("131         ->", validar_viento_velocidad(131))          # False

print("\n--- DUPLICADOS ---")
print("2026-04-07 / centro ->", validar_duplicado("2026-04-07", "centro", registros_existentes))  # False
print("2026-04-07 / Centro ->", validar_duplicado("2026-04-07", "Centro", registros_existentes))  # False
print("2026-04-08 / sur    ->", validar_duplicado("2026-04-08", "sur", registros_existentes))     # True
