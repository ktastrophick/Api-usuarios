from Crud_api import API

def menu_api():
    url = 'http://127.0.0.1:8000/api/'
    datos_api = API(url)

    while True:
        print("\n========================")
        print("MENU PRINCIPAL")
        print("========================")
        print("[1] Registrarse")
        print("[2] Iniciar Sesión")
        print("[3] Salir")
        print("========================")

        opcion = input("Seleccionar una opción: ").strip()

        if opcion == "1":
            datos_api.registrar()
        elif opcion == "2":
            # Inicia sesión y luego redirige automáticamente al menú CRUD
            if datos_api.iniciar_sesion():
                menu_crud(datos_api)  # Solo redirigir al menú CRUD si el login es exitoso
            else:
                print("Error al iniciar sesión. Intente nuevamente.")
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def menu_crud(api):
    while True:
        print("\n========================")
        print("MENU CRUD")
        print("========================")
        print("[1] Insertar Registro")
        print("[2] Listar Registros")
        print("[3] Actualizar Registro")
        print("[4] Eliminar Registro")
        print("[5] Regresar al Menú Principal")
        print("========================")

        opcion = input("Seleccionar una opción: ").strip()

        if opcion == "1":
            api.insertar()
        elif opcion == "2":
            api.listar()
        elif opcion == "3":
            api.actualizar()
        elif opcion == "4":
            api.eliminar()
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu_api()
