import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "Fi6ak3qo646FAjs9MnA41zTe3Oyk5Hxt"  # <-- Reemplaza con tu key de MapQuest

# Diccionario de modos de transporte soportados por MapQuest (valor técnico para la API)
modos_transporte = {
    "1": "fastest",     # Auto - ruta más rápida
    "2": "shortest",    # Auto - ruta más corta
    "3": "pedestrian",  # A pie
    "4": "bicycle"      # Bicicleta
}

# Nombres en español para mostrar en pantalla
nombres_transporte = {
    "fastest": "Auto (ruta más rápida)",
    "shortest": "Auto (ruta más corta)",
    "pedestrian": "A pie",
    "bicycle": "Bicicleta"
}

while True:
    orig = input("\nCiudad de Origen (o 's' para salir): ")
    if orig.lower() == "s":
        break

    dest = input("Ciudad de Destino: ")
    if dest.lower() == "s":
        break

    print("\nSeleccione el medio de transporte:")
    print("1. Auto (ruta más rápida)")
    print("2. Auto (ruta más corta)")
    print("3. A pie")
    print("4. Bicicleta")
    opcion = input("Opción: ")

    tipo_ruta = modos_transporte.get(opcion, "fastest")
    nombre_tipo_ruta = nombres_transporte.get(tipo_ruta, "Auto (ruta más rápida)")

    url = main_api + urllib.parse.urlencode({
        "key": key,
        "from": orig,
        "to": dest,
        "routeType": tipo_ruta,
        "locale": "es_ES"   # <-- Fuerza la narrativa en español
    })

    json_data = requests.get(url).json()

    # Verificación defensiva por si la respuesta no trae "info"
    if "info" not in json_data:
        print("Error inesperado en la respuesta de la API:")
        print(json_data)
        continue

    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        distancia_millas = json_data["route"]["distance"]
        distancia_km = distancia_millas * 1.60934

        tiempo_segundos = json_data["route"]["time"]
        horas = tiempo_segundos // 3600
        minutos = (tiempo_segundos % 3600) // 60
        segundos = tiempo_segundos % 60

        print(f"\nCómo llegar desde {orig} hasta {dest}")
        print(f"Medio de transporte: {nombre_tipo_ruta}")
        print("Distancia: {:.2f} millas ({:.2f} km)".format(distancia_millas, distancia_km))
        print("Duración del viaje: {:.2f} horas, {:.2f} minutos, {:.2f} segundos".format(
            float(horas), float(minutos), float(segundos)))

        print("\n--- Narrativa del viaje ---")
        for maniobra in json_data["route"]["legs"][0]["maneuvers"]:
            print(maniobra["narrative"])
    else:
        print("No se pudo calcular la ruta entre esas ciudades. Verifique los nombres ingresados.")
        print("Mensajes de la API:", json_data["info"].get("messages"))

print("\nPrograma finalizado.")
