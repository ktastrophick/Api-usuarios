import requests

class API:
    def __init__(self,url):
        self.url = url
        self.token = None  # Aquí se almacenará el token JWT

    def registrar(self):
        """Registra un nuevo usuario."""
        print("\n=== Registro ===")
        username = input("Nombre de usuario: ").strip()
        password = input("Contraseña: ").strip()
        email = input("Correo electrónico: ").strip()

        try:
            response = requests.post(f"{self.url}register/", json={
                "username": username,
                "password": password,
                "email": email
            })
            if response.status_code == 201:
                print("Usuario registrado exitosamente.")
            else:
                print(f"Error al registrar: {response.json().get('detail', response.text)}")
                print("Respuesta del servidor:"), response.text
        except Exception as e:
            print(f"Error al conectarse al servidor: {e}")

    def iniciar_sesion(self):
        """Inicia sesión y obtiene un token JWT."""
        print("\n=== Iniciar Sesión ===")
        username = input("Nombre de usuario: ").strip()
        password = input("Contraseña: ").strip()

        # Validar campos vacíos antes de enviar la solicitud
        if not username or not password:
            print("Error: Nombre de usuario y contraseña no pueden estar vacíos.")
            return False

        try:
            # Realizar la solicitud al servidor
            response = requests.post(f"{self.url}login/", json={
                "username": username,
                "password": password
            })

            # Evaluar el código de estado HTTP
            if response.status_code == 200:
                # Guardar y retornar el token
                self.token = response.json().get("access")
                print("Inicio de sesión exitoso. ¡Bienvenido!")
                return True
            else:
                # Manejar errores de autenticación o validación
                error_message = response.json().get('detail') or response.text
                print(f"Error al iniciar sesión: {error_message}")
                return False

        except requests.exceptions.RequestException as e:
            # Manejar errores de red o de conexión
            print(f"Error al conectarse al servidor: {e}")
            return False


    def _headers(self):
        """Genera los encabezados con el token JWT."""
        if not self.token:
            raise Exception("Error: No autenticado. Inicie sesión primero.")
        return {
            "Authorization": f"Bearer {self.token}"
        }

    def insertar(self):
        try:
            # Solicitar datos al usuario
            name = input("Nombre completo: ")
            username = input("Nombre de usuario: ")
            lenguaje = input("Lenguaje de programación: ")
            edad = int(input("Edad: "))
            print("¿Es un programador activo?")
            print("[1] Sí")
            print("[2] No")
            op = input("Seleccione una opción: ")
            
            # Validar la entrada
            if op == "1":
                activo = True
            elif op == "2":
                activo = False
            else:
                print(f"'{op}' no es una opción válida.")
                return  # Salir del método si la entrada no es válida

            # Crear el diccionario con los datos
            datos = {
                'fullname': name,
                'nickname': username,
                'language': lenguaje,
                'age': edad,
                'is_active': activo, 
            }

            # Hacer la solicitud POST
            respuesta = requests.post(f"{self.url}programmers/", json=datos, headers=self._headers())
            respuesta.raise_for_status()  # Verificar si la respuesta fue exitosa
            datos_respuesta = respuesta.json()
            
            # Mostrar los datos de la respuesta
            print("========================")
            print(f"Producto Insertado:")
            print(f"ID: {datos_respuesta.get('id', 'N/A')}")
            print(f"Nombre: {datos_respuesta.get('fullname', 'N/A')}") 
            print(f"Usuario: {datos_respuesta.get('nickname', 'N/A')}") 
            print(f"Lenguaje de programación: {datos_respuesta.get('language', 'N/A')}") 
            print(f"Edad: {datos_respuesta.get('age', 'N/A')}")
            print(f"Programador activo: {datos_respuesta.get('is_active', 'N/A')}")
            print("========================")

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
        except ValueError:
            print("Error en los datos ingresados. Verifique e intente nuevamente.")

    def listar(self):
        try:
            print("[1] Listar por ID")
            print("[2] Listar por cantidad")
            op = int(input("Seleccione una opción: "))

            if op == 1:
                user_id = int(input("ID del usuario: "))
                # URL específica para listar por ID
                user_url = f"{self.url}programmers/{user_id}/"  
                response = requests.get(user_url)

                if response.status_code == 200:
                    user_data = response.json()
                    print("========================")
                    print(f"ID: {user_data.get('id', 'N/A')}")
                    print(f"Nombre: {user_data.get('fullname', 'N/A')}")
                    print(f"Usuario: {user_data.get('nickname', 'N/A')}")
                    print(f"Lenguaje: {user_data.get('language', 'N/A')}")
                    print(f"Edad: {user_data.get('age', 'N/A')}")
                    # Transformación de 'is_active' a 'Sí' o 'No'
                    is_active = "Sí" if user_data.get('is_active', False) else "No"
                    print(f"Activo: {is_active}")
                    print("========================")
                else:
                    print(f"Error: Usuario con ID {user_id} no encontrado.")
                    print(f"Status Code: {response.status_code}")
            elif op == 2:
                update_url = f"{self.url}programmers/"
                response = requests.get(update_url, headers=self._headers())
                response.raise_for_status()
                users = response.json()

                if not isinstance(users, list):
                    print("La respuesta del API no es una lista válida.")
                    return

                count = int(input("Cantidad de usuarios a mostrar: "))
                print("Usuarios Listados:")
                for user in users[:count]:
                    print("========================")
                    print(f"ID: {user.get('id', 'N/A')}")
                    print(f"Nombre: {user.get('fullname', 'N/A')}")
                    print(f"Usuario: {user.get('nickname', 'N/A')}")
                    print(f"Lenguaje: {user.get('language', 'N/A')}")
                    print(f"Edad: {user.get('age', 'N/A')}")
                    # Transformación de 'is_active' a 'Sí' o 'No'
                    is_active = "Sí" if user_data.get('is_active', False) else "No"
                    print(f"Activo: {is_active}")
                    print("========================")
            else:
                print("Opción no válida.")

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
        except ValueError:
            print("Error en los datos ingresados. Verifique e intente nuevamente.")

    def actualizar(self):
        try:
            # Solicitar datos al usuario
            id_usuario = int(input("ID del usuario a actualizar: "))
            nombre = input("Nuevo nombre del Usuario: ")
            usuario = input("Nuevo nombre de usuario: ")
            lenguaje = input("Nueva lenguaje de programacion: ")
            edad = input("Nueva edad del programador: ")
            print("¿Es un programador activo?")
            print("[1] Sí")
            print("[2] No")
            op = input("Seleccione una opción: ")
            
            # Validar la entrada
            if op == "1":
                activo = True
            elif op == "2":
                activo = False
            else:
                print(f"'{op}' no es una opción válida.")
                return  # Salir del método si la entrada no es válida
            activo = input("Nuevo estado del programador: ")
            
            # Crear el diccionario con los datos
            datos = {
                'fullname': nombre,
                'nickname': usuario,
                'language': lenguaje,
                'age': edad,
                'is_active': activo, 
            }

            # Hacer la solicitud PUT
            update_url = f"{self.url}programmers/{id_usuario}/"
            respuesta = requests.put(update_url, json=datos, headers=self._headers())
            respuesta.raise_for_status()  # Verificar si la respuesta fue exitosa
            datos = respuesta.json()
            print("========================")
            print(f"Producto Actualizado:")
            print(f"ID: {datos['id']}")
            print(f"Nombre: {datos['fullname']}") 
            print(f"Usuario: {datos['nickname']}") 
            print(f"Lenguaje de Programacion: {datos['language']}") 
            print(f"Edad: {datos['age']}")
            # Transformación de 'is_active' a 'Sí' o 'No'
            is_active = "Sí" if datos.get('is_active', False) else "No"
            print(f"Activo: {is_active}")
            print("========================")

            
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
        except ValueError:
            print("Error en los datos ingresados. Verifique e intente nuevamente.")

    def eliminar(self):
        try:
            # Solicitar ID del producto a eliminar
            id_usuario = int(input("ID del usuario a eliminar: "))
            delete_url = f"{self.url}programmers/{id_usuario}/"

            # Hacer la solicitud DELETE
            respuesta = requests.delete(delete_url, headers=self._headers())
            respuesta.raise_for_status()  # Verificar si la respuesta fue exitosa
            print(f"Usuario {id_usuario} Eliminado.")

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
        except ValueError:
            print("Error al ingresar el ID del producto. Verifique e intente nuevamente.")
