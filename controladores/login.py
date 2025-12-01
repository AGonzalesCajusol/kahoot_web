import hashlib
import os
import base64
import io
from conexion import conectarbd
from flask import session
try:
    from PIL import Image
    PIL_AVAILABLE = True
    try:
        import numpy as np
        NUMPY_AVAILABLE = True
    except ImportError:
        NUMPY_AVAILABLE = False
except ImportError:
    PIL_AVAILABLE = False
    NUMPY_AVAILABLE = False

def validar_docente(correo, password):
    try:
        connection = conectarbd()
        if connection:
            cursor = connection.cursor()
        
            query = "SELECT * FROM Docente WHERE correo = %s"
            cursor.execute(query, (correo,))
            result = cursor.fetchone()  

            if result:
                hashed_password = result['password']
                input_hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

                if input_hashed_password == hashed_password:
                    session['docente_id'] = result['id_docente']
                    session['correo'] = result['correo']
                    session['nombres'] = result['nombres']
                    session['apellidos'] = result['apellidos']
                    return result  
                else:
                    return None  

            connection.close()
            return None  
        
    except Exception as e:
        return None

def validar_docente_facial(rostro_data):
    """
    Valida un docente mediante reconocimiento facial
    Args:
        rostro_data: Imagen en base64 del rostro a verificar
    Returns:
        Diccionario con datos del docente si coincide, None si no
    """
    try:
        connection = conectarbd()
        if not connection:
            return None

        cursor = connection.cursor()
        
        # Obtener todos los docentes que tienen rostro registrado
        query = "SELECT id_docente, correo, nombres, apellidos, rostro FROM Docente WHERE rostro IS NOT NULL AND rostro != ''"
        cursor.execute(query)
        docentes = cursor.fetchall()

        if not docentes:
            connection.close()
            return None

        for docente in docentes:
            rostro_path = docente.get('rostro')
            if not rostro_path:
                continue

            rostro_almacenado = leer_rostro_archivo(rostro_path)
            if not rostro_almacenado:
                continue
            
            similitud = comparar_rostros_simple(rostro_data, rostro_almacenado)
            
            if similitud >= 0.85:
                connection.close()
                return {
                    'id_docente': docente['id_docente'],
                    'correo': docente['correo'],
                    'nombres': docente['nombres'],
                    'apellidos': docente.get('apellidos', '')
                }

        connection.close()
        return None

    except Exception as e:
        return None

def validar_jugador_facial(rostro_data):
    """
    Valida un jugador mediante reconocimiento facial
    Args:
        rostro_data: Imagen en base64 del rostro a verificar
    Returns:
        Diccionario con datos del jugador si coincide, None si no
    """
    try:
        connection = conectarbd()
        if not connection:
            return None

        cursor = connection.cursor()
        
        # Obtener todos los jugadores que tienen rostro registrado
        query = "SELECT id_jugador, email, rostro FROM Jugador WHERE rostro IS NOT NULL AND rostro != ''"
        cursor.execute(query)
        jugadores = cursor.fetchall()

        if not jugadores:
            connection.close()
            return None

        for jugador in jugadores:
            rostro_path = jugador.get('rostro')
            if not rostro_path:
                continue

            rostro_almacenado = leer_rostro_archivo(rostro_path)
            if not rostro_almacenado:
                continue
            
            similitud = comparar_rostros_simple(rostro_data, rostro_almacenado)
            
            if similitud >= 0.85:
                connection.close()
                return {
                    'id_jugador': jugador['id_jugador'],
                    'email': jugador['email']
                }

        connection.close()
        return None

    except Exception as e:
        return None

