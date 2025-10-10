from conexion import conectarbd
from hashlib import sha256
import pymysql


def validar_docente(correo, password):
    try:
        connection = conectarbd()
        if not connection:
            return None

        with connection.cursor() as cursor:
            query = "SELECT * FROM Docente WHERE correo = %s AND password = %s"
            cursor.execute(query, (correo, password))
            result = cursor.fetchone()

        connection.close()
        return result

    except Exception as e:
        # opcional: print(e) para depuración
        return None
    


def validar_docente(correo, password, nombres, apellidos):
    try:
        connection = conectarbd()
        if not connection:
            return None

        password_encript = sha256(str(password).encode('utf-8')).hexdigest()
        with connection.cursor() as cursor:
            query = "insert into Docente (correo, password, nombres, apellidos)  values (%s, %s, %s, %s)"
            cursor.execute(query, (correo, password_encript, nombres, apellidos))
            cursor.fetchone()
        return True

    except pymysql.err.IntegrityError as e:
        # Código 1062 de MySQL = Duplicate entry
        if e.args[0] == 1062:
            print("Error: El correo ya existe")
            return "duplicado"
        else:
            print("Error de integridad:", e)
            return None

    except Exception as e:
        print("Otro error:", e)
        return None