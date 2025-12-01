"""
Reconocimiento Facial usando OpenCV (compatible con Python 3.13)
Librería liviana sin dependencias adicionales pesadas
"""
import numpy as np
import cv2
import json
import base64
from scipy.spatial.distance import cosine
import os


# Ruta para el clasificador Haar de OpenCV
HAAR_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'


def cargar_clasificador_facial():
    """Carga el clasificador Haar de OpenCV para detección facial"""
    try:
        if not os.path.exists(HAAR_CASCADE_PATH):
            print(f"⚠️ No se encontró el clasificador en: {HAAR_CASCADE_PATH}")
            return None
        
        clasificador = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
        if clasificador.empty():
            print("⚠️ Error al cargar el clasificador facial")
            return None
        
        return clasificador
    except Exception as e:
        print(f"❌ Error al cargar clasificador facial: {e}")
        return None


def convertir_base64_a_imagen(imagen_base64):
    """Convierte imagen base64 a array numpy de OpenCV"""
    try:
        # Si viene con prefijo data:image, lo removemos
        if ',' in imagen_base64:
            imagen_base64 = imagen_base64.split(',')[1]
        
        img_bytes = base64.b64decode(imagen_base64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            print("❌ Error: No se pudo decodificar la imagen")
            return None
        
        return img
    except Exception as e:
        print(f"❌ Error al convertir base64 a imagen: {e}")
        return None


def detectar_rostro(imagen):
    """Detecta rostros en una imagen usando OpenCV Haar Cascade"""
    try:
        clasificador = cargar_clasificador_facial()
        if clasificador is None:
            return None
        
        # Convertir a escala de grises para mejor detección
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        
        # Detectar rostros
        rostros = clasificador.detectMultiScale(
            gris,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        if len(rostros) == 0:
            print("⚠️ No se detectó ningún rostro en la imagen")
            return None
        
        # Obtener el rostro más grande (asumimos que es el principal)
        rostro = max(rostros, key=lambda r: r[2] * r[3])
        x, y, w, h = rostro
        
        # Extraer región facial
        region_facial = imagen[y:y+h, x:x+w]
        
        return region_facial
    except Exception as e:
        print(f"❌ Error al detectar rostro: {e}")
        return None


def calcular_lbp(imagen_gris):
    """Calcula Local Binary Pattern (LBP) como descriptor de textura"""
    try:
        # Tamaño de la ventana para LBP
        radio = 1
        puntos = 8
        
        lbp = np.zeros_like(imagen_gris)
        h, w = imagen_gris.shape
        
        for i in range(radio, h - radio):
            for j in range(radio, w - radio):
                centro = imagen_gris[i, j]
                codigo = 0
                
                for k in range(puntos):
                    angulo = 2 * np.pi * k / puntos
                    x = int(i + radio * np.cos(angulo))
                    y = int(j + radio * np.sin(angulo))
                    
                    if imagen_gris[x, y] >= centro:
                        codigo |= (1 << k)
                
                lbp[i, j] = codigo
        
        # Calcular histograma del LBP
        hist, _ = np.histogram(lbp.ravel(), bins=256, range=(0, 256))
        hist = hist.astype(np.float32)
        hist /= (hist.sum() + 1e-7)  # Normalizar
        
        return hist
    except Exception as e:
        print(f"⚠️ Error calculando LBP, usando método alternativo: {e}")
        # Método alternativo más simple
        hist, _ = np.histogram(imagen_gris.ravel(), bins=64, range=(0, 256))
        hist = hist.astype(np.float32)
        hist /= (hist.sum() + 1e-7)
        return hist


def extraer_caracteristicas_faciales(region_facial):
    """
    Extrae características faciales para crear un embedding
    Usa histogramas, momentos de imagen y LBP
    """
    try:
        # Redimensionar a tamaño estándar para consistencia
        region_facial = cv2.resize(region_facial, (128, 128))
        
        # Convertir a escala de grises
        gris = cv2.cvtColor(region_facial, cv2.COLOR_BGR2GRAY)
        
        # 1. Histograma de intensidades (64 bins)
        hist_intensidad, _ = np.histogram(gris.ravel(), bins=64, range=(0, 256))
        hist_intensidad = hist_intensidad.astype(np.float32)
        hist_intensidad /= (hist_intensidad.sum() + 1e-7)  # Normalizar
        
        # 2. Momentos de imagen (características geométricas)
        momentos = cv2.moments(gris)
        caracteristicas_momentos = [
            momentos['m00'] if momentos['m00'] != 0 else 0,
            momentos['m10'] / momentos['m00'] if momentos['m00'] != 0 else 0,
            momentos['m01'] / momentos['m00'] if momentos['m00'] != 0 else 0,
            momentos['mu20'] / momentos['m00'] if momentos['m00'] != 0 else 0,
            momentos['mu11'] / momentos['m00'] if momentos['m00'] != 0 else 0,
            momentos['mu02'] / momentos['m00'] if momentos['m00'] != 0 else 0,
            momentos['mu30'] / momentos['m00'] if momentos['m00'] != 0 else 0,
            momentos['mu21'] / momentos['m00'] if momentos['m00'] != 0 else 0,
            momentos['mu12'] / momentos['m00'] if momentos['m00'] != 0 else 0,
            momentos['mu03'] / momentos['m00'] if momentos['m00'] != 0 else 0,
        ]
        
        # 3. Histograma de gradientes (HOG simplificado)
        sobelx = cv2.Sobel(gris, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gris, cv2.CV_64F, 0, 1, ksize=3)
        magnitud = np.sqrt(sobelx**2 + sobely**2)
        hist_gradientes, _ = np.histogram(magnitud.ravel(), bins=32, range=(0, np.max(magnitud)))
        hist_gradientes = hist_gradientes.astype(np.float32)
        hist_gradientes /= (hist_gradientes.sum() + 1e-7)
        
        # 4. LBP (Local Binary Pattern) para textura
        lbp_hist = calcular_lbp(gris)
        # Reducir a 32 bins para mantener compacto
        lbp_reducido = lbp_hist[:32] if len(lbp_hist) >= 32 else lbp_hist
        
        # 5. Estadísticas básicas
        estadisticas = [
            np.mean(gris),
            np.std(gris),
            np.median(gris),
            np.min(gris),
            np.max(gris)
        ]
        
        # Combinar todas las características en un embedding
        embedding = np.concatenate([
            hist_intensidad,  # 64 características
            np.array(caracteristicas_momentos),  # 10 características
            hist_gradientes,  # 32 características
            lbp_reducido[:32],  # 32 características (máximo)
            np.array(estadisticas)  # 5 características
        ])
        
        # Normalizar el embedding
        norma = np.linalg.norm(embedding)
        if norma > 0:
            embedding = embedding / norma
        
        return embedding.tolist()
        
    except Exception as e:
        print(f"❌ Error al extraer características faciales: {e}")
        import traceback
        traceback.print_exc()
        return None


def generar_embedding_facial(imagen_base64):
    """
    Genera un embedding facial desde una imagen en base64
    Retorna el embedding como JSON string para guardar en BD
    """
    try:
        # Convertir base64 a imagen
        imagen = convertir_base64_a_imagen(imagen_base64)
        if imagen is None:
            return None
        
        # Detectar rostro
        region_facial = detectar_rostro(imagen)
        if region_facial is None:
            return None
        
        # Extraer características
        embedding = extraer_caracteristicas_faciales(region_facial)
        if embedding is None:
            return None
        
        # Retornar como JSON string para guardar en BD
        return json.dumps(embedding)
        
    except Exception as e:
        print(f"❌ Error al generar embedding facial: {e}")
        import traceback
        traceback.print_exc()
        return None


def verificar_rostro(imagen_base64, embedding_guardado):
    """
    Verifica si el rostro en la imagen coincide con el embedding guardado
    Retorna True si coinciden, False en caso contrario
    """
    try:
        # Generar embedding de la imagen de login
        embedding_login_json = generar_embedding_facial(imagen_base64)
        if embedding_login_json is None:
            return False
        
        embedding_login = np.array(json.loads(embedding_login_json))
        
        # Cargar embedding guardado
        if isinstance(embedding_guardado, str):
            embedding_almacenado = np.array(json.loads(embedding_guardado))
        else:
            embedding_almacenado = np.array(embedding_guardado)
        
        # Verificar que tengan la misma dimensión
        if len(embedding_login) != len(embedding_almacenado):
            print(f"⚠️ Dimensiones diferentes: {len(embedding_login)} vs {len(embedding_almacenado)}")
            return False
        
        # Calcular distancia coseno
        distancia = cosine(embedding_login, embedding_almacenado)
        
        # Umbral de similitud (ajustable según necesidades)
        # Valores más bajos = más estricto
        umbral = 0.35
        
        if distancia < umbral:
            print(f"✅ Rostro verificado correctamente (distancia: {distancia:.4f})")
            return True
        else:
            print(f"❌ Rostro no coincide (distancia: {distancia:.4f}, umbral: {umbral})")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar rostro: {e}")
        import traceback
        traceback.print_exc()
        return False