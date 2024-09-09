from flask import Flask, request, jsonify
import bcrypt
import re
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Conectar a MySQL
def conectar_db():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='microservicios',
            user='micro',
            password='Linux123'
        )
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Validación de la contraseña
def validar_contrasena(password):
    if 8 <= len(password) <= 15:
        if re.search("[A-Z]", password) and re.search("[a-z]", password) and re.search(r"[!\"#$%&/()]", password):
            return True
    return False

# Encriptar la contraseña
def encriptar_contrasena(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed

# Manejo de errores
def manejo_errores(mensaje):
    return jsonify({"error": mensaje}), 400

# Verificar si el estudiante ya existe
def estudiante_existe(cursor, email_or_username):
    cursor.execute("SELECT * FROM estudiantes WHERE email_or_username = %s", (email_or_username,))
    return cursor.fetchone() is not None

@app.route('/registrar_estudiante', methods=['POST'])
def registrar_estudiante():
    data = request.get_json()

    email_or_username = data.get('email_or_username')
    password = data.get('password')
    nombre = data.get('nombre')
    numero_control = data.get('numero_control')
    carrera = data.get('carrera')
    grupo = data.get('grupo')  # Nuevo campo

    if not email_or_username or not password or not nombre or not numero_control:
        return manejo_errores("Se requiere correo electrónico o nombre de usuario, contraseña, nombre y número de control")

    if not validar_contrasena(password):
        return manejo_errores("La contraseña no cumple con los requisitos")

    connection = conectar_db()
    if connection is None:
        return manejo_errores("No se pudo conectar a la base de datos")

    cursor = connection.cursor()

    if estudiante_existe(cursor, email_or_username):
        return manejo_errores("El estudiante ya está registrado")

    password_encriptada = encriptar_contrasena(password)

    try:
        cursor.execute(
            "INSERT INTO estudiantes (email_or_username, password, nombre, numero_control, carrera, grupo) VALUES (%s, %s, %s, %s, %s, %s)",
            (email_or_username, password_encriptada.decode('utf-8'), nombre, numero_control, carrera, grupo)
        )
        connection.commit()
    except Error as e:
        return manejo_errores(f"Error al registrar estudiante: {e}")
    finally:
        cursor.close()
        connection.close()

    return jsonify({"mensaje": "Estudiante registrado exitosamente"}), 201

# Ruta para iniciar sesión (login)
@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    data = request.get_json()

    email_or_username = data.get('email_or_username')
    password = data.get('password')

    if not email_or_username or not password:
        return manejo_errores("Se requiere correo electrónico o nombre de usuario y contraseña")

    # Conectar a la base de datos
    connection = conectar_db()
    if connection is None:
        return manejo_errores("No se pudo conectar a la base de datos")

    cursor = connection.cursor()

    # Verificar si el estudiante existe
    cursor.execute("SELECT password FROM estudiantes WHERE email_or_username = %s", (email_or_username,))
    estudiante = cursor.fetchone()

    if estudiante is None:
        return manejo_errores("El estudiante no está registrado")

    password_encriptada = estudiante[0]

    # Verificar la contraseña
    if not bcrypt.checkpw(password.encode('utf-8'), password_encriptada.encode('utf-8')):
        return manejo_errores("La contraseña es incorrecta")

    return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200

@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estudiantes")
        estudiantes = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify(estudiantes), 200
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500


@app.route('/estudiantes/<int:id>', methods=['GET'])
def obtener_estudiante_por_id(id):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estudiantes WHERE id = %s", (id,))
        estudiante = cursor.fetchone()
        cursor.close()
        conexion.close()
        if estudiante:
            return jsonify(estudiante), 200
        else:
            return jsonify({"error": "Estudiante no encontrado"}), 404
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

@app.route('/estudiantes/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    data = request.get_json()
    nombre = data.get('nombre')
    email_or_username = data.get('email_or_username')
    password = data.get('password')
    carrera = data.get('carrera')
    numero_control = data.get('numero_control')
    grupo = data.get('grupo')  # Nuevo campo

    if password:
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode('utf-8'), salt)

    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM estudiantes WHERE id = %s", (id,))
            estudiante_actual = cursor.fetchone()

            if not estudiante_actual:
                cursor.close()
                conexion.close()
                return jsonify({"error": "Estudiante no encontrado"}), 404

            update_fields = []
            params = []

            if nombre and nombre != estudiante_actual[3]:
                update_fields.append("nombre = %s")
                params.append(nombre)

            if email_or_username and email_or_username != estudiante_actual[1]:
                update_fields.append("email_or_username = %s")
                params.append(email_or_username)

            if password:
                update_fields.append("password = %s")
                params.append(password)

            if carrera:
                update_fields.append("carrera = %s")
                params.append(carrera)

            if numero_control:
                update_fields.append("numero_control = %s")
                params.append(numero_control)

            if grupo:  # Actualización del campo grupo
                update_fields.append("grupo = %s")
                params.append(grupo)

            if not update_fields:
                cursor.close()
                conexion.close()
                return jsonify({"message": "No se realizaron cambios"}), 200

            update_fields_str = ", ".join(update_fields)
            params.append(id)

            cursor.execute(f"""
                UPDATE estudiantes
                SET {update_fields_str}
                WHERE id = %s
            """, tuple(params))
            conexion.commit()

            return jsonify({"message": "Estudiante actualizado con éxito"}), 200

        except mysql.connector.Error as err:
            return jsonify({"error": f"Error en la base de datos: {str(err)}"}), 500

        finally:
            cursor.close()
            conexion.close()
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

@app.route('/estudiantes/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Primero, intentamos eliminar el estudiante por ID
            cursor.execute("DELETE FROM estudiantes WHERE id = %s", (id,))
            conexion.commit()

            # Verificamos si el estudiante fue eliminado
            if cursor.rowcount > 0:
                # Si el estudiante fue eliminado, ajustamos el AUTO_INCREMENT
                cursor.execute("SELECT MAX(id) FROM estudiantes")
                max_id = cursor.fetchone()[0]
                # Si no hay registros restantes, restablecemos a 1, de lo contrario, incrementamos en 1
                if max_id is None:
                    nuevo_auto_increment = 1
                else:
                    nuevo_auto_increment = max_id + 1

                # Ajustar el valor de AUTO_INCREMENT
                cursor.execute(f"ALTER TABLE estudiantes AUTO_INCREMENT = {nuevo_auto_increment}")
                conexion.commit()

                return jsonify({"message": "Estudiante eliminado y AUTO_INCREMENT ajustado correctamente"}), 200
            else:
                return jsonify({"error": "Estudiante no encontrado"}), 404

        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conexion.close()
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500



@app.route('/registrar_clase', methods=['POST'])
def registrar_clase():
    data = request.get_json()

    nombre_clase = data.get('nombre_clase')
    profesor = data.get('profesor')
    horario = data.get('horario')
    aula = data.get('aula')
    calificacion = data.get('calificacion')
    semestre = data.get('semestre')
    descripcion = data.get('descripcion')
    estudiante_id = data.get('estudiante_id')

    # Validación de campos obligatorios
    if not nombre_clase or not profesor or not estudiante_id or not horario:
        return manejo_errores("Se requiere nombre de clase, profesor, horario y estudiante asociado")

    # Validación de calificación
    if not isinstance(calificacion, (int, float)) or not (0 <= calificacion <= 10):
        return manejo_errores("La calificación debe ser un número entre 0 y 10")

    # Validación de semestre
    if not isinstance(semestre, int) or semestre <= 0:
        return manejo_errores("El semestre debe ser un número entero positivo")

    connection = conectar_db()
    if connection is None:
        return manejo_errores("No se pudo conectar a la base de datos")

    cursor = connection.cursor()

    try:
        # Verificar si el estudiante existe
        cursor.execute("SELECT * FROM estudiantes WHERE id = %s", (estudiante_id,))
        estudiante = cursor.fetchone()
        if not estudiante:
            return manejo_errores("El estudiante no existe")

        # Verificar si la clase ya existe para el mismo estudiante y el mismo horario
        cursor.execute("""
            SELECT * FROM clases 
            WHERE nombre_clase = %s AND estudiante_id = %s AND horario = %s
        """, (nombre_clase, estudiante_id, horario))
        clase_duplicada = cursor.fetchone()

        if clase_duplicada:
            return manejo_errores("El estudiante ya está registrado en esta clase y horario")

        # Insertar la clase en la base de datos
        cursor.execute(
            "INSERT INTO clases (nombre_clase, profesor, horario, aula, calificacion, semestre, descripcion, estudiante_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (nombre_clase, profesor, horario, aula, calificacion, semestre, descripcion, estudiante_id)
        )
        connection.commit()

    except Error as e:
        return manejo_errores(f"Error al registrar la clase: {e}")
    finally:
        cursor.close()
        connection.close()

    return jsonify({"mensaje": "Clase registrada exitosamente"}), 201

@app.route('/clases/<int:id>', methods=['PUT'])
def actualizar_clase(id):
    data = request.get_json()
    nombre_clase = data.get('nombre_clase')
    profesor = data.get('profesor')
    horario = data.get('horario')
    aula = data.get('aula')
    calificacion = data.get('calificacion')
    semestre = data.get('semestre')
    descripcion = data.get('descripcion')
    estudiante_id = data.get('estudiante_id')

    # Conexión a la base de datos
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()

            # Verificar si la clase con el ID proporcionado existe
            cursor.execute("SELECT * FROM clases WHERE id = %s", (id,))
            clase_actual = cursor.fetchone()

            if not clase_actual:
                cursor.close()
                conexion.close()
                return jsonify({"error": "Clase no encontrada"}), 404

            # Permitir que el mismo estudiante se registre más de una vez con un horario diferente
            cursor.execute("""
                SELECT * FROM clases WHERE nombre_clase = %s AND estudiante_id = %s AND horario = %s
            """, (nombre_clase, estudiante_id, horario))
            clase_duplicada = cursor.fetchone()

            if clase_duplicada:
                return jsonify({"error": "El estudiante ya está registrado en esta clase y horario"}), 409

            # Actualizar los campos de la clase
            update_fields = []
            params = []

            if nombre_clase and nombre_clase != clase_actual[1]:
                update_fields.append("nombre_clase = %s")
                params.append(nombre_clase)

            if profesor and profesor != clase_actual[2]:
                update_fields.append("profesor = %s")
                params.append(profesor)

            if horario and horario != clase_actual[3]:
                update_fields.append("horario = %s")
                params.append(horario)

            if aula and aula != clase_actual[4]:
                update_fields.append("aula = %s")
                params.append(aula)

            if calificacion and isinstance(calificacion, (int, float)) and 0 <= calificacion <= 10:
                update_fields.append("calificacion = %s")
                params.append(calificacion)

            if semestre and isinstance(semestre, int) and semestre != clase_actual[6]:
                update_fields.append("semestre = %s")
                params.append(semestre)

            if descripcion and descripcion != clase_actual[7]:
                update_fields.append("descripcion = %s")
                params.append(descripcion)

            if not update_fields:
                cursor.close()
                conexion.close()
                return jsonify({"message": "No se realizaron cambios"}), 200

            update_fields_str = ", ".join(update_fields)
            params.append(id)

            cursor.execute(f"""
                UPDATE clases
                SET {update_fields_str}
                WHERE id = %s
            """, tuple(params))
            conexion.commit()

            return jsonify({"mensaje": "Clase actualizada exitosamente"}), 200

        except mysql.connector.Error as err:
            return jsonify({"error": f"Error en la base de datos: {str(err)}"}), 500

        finally:
            cursor.close()
            conexion.close()
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500


@app.route('/clases', methods=['GET'])
def obtener_clases():
    connection = conectar_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clases")
        clases = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(clases), 200
    else:
        return manejo_errores("No se pudo conectar a la base de datos")
@app.route('/clases/<int:id>', methods=['GET'])
def obtener_clase_por_id(id):
    connection = conectar_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clases WHERE id = %s", (id,))
        clase = cursor.fetchone()
        cursor.close()
        connection.close()
        if clase:
            return jsonify(clase), 200
        else:
            return manejo_errores("Clase no encontrada"), 404
    else:
        return manejo_errores("No se pudo conectar a la base de datos")


@app.route('/clases/<int:id>', methods=['DELETE'])
def eliminar_clase(id):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Intentamos eliminar la clase por ID
            cursor.execute("DELETE FROM clases WHERE id = %s", (id,))
            conexion.commit()

            # Verificamos si la clase fue eliminada
            if cursor.rowcount > 0:
                # Si la clase fue eliminada, ajustamos el AUTO_INCREMENT
                cursor.execute("SELECT MAX(id) FROM clases")
                max_id = cursor.fetchone()[0]

                # Si no hay registros restantes, restablecemos a 1, de lo contrario, ajustamos al siguiente valor
                if max_id is None:
                    nuevo_auto_increment = 1
                else:
                    nuevo_auto_increment = max_id + 1

                # Ajustar el valor de AUTO_INCREMENT
                cursor.execute(f"ALTER TABLE clases AUTO_INCREMENT = {nuevo_auto_increment}")
                conexion.commit()

                return jsonify({"message": "Clase eliminada y AUTO_INCREMENT ajustado correctamente"}), 200
            else:
                return jsonify({"error": "Clase no encontrada"}), 404

        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            conexion.close()
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
