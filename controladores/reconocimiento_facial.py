from deepface import DeepFace
import numpy as np
import cv2
import json
import base64
from scipy.spatial.distance import cosine

modelo = DeepFace.build_model('VGG-Face')

def generar_embedding_facial(imagen_base64):
    try:
        img_bytes = base64.b64decode(imagen_base64.split(',')[1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        embedding_objs = DeepFace.represent(img_path=img, model_name='VGG-Face', enforce_detection=False)
        embedding = embedding_objs[0]['embedding']

        return json.dumps(embedding)
    except Exception as e:
        print(f"Error al generar embedding: {e}")
        return None

def verificar_rostro(imagen_base64, embedding_guardado):
    try:
        embedding_login_json = generar_embedding_facial(imagen_base64)
        if embedding_login_json is None:
            return False
        embedding_login = np.array(json.loads(embedding_login_json))

        embedding_almacenado = np.array(json.loads(embedding_guardado))


        distance = cosine(embedding_login, embedding_almacenado)

       
        threshold = 0.68  

        if distance < threshold:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al verificar rostro: {e}")
        return False