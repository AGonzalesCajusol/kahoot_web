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
    


def registrardocente(correo, password, nombres, apellidos):
    try:
        connection = conectarbd()
        if not connection:
            return None

        password_encript = sha256(str(password).encode('utf-8')).hexdigest()
        with connection.cursor() as cursor:
            query = "insert into Docente (correo, password, nombres, apellidos)  values (%s, %s, %s, %s)"
            cursor.execute(query, (correo, password_encript, nombres, apellidos))
            connection.commit()
        return True 
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:    
            return {"mensaje": "Ya existe ese usuario"}

    except Exception as e:
        return {"mensaje" : str(e) }