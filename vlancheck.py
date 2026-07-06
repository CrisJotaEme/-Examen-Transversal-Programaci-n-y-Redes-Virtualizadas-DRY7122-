def verificar_vlan():
    while True:
        entrada = input("Ingrese el número de VLAN (o 's' para salir): ")
        if entrada.lower() == "s":
            print("Saliendo...")
            break
        if not entrada.isdigit():
            print("Debe ingresar solo números.\n")
            continue
        vlan = int(entrada)
        if 1 <= vlan <= 1005:
            print(f"La VLAN {vlan} corresponde al rango NORMAL (1-1005).\n")
        elif 1006 <= vlan <= 4094:
            print(f"La VLAN {vlan} corresponde al rango EXTENDIDO (1006-4094).\n")
        else:
            print(f"La VLAN {vlan} no es válida (rango 1-4094).\n")

if __name__ == "__main__":
    verificar_vlan()