def leer_rostro_archivo(rostro_path):
    """
    Lee un archivo de rostro y lo convierte a base64
    Args:
        rostro_path: Ruta relativa del archivo (ej: 'uploads/reconocimiento_facial/docente_...jpg')
    Returns:
        String base64 de la imagen o None si hay error
    """
    try:
        if isinstance(rostro_path, (list, tuple)):
            return None
        
        if not isinstance(rostro_path, str):
            return None

        if rostro_path.startswith('data:image'):
            return rostro_path

        if rostro_path.startswith('uploads/'):
            filepath = os.path.join('static', rostro_path)
        elif rostro_path.startswith('static/'):
            filepath = rostro_path
        else:
            filepath = os.path.join('static', 'uploads', 'reconocimiento_facial', rostro_path)

        if not os.path.exists(filepath):
            return None

        with open(filepath, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            return f"data:image/jpeg;base64,{base64_data}"
    except Exception as e:
        return None

def comparar_rostros_simple(rostro1, rostro2):
    """
    Comparación mejorada de rostros usando análisis de imágenes con Pillow (ligera)
    Esta función analiza las imágenes reales en lugar de solo strings base64.
    
    Args:
        rostro1: Imagen base64 del rostro capturado
        rostro2: Imagen base64 del rostro almacenado
    Returns:
        Valor de similitud entre 0 y 1
    """
    try:
        if PIL_AVAILABLE:
            return comparar_rostros_pillow(rostro1, rostro2)
        else:
            return comparar_rostros_basico(rostro1, rostro2)
    except Exception as e:
        return 0.0

def comparar_rostros_pillow(rostro1, rostro2):
    """
    Comparación de rostros usando Pillow para análisis de imágenes
    Compara histogramas, características de color y texturas básicas
    """
    try:
        # Decodificar imágenes base64
        if ',' in rostro1:
            rostro1_data = base64.b64decode(rostro1.split(',')[1])
        else:
            rostro1_data = base64.b64decode(rostro1)
            
        if ',' in rostro2:
            rostro2_data = base64.b64decode(rostro2.split(',')[1])
        else:
            rostro2_data = base64.b64decode(rostro2)

        # Cargar imágenes
        img1 = Image.open(io.BytesIO(rostro1_data))
        img2 = Image.open(io.BytesIO(rostro2_data))

        # Convertir a RGB si es necesario
        if img1.mode != 'RGB':
            img1 = img1.convert('RGB')
        if img2.mode != 'RGB':
            img2 = img2.convert('RGB')

        # Redimensionar a tamaño estándar para comparación (200x200)
        img1 = img1.resize((200, 200), Image.Resampling.LANCZOS)
        img2 = img2.resize((200, 200), Image.Resampling.LANCZOS)

        # 1. Comparar histogramas de color (muy efectivo para rostros similares)
        hist1 = img1.histogram()
        hist2 = img2.histogram()
        
        # Calcular correlación de histogramas
        hist_similarity = calcular_similitud_histogramas(hist1, hist2)

        # 2. Comparar características de color promedio
        pixels1 = list(img1.getdata())
        pixels2 = list(img2.getdata())
        
        # Calcular promedios RGB
        avg_r1 = sum(p[0] for p in pixels1) / len(pixels1)
        avg_g1 = sum(p[1] for p in pixels1) / len(pixels1)
        avg_b1 = sum(p[2] for p in pixels1) / len(pixels1)
        
        avg_r2 = sum(p[0] for p in pixels2) / len(pixels2)
        avg_g2 = sum(p[1] for p in pixels2) / len(pixels2)
        avg_b2 = sum(p[2] for p in pixels2) / len(pixels2)
        
        # Similitud de color promedio
        color_diff = abs(avg_r1 - avg_r2) + abs(avg_g1 - avg_g2) + abs(avg_b1 - avg_b2)
        max_diff = 255 * 3  # Máxima diferencia posible
        color_similarity = 1.0 - (color_diff / max_diff)

        # 3. Comparar distribución de píxeles (análisis de textura básico)
        # Convertir a arrays numpy si está disponible
        if NUMPY_AVAILABLE:
            try:
                arr1 = np.array(img1)
                arr2 = np.array(img2)
                
                # Calcular diferencia de píxeles
                diff = np.abs(arr1.astype(float) - arr2.astype(float))
                pixel_diff = np.mean(diff) / 255.0
                pixel_similarity = 1.0 - pixel_diff
            except:
                pixel_similarity = calcular_similitud_pixeles_basica(pixels1, pixels2)
        else:
            # Comparación básica sin numpy
            pixel_similarity = calcular_similitud_pixeles_basica(pixels1, pixels2)

        similitud_final = (hist_similarity * 0.5 + pixel_similarity * 0.3 + color_similarity * 0.2)
        return similitud_final

    except Exception as e:
        return comparar_rostros_basico(rostro1, rostro2)

def calcular_similitud_pixeles_basica(pixels1, pixels2):
    """Calcula similitud de píxeles sin numpy"""
    try:
        if len(pixels1) != len(pixels2):
            return 0.5
        
        total_diff = 0
        for p1, p2 in zip(pixels1, pixels2):
            diff_r = abs(p1[0] - p2[0])
            diff_g = abs(p1[1] - p2[1])
            diff_b = abs(p1[2] - p2[2])
            total_diff += (diff_r + diff_g + diff_b) / 3.0
        
        avg_diff = total_diff / len(pixels1) / 255.0
        return 1.0 - avg_diff
    except:
        return 0.5

def calcular_similitud_histogramas(hist1, hist2):
    """Calcula similitud entre dos histogramas usando correlación"""
    try:
        if len(hist1) != len(hist2):
            return 0.0
        
        # Normalizar histogramas
        sum1 = sum(hist1)
        sum2 = sum(hist2)
        
        if sum1 == 0 or sum2 == 0:
            return 0.0
        
        hist1_norm = [h / sum1 for h in hist1]
        hist2_norm = [h / sum2 for h in hist2]
        
        # Calcular correlación (similitud coseno)
        dot_product = sum(a * b for a, b in zip(hist1_norm, hist2_norm))
        magnitude1 = sum(a * a for a in hist1_norm) ** 0.5
        magnitude2 = sum(b * b for b in hist2_norm) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        correlation = dot_product / (magnitude1 * magnitude2)
        return max(0.0, min(1.0, correlation))
    except:
        return 0.0

def comparar_rostros_basico(rostro1, rostro2):
    """
    Comparación básica de strings base64 (fallback si Pillow no está disponible)
    """
    try:
        # Extraer solo la parte de datos de las imágenes base64
        if ',' in rostro1:
            rostro1 = rostro1.split(',')[1]
        if ',' in rostro2:
            rostro2 = rostro2.split(',')[1]

        if len(rostro1) == 0 or len(rostro2) == 0:
            return 0.0

        len_diff = abs(len(rostro1) - len(rostro2))
        max_len = max(len(rostro1), len(rostro2))
        if len_diff / max_len > 0.1:
            return 0.0

        # Comparar una muestra más grande
        comparison_length = min(len(rostro1), len(rostro2), 5000)
        
        matches = sum(1 for i in range(comparison_length) if rostro1[i] == rostro2[i])
        similitud_caracteres = matches / comparison_length if comparison_length > 0 else 0.0
        length_similarity = 1.0 - (len_diff / max_len) if max_len > 0 else 0.0

        # Comparar bloques
        bloque_size = 100
        num_bloques = min(len(rostro1), len(rostro2)) // bloque_size
        bloques_coincidentes = sum(1 for i in range(num_bloques) 
                                   if rostro1[i*bloque_size:(i+1)*bloque_size] == 
                                      rostro2[i*bloque_size:(i+1)*bloque_size])
        similitud_bloques = bloques_coincidentes / num_bloques if num_bloques > 0 else 0.0

        similitud_final = (similitud_caracteres * 0.6 + similitud_bloques * 0.3 + length_similarity * 0.1)
        return similitud_final

    except Exception as e:
        return 0.0
