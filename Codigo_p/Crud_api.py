import requests

class API:
    def __init__(self, url):
        self.url = url
        self.token = None  # Aquí se almacenará el token JWT de acceso
        self.refresh_token = None  # Aquí se almacenará el token de renovación

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
        except Exception as e:
            print(f"Error al conectarse al servidor: {e}")

    def iniciar_sesion(self):
        """Inicia sesión y obtiene un token JWT."""
        print("\n=== Iniciar Sesión ===")
        username = input("Nombre de usuario: ").strip()
        password = input("Contraseña: ").strip()

        if not username or not password:
            print("Error: Nombre de usuario y contraseña no pueden estar vacíos.")
            return False

        try:
            response = requests.post(f"{self.url}login/", json={
                "username": username,
                "password": password
            })

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access")
                self.refresh_token = data.get("refresh")
                print("Inicio de sesión exitoso. ¡Bienvenido!")
                return True
            else:
                error_message = response.json().get('detail') or response.text
                print(f"Error al iniciar sesión: {error_message}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error al conectarse al servidor: {e}")
            return False

    def renovar_token(self):
        """Renueva el token JWT usando el refresh token."""
        if not self.refresh_token:
            print("Error: No hay refresh token disponible. Inicie sesión nuevamente.")
            return False

        try:
            response = requests.post(f"{self.url}refresh/", json={
                "refresh": self.refresh_token
            })
            if response.status_code == 200:
                self.token = response.json().get("access")
                print("Token renovado exitosamente.")
                return True
            else:
                print(f"Error al renovar el token: {response.json().get('detail', response.text)}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error al conectarse al servidor: {e}")
            return False

    def _headers(self):
        """Genera los encabezados con el token JWT, renovándolo si es necesario."""
        if not self.token:
            raise Exception("Error: No autenticado. Inicie sesión primero.")

        # Intentar renovar el token si está cerca de expirar o es inválido
        try:
            # Opcional: aquí podrías agregar una lógica para verificar la expiración del token
            return {"Authorization": f"Bearer {self.token}"}
        except Exception as e:
            print(f"Error al generar encabezados: {e}")
            raise
    def insertar(self):
        try:
            # Solicitar datos al usuario
            name = input("Nombre completo: ").strip()
            username = input("Nombre de usuario: ").strip()
            lenguaje = input("Lenguaje de programación: ").strip()
            
            # Validar que los campos no estén vacíos
            if not name or not username or not lenguaje:
                print("Error: Todos los campos de texto deben completarse.")
                return
            
            # Validar la edad
            try:
                edad = int(input("Edad: "))
                if edad <= 0:
                    print("La edad debe ser un número mayor a 0.")
                    return
            except ValueError:
                print("Error: La edad debe ser un número válido.")
                return
            
            print("¿Es un programador activo?")
            print("[1] Sí")
            print("[2] No")
            op = input("Seleccione una opción: ").strip()
            
            # Validar la entrada para el estado activo
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
            
            # Manejo de códigos HTTP
            if respuesta.status_code == 201:  # Código 201: Creación exitosa
                print(f"Operación exitosa (Status Code: {respuesta.status_code})")
                datos_respuesta = respuesta.json()
                print("========================")
                print(f"Usuario Insertado:")
                print("========================")
                print(f"ID: {datos_respuesta.get('id', 'N/A')}")
                print(f"Nombre: {datos_respuesta.get('fullname', 'N/A')}") 
                print(f"Usuario: {datos_respuesta.get('nickname', 'N/A')}") 
                print(f"Lenguaje de programación: {datos_respuesta.get('language', 'N/A')}") 
                print(f"Edad: {datos_respuesta.get('age', 'N/A')}")
                is_active = "Sí" if datos_respuesta.get('is_active', False) else "No"
                print(f"Activo: {is_active}")
                print("========================")
            elif 400 <= respuesta.status_code < 500:
                print(f"Error del cliente ({respuesta.status_code}): {respuesta.json().get('message', 'Solicitud inválida.')}")
            elif 500 <= respuesta.status_code < 600:
                print(f"Error del servidor ({respuesta.status_code}): Por favor, intente más tarde.")
            else:
                print(f"Respuesta no manejada: {respuesta.status_code}")

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
                respuesta = requests.get(user_url, headers=self._headers())

                if respuesta.status_code == 200:
                    print(f"Operación exitosa (Status Code: {respuesta.status_code})")
                    user_data = respuesta.json()
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
                elif 400 <= respuesta.status_code < 500:
                    # Error del cliente
                    print(f"Error del cliente ({respuesta.status_code}): {respuesta.json().get('message', 'Solicitud inválida.')}")
                elif 500 <= respuesta.status_code < 600:
                    # Error del servidor
                    print(f"Error del servidor ({respuesta.status_code}): Por favor, intente más tarde.")
                else:
                    # Otros códigos no esperados
                    print(f"Respuesta no manejada: {respuesta.status_code}")
            elif op == 2:
                try:
                    update_url = f"{self.url}programmers/"
                    respuesta = requests.get(update_url, headers=self._headers())
                    
                    # Manejo de códigos de estado HTTP
                    if respuesta.status_code == 200:
                        print(f"Operación exitosa (Status Code: {respuesta.status_code})")
                        users = respuesta.json()
                        
                        if not isinstance(users, list):
                            print("La respuesta del API no es una lista válida.")
                            return
                        
                        count = int(input("Cantidad de usuarios a mostrar: "))
                        if count <= 0:
                            print("Debe ingresar un número mayor a 0.")
                            return
                        
                        print("Usuarios Listados:")
                        print("========================")
                        for user in users[:count]:
                            print(f"ID: {user.get('id', 'N/A')}")
                            print(f"Nombre: {user.get('fullname', 'N/A')}")
                            print(f"Usuario: {user.get('nickname', 'N/A')}")
                            print(f"Lenguaje: {user.get('language', 'N/A')}")
                            print(f"Edad: {user.get('age', 'N/A')}")
                            # Transformación de 'is_active' a 'Sí' o 'No'
                            is_active = "Sí" if user.get('is_active', False) else "No"
                            print(f"Activo: {is_active}")
                            print("========================")
                    elif 400 <= respuesta.status_code < 500:
                        print(f"Error del cliente ({respuesta.status_code}): {respuesta.json().get('message', 'Solicitud inválida.')}")
                    elif 500 <= respuesta.status_code < 600:
                        print(f"Error del servidor ({respuesta.status_code}): Por favor, intente más tarde.")
                    else:
                        print(f"Respuesta no manejada: {respuesta.status_code}")
                
                except requests.exceptions.RequestException as e:
                    print(f"Error en la solicitud: {e}")
                except ValueError:
                    print("Debe ingresar un número válido para la cantidad de usuarios.")
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
            lenguaje = input("Nueva lenguaje de programación: ")
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

            # Manejo de códigos de estado HTTP
            if respuesta.status_code == 200:
                print(f"Operación exitosa (Status Code: {respuesta.status_code})")
                datos = respuesta.json()
                print("========================")
                print(f"Usuario Actualizado:")
                print("========================")
                print(f"ID: {datos['id']}")
                print(f"Nombre: {datos['fullname']}")
                print(f"Usuario: {datos['nickname']}")
                print(f"Lenguaje de Programación: {datos['language']}")
                print(f"Edad: {datos['age']}")
                # Transformación de 'is_active' a 'Sí' o 'No'
                is_active = "Sí" if datos.get('is_active', False) else "No"
                print(f"Activo: {is_active}")
                print("========================")
            elif respuesta.status_code == 404:
                print(f"Error: Usuario con ID {id_usuario} no encontrado.")
            elif 400 <= respuesta.status_code < 500:
                print(f"Error del cliente ({respuesta.status_code}): {respuesta.json().get('message', 'Solicitud inválida.')}")
            elif 500 <= respuesta.status_code < 600:
                print(f"Error del servidor ({respuesta.status_code}): Por favor, intente más tarde.")
            else:
                print(f"Respuesta no manejada: {respuesta.status_code}")

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
            if respuesta.status_code == 200 or respuesta.status_code == 204:
                print(f"Operación exitosa (Status Code: {respuesta.status_code})")
                # Eliminación exitosa
                print(f"Usuario con ID {id_usuario} eliminado correctamente.")
            elif respuesta.status_code == 404:
                # Usuario no encontrado
                print(f"Error: Usuario con ID {id_usuario} no encontrado.")
            elif 400 <= respuesta.status_code < 500:
                # Error del cliente
                print(f"Error del cliente ({respuesta.status_code}): {respuesta.json().get('message', 'Solicitud inválida.')}")
            elif 500 <= respuesta.status_code < 600:
                # Error del servidor
                print(f"Error del servidor ({respuesta.status_code}): Por favor, intente más tarde.")
            else:
                # Otros códigos no esperados
                print(f"Respuesta no manejada: {respuesta.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
        except ValueError:
            print("Error al ingresar el ID del producto. Verifique e intente nuevamente.")
