"""
Modelos del Sistema GoQuiz
Este módulo contiene todas las clases que representan las entidades del dominio,
manteniendo un nivel elevado de orden y aplicando herencia correcta cuando es necesario.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List, Dict, Any
import hashlib


# ============================================================================
# CLASE BASE: USUARIO
# ============================================================================

class Usuario(ABC):
    """
    Clase base abstracta que representa un usuario del sistema.
    Aplica el principio de abstracción para definir la estructura común
    de todos los tipos de usuarios.
    """
    
    def __init__(self, id_usuario: Optional[int], email: str, password: str):
        """
        Inicializa un usuario base.
        
        Args:
            id_usuario: Identificador único del usuario (None si es nuevo)
            email: Correo electrónico del usuario
            password: Contraseña en texto plano (se encriptará)
        """
        self._id = id_usuario
        self._email = email
        self._password_hash = self._encriptar_password(password)
        self._fecha_registro = datetime.now()
    
    @property
    def id(self) -> Optional[int]:
        """Retorna el ID del usuario"""
        return self._id
    
    @id.setter
    def id(self, valor: int):
        """Establece el ID del usuario"""
        self._id = valor
    
    @property
    def email(self) -> str:
        """Retorna el email del usuario"""
        return self._email
    
    @email.setter
    def email(self, valor: str):
        """Establece el email del usuario"""
        self._email = valor
    
    @property
    def password_hash(self) -> str:
        """Retorna el hash de la contraseña"""
        return self._password_hash
    
    def verificar_password(self, password: str) -> bool:
        """
        Verifica si una contraseña coincide con la almacenada.
        
        Args:
            password: Contraseña en texto plano a verificar
            
        Returns:
            True si la contraseña coincide, False en caso contrario
        """
        return self._password_hash == self._encriptar_password(password)
    
    def cambiar_password(self, nueva_password: str):
        """
        Cambia la contraseña del usuario.
        
        Args:
            nueva_password: Nueva contraseña en texto plano
        """
        self._password_hash = self._encriptar_password(nueva_password)
    
    @staticmethod
    def _encriptar_password(password: str) -> str:
        """
        Encripta una contraseña usando SHA-256.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash SHA-256 de la contraseña
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @abstractmethod
    def obtener_tipo(self) -> str:
        """
        Retorna el tipo de usuario.
        Debe ser implementado por las clases hijas.
        
        Returns:
            String que identifica el tipo de usuario
        """
        pass
    
    def __str__(self) -> str:
        """Representación en string del usuario"""
        return f"{self.__class__.__name__}(id={self._id}, email={self._email})"
    
    def __repr__(self) -> str:
        """Representación oficial del usuario"""
        return self.__str__()


# ============================================================================
# CLASES DERIVADAS: DOCENTE Y JUGADOR
# ============================================================================

class Docente(Usuario):
    """
    Clase que representa un docente en el sistema.
    Hereda de Usuario y agrega funcionalidades específicas de docentes.
    """
    
    def __init__(self, id_docente: Optional[int], correo: str, password: str,
                 nombres: str, apellidos: str, rostro: Optional[bytes] = None):
        """
        Inicializa un docente.
        
        Args:
            id_docente: Identificador único del docente
            correo: Correo electrónico del docente
            password: Contraseña en texto plano
            nombres: Nombres del docente
            apellidos: Apellidos del docente
            rostro: Datos biométricos (opcional, actualmente no se usa)
        """
        super().__init__(id_docente, correo, password)
        self._nombres = nombres
        self._apellidos = apellidos
        self._rostro = rostro  # Mantenido por compatibilidad, no se usa
    
    @property
    def id_docente(self) -> Optional[int]:
        """Retorna el ID del docente"""
        return self._id
    
    @property
    def nombres(self) -> str:
        """Retorna los nombres del docente"""
        return self._nombres
    
    @nombres.setter
    def nombres(self, valor: str):
        """Establece los nombres del docente"""
        self._nombres = valor
    
    @property
    def apellidos(self) -> str:
        """Retorna los apellidos del docente"""
        return self._apellidos
    
    @apellidos.setter
    def apellidos(self, valor: str):
        """Establece los apellidos del docente"""
        self._apellidos = valor
    
    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del docente"""
        return f"{self._nombres} {self._apellidos}"
    
    def obtener_tipo(self) -> str:
        """Retorna el tipo de usuario como 'docente'"""
        return 'docente'
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el docente a un diccionario.
        
        Returns:
            Diccionario con los datos del docente
        """
        return {
            'id_docente': self._id,
            'correo': self._email,
            'nombres': self._nombres,
            'apellidos': self._apellidos,
            'nombre_completo': self.nombre_completo
        }


class Jugador(Usuario):
    """
    Clase que representa un jugador en el sistema.
    Hereda de Usuario y agrega funcionalidades específicas de jugadores.
    """
    
    def __init__(self, id_jugador: Optional[int], email: str, password: str):
        """
        Inicializa un jugador.
        
        Args:
            id_jugador: Identificador único del jugador
            email: Correo electrónico del jugador
            password: Contraseña en texto plano
        """
        super().__init__(id_jugador, email, password)
        self._puntos_recompensa = 0
    
    @property
    def id_jugador(self) -> Optional[int]:
        """Retorna el ID del jugador"""
        return self._id
    
    @property
    def puntos_recompensa(self) -> int:
        """Retorna los puntos de recompensa acumulados"""
        return self._puntos_recompensa
    
    @puntos_recompensa.setter
    def puntos_recompensa(self, valor: int):
        """Establece los puntos de recompensa (máximo 1000)"""
        self._puntos_recompensa = min(max(0, valor), 1000)
    
    def agregar_puntos_recompensa(self, puntos: int):
        """
        Agrega puntos de recompensa al jugador.
        
        Args:
            puntos: Puntos a agregar
        """
        nuevo_total = self._puntos_recompensa + puntos
        self.puntos_recompensa = nuevo_total
    
    def obtener_tipo(self) -> str:
        """Retorna el tipo de usuario como 'jugador'"""
        return 'jugador'
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el jugador a un diccionario.
        
        Returns:
            Diccionario con los datos del jugador
        """
        return {
            'id_jugador': self._id,
            'email': self._email,
            'puntos_recompensa': self._puntos_recompensa
        }


# ============================================================================
# CLASE: CUESTIONARIO
# ============================================================================

class Cuestionario:
    """
    Clase que representa un cuestionario en el sistema.
    Encapsula toda la información y funcionalidades relacionadas con un cuestionario.
    """
    
    ESTADO_PUBLICO = 'P'
    ESTADO_PRIVADO = 'R'
    TIPO_INDIVIDUAL = 'I'
    TIPO_GRUPAL = 'G'
    ESTADO_JUEGO_SIN_INICIAR = 'SL'
    ESTADO_JUEGO_INICIADO = 'IN'
    ESTADO_JUEGO_FINALIZADO = 'FN'
    
    def __init__(self, id_cuestionario: Optional[int], nombre: str,
                 id_docente: int, tipo_cuestionario: str = TIPO_INDIVIDUAL,
                 descripcion: Optional[str] = None, estado: str = ESTADO_PUBLICO,
                 pin: Optional[str] = None, imagen_url: Optional[str] = None,
                 estado_juego: str = ESTADO_JUEGO_SIN_INICIAR):
        """
        Inicializa un cuestionario.
        
        Args:
            id_cuestionario: Identificador único del cuestionario
            nombre: Nombre del cuestionario
            id_docente: ID del docente propietario
            tipo_cuestionario: 'I' para individual, 'G' para grupal
            descripcion: Descripción del cuestionario (opcional)
            estado: 'P' para público, 'R' para privado
            pin: PIN de acceso al cuestionario
            imagen_url: URL de la imagen del cuestionario (opcional)
            estado_juego: Estado del juego ('SL', 'IN', 'FN')
        """
        self._id = id_cuestionario
        self._nombre = nombre
        self._id_docente = id_docente
        self._tipo_cuestionario = tipo_cuestionario
        self._descripcion = descripcion
        self._estado = estado
        self._pin = pin
        self._imagen_url = imagen_url
        self._estado_juego = estado_juego
        self._fecha_creacion = datetime.now()
        self._preguntas: List['Pregunta'] = []
    
    @property
    def id_cuestionario(self) -> Optional[int]:
        """Retorna el ID del cuestionario"""
        return self._id
    
    @property
    def nombre(self) -> str:
        """Retorna el nombre del cuestionario"""
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str):
        """Establece el nombre del cuestionario"""
        if not valor or len(valor.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        if len(valor) > 200:
            raise ValueError("El nombre no puede exceder 200 caracteres")
        self._nombre = valor.strip()
    
    @property
    def id_docente(self) -> int:
        """Retorna el ID del docente propietario"""
        return self._id_docente
    
    @property
    def tipo_cuestionario(self) -> str:
        """Retorna el tipo de cuestionario"""
        return self._tipo_cuestionario
    
    @tipo_cuestionario.setter
    def tipo_cuestionario(self, valor: str):
        """Establece el tipo de cuestionario"""
        if valor not in [self.TIPO_INDIVIDUAL, self.TIPO_GRUPAL]:
            raise ValueError("Tipo de cuestionario inválido")
        self._tipo_cuestionario = valor
    
    @property
    def descripcion(self) -> Optional[str]:
        """Retorna la descripción del cuestionario"""
        return self._descripcion
    
    @descripcion.setter
    def descripcion(self, valor: Optional[str]):
        """Establece la descripción del cuestionario"""
        if valor and len(valor) > 1000:
            raise ValueError("La descripción no puede exceder 1000 caracteres")
        self._descripcion = valor
    
    @property
    def estado(self) -> str:
        """Retorna el estado del cuestionario"""
        return self._estado
    
    @estado.setter
    def estado(self, valor: str):
        """Establece el estado del cuestionario"""
        if valor not in [self.ESTADO_PUBLICO, self.ESTADO_PRIVADO]:
            raise ValueError("Estado inválido")
        self._estado = valor
    
    @property
    def pin(self) -> Optional[str]:
        """Retorna el PIN del cuestionario"""
        return self._pin
    
    @property
    def imagen_url(self) -> Optional[str]:
        """Retorna la URL de la imagen"""
        return self._imagen_url
    
    @imagen_url.setter
    def imagen_url(self, valor: Optional[str]):
        """Establece la URL de la imagen"""
        self._imagen_url = valor
    
    @property
    def estado_juego(self) -> str:
        """Retorna el estado del juego"""
        return self._estado_juego
    
    @estado_juego.setter
    def estado_juego(self, valor: str):
        """Establece el estado del juego"""
        if valor not in [self.ESTADO_JUEGO_SIN_INICIAR, self.ESTADO_JUEGO_INICIADO,
                         self.ESTADO_JUEGO_FINALIZADO]:
            raise ValueError("Estado de juego inválido")
        self._estado_juego = valor
    
    @property
    def es_individual(self) -> bool:
        """Retorna True si el cuestionario es individual"""
        return self._tipo_cuestionario == self.TIPO_INDIVIDUAL
    
    @property
    def es_grupal(self) -> bool:
        """Retorna True si el cuestionario es grupal"""
        return self._tipo_cuestionario == self.TIPO_GRUPAL
    
    @property
    def es_publico(self) -> bool:
        """Retorna True si el cuestionario es público"""
        return self._estado == self.ESTADO_PUBLICO
    
    @property
    def preguntas(self) -> List['Pregunta']:
        """Retorna la lista de preguntas"""
        return self._preguntas.copy()
    
    def agregar_pregunta(self, pregunta: 'Pregunta'):
        """
        Agrega una pregunta al cuestionario.
        
        Args:
            pregunta: Instancia de Pregunta a agregar
        """
        if len(self._preguntas) >= 50:
            raise ValueError("No se pueden tener más de 50 preguntas")
        self._preguntas.append(pregunta)
    
    def eliminar_pregunta(self, id_pregunta: int):
        """
        Elimina una pregunta del cuestionario.
        
        Args:
            id_pregunta: ID de la pregunta a eliminar
        """
        self._preguntas = [p for p in self._preguntas if p.id_pregunta != id_pregunta]
    
    def obtener_pregunta(self, id_pregunta: int) -> Optional['Pregunta']:
        """
        Obtiene una pregunta por su ID.
        
        Args:
            id_pregunta: ID de la pregunta
            
        Returns:
            Instancia de Pregunta o None si no se encuentra
        """
        for pregunta in self._preguntas:
            if pregunta.id_pregunta == id_pregunta:
                return pregunta
        return None
    
    def validar(self) -> tuple[bool, Optional[str]]:
        """
        Valida que el cuestionario tenga todos los datos necesarios.
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not self._nombre or len(self._nombre.strip()) < 3:
            return False, "El nombre del cuestionario debe tener al menos 3 caracteres"
        
        if self._tipo_cuestionario not in [self.TIPO_INDIVIDUAL, self.TIPO_GRUPAL]:
            return False, "Tipo de cuestionario inválido"
        
        if len(self._preguntas) == 0:
            return False, "Debe agregar al menos una pregunta"
        
        if len(self._preguntas) > 50:
            return False, "No se pueden tener más de 50 preguntas"
        
        return True, None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el cuestionario a un diccionario.
        
        Returns:
            Diccionario con los datos del cuestionario
        """
        return {
            'id_cuestionario': self._id,
            'nombre': self._nombre,
            'id_docente': self._id_docente,
            'tipo_cuestionario': self._tipo_cuestionario,
            'descripcion': self._descripcion,
            'estado': self._estado,
            'pin': self._pin,
            'imagen_url': self._imagen_url,
            'estado_juego': self._estado_juego,
            'preguntas': [p.to_dict() for p in self._preguntas]
        }


# ============================================================================
# CLASE: PREGUNTA
# ============================================================================

class Pregunta:
    """
    Clase que representa una pregunta dentro de un cuestionario.
    Encapsula la información y funcionalidades de una pregunta.
    """
    
    TIPO_VERDADERO_FALSO = 'VF'
    TIPO_ALTERNATIVA = 'ALT'
    
    def __init__(self, id_pregunta: Optional[int], pregunta: str,
                 id_cuestionario: int, tipo_pregunta: str = TIPO_ALTERNATIVA,
                 puntaje: int = 100, tiempo_respuesta: int = 30):
        """
        Inicializa una pregunta.
        
        Args:
            id_pregunta: Identificador único de la pregunta
            pregunta: Texto de la pregunta
            id_cuestionario: ID del cuestionario al que pertenece
            tipo_pregunta: 'VF' para verdadero/falso, 'ALT' para alternativa múltiple
            puntaje: Puntos que vale la pregunta (1-1000)
            tiempo_respuesta: Tiempo en segundos para responder (2-300)
        """
        self._id = id_pregunta
        self._pregunta = pregunta
        self._id_cuestionario = id_cuestionario
        self._tipo_pregunta = tipo_pregunta
        self._puntaje = puntaje
        self._tiempo_respuesta = tiempo_respuesta
        self._alternativas: List['Alternativa'] = []
    
    @property
    def id_pregunta(self) -> Optional[int]:
        """Retorna el ID de la pregunta"""
        return self._id
    
    @property
    def pregunta(self) -> str:
        """Retorna el texto de la pregunta"""
        return self._pregunta
    
    @pregunta.setter
    def pregunta(self, valor: str):
        """Establece el texto de la pregunta"""
        if not valor or len(valor.strip()) < 5:
            raise ValueError("La pregunta debe tener al menos 5 caracteres")
        if len(valor) > 500:
            raise ValueError("La pregunta no puede exceder 500 caracteres")
        self._pregunta = valor.strip()
    
    @property
    def id_cuestionario(self) -> int:
        """Retorna el ID del cuestionario"""
        return self._id_cuestionario
    
    @property
    def tipo_pregunta(self) -> str:
        """Retorna el tipo de pregunta"""
        return self._tipo_pregunta
    
    @tipo_pregunta.setter
    def tipo_pregunta(self, valor: str):
        """Establece el tipo de pregunta"""
        if valor not in [self.TIPO_VERDADERO_FALSO, self.TIPO_ALTERNATIVA]:
            raise ValueError("Tipo de pregunta inválido")
        self._tipo_pregunta = valor
    
    @property
    def puntaje(self) -> int:
        """Retorna el puntaje de la pregunta"""
        return self._puntaje
    
    @puntaje.setter
    def puntaje(self, valor: int):
        """Establece el puntaje de la pregunta"""
        if not (1 <= valor <= 1000):
            raise ValueError("El puntaje debe estar entre 1 y 1000")
        self._puntaje = valor
    
    @property
    def tiempo_respuesta(self) -> int:
        """Retorna el tiempo de respuesta en segundos"""
        return self._tiempo_respuesta
    
    @tiempo_respuesta.setter
    def tiempo_respuesta(self, valor: int):
        """Establece el tiempo de respuesta en segundos"""
        if not (2 <= valor <= 300):
            raise ValueError("El tiempo debe estar entre 2 y 300 segundos")
        self._tiempo_respuesta = valor
    
    @property
    def alternativas(self) -> List['Alternativa']:
        """Retorna la lista de alternativas"""
        return self._alternativas.copy()
    
    @property
    def es_verdadero_falso(self) -> bool:
        """Retorna True si es pregunta de verdadero/falso"""
        return self._tipo_pregunta == self.TIPO_VERDADERO_FALSO
    
    @property
    def es_alternativa_multiple(self) -> bool:
        """Retorna True si es pregunta de alternativa múltiple"""
        return self._tipo_pregunta == self.TIPO_ALTERNATIVA
    
    def agregar_alternativa(self, alternativa: 'Alternativa'):
        """
        Agrega una alternativa a la pregunta.
        
        Args:
            alternativa: Instancia de Alternativa a agregar
        """
        if self.es_verdadero_falso and len(self._alternativas) >= 2:
            raise ValueError("Las preguntas VF solo pueden tener 2 alternativas")
        if self.es_alternativa_multiple and len(self._alternativas) >= 6:
            raise ValueError("Las preguntas ALT no pueden tener más de 6 alternativas")
        self._alternativas.append(alternativa)
    
    def eliminar_alternativa(self, id_alternativa: int):
        """
        Elimina una alternativa de la pregunta.
        
        Args:
            id_alternativa: ID de la alternativa a eliminar
        """
        self._alternativas = [a for a in self._alternativas 
                             if a.id_alternativa != id_alternativa]
    
    def obtener_alternativa_correcta(self) -> Optional['Alternativa']:
        """
        Obtiene la alternativa correcta de la pregunta.
        
        Returns:
            Instancia de Alternativa correcta o None si no hay
        """
        for alternativa in self._alternativas:
            if alternativa.es_correcta:
                return alternativa
        return None
    
    def validar(self) -> tuple[bool, Optional[str]]:
        """
        Valida que la pregunta tenga todos los datos necesarios.
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not self._pregunta or len(self._pregunta.strip()) < 5:
            return False, "La pregunta debe tener al menos 5 caracteres"
        
        if self._tipo_pregunta not in [self.TIPO_VERDADERO_FALSO, self.TIPO_ALTERNATIVA]:
            return False, "Tipo de pregunta inválido"
        
        if self.es_verdadero_falso:
            if len(self._alternativas) != 2:
                return False, "Las preguntas VF deben tener exactamente 2 alternativas"
            # Verificar que tenga una correcta
            if not any(a.es_correcta for a in self._alternativas):
                return False, "Debe haber una alternativa correcta"
        else:
            if len(self._alternativas) < 2:
                return False, "Debe tener al menos 2 alternativas"
            if len(self._alternativas) > 6:
                return False, "No puede tener más de 6 alternativas"
            # Verificar que tenga una correcta
            if not any(a.es_correcta for a in self._alternativas):
                return False, "Debe haber una alternativa correcta"
        
        return True, None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la pregunta a un diccionario.
        
        Returns:
            Diccionario con los datos de la pregunta
        """
        return {
            'id_pregunta': self._id,
            'pregunta': self._pregunta,
            'id_cuestionario': self._id_cuestionario,
            'tipo_pregunta': self._tipo_pregunta,
            'puntaje': self._puntaje,
            'tiempo_respuesta': self._tiempo_respuesta,
            'alternativas': [a.to_dict() for a in self._alternativas]
        }


# ============================================================================
# CLASE: ALTERNATIVA
# ============================================================================

class Alternativa:
    """
    Clase que representa una alternativa de respuesta para una pregunta.
    Encapsula la información de una opción de respuesta.
    """
    
    def __init__(self, id_alternativa: Optional[int], respuesta: str,
                 id_pregunta: int, es_correcta: bool = False):
        """
        Inicializa una alternativa.
        
        Args:
            id_alternativa: Identificador único de la alternativa
            respuesta: Texto de la alternativa
            id_pregunta: ID de la pregunta a la que pertenece
            es_correcta: True si es la respuesta correcta
        """
        self._id = id_alternativa
        self._respuesta = respuesta
        self._id_pregunta = id_pregunta
        self._es_correcta = es_correcta
    
    @property
    def id_alternativa(self) -> Optional[int]:
        """Retorna el ID de la alternativa"""
        return self._id
    
    @property
    def respuesta(self) -> str:
        """Retorna el texto de la alternativa"""
        return self._respuesta
    
    @respuesta.setter
    def respuesta(self, valor: str):
        """Establece el texto de la alternativa"""
        if not valor or len(valor.strip()) == 0:
            raise ValueError("La alternativa no puede estar vacía")
        self._respuesta = valor.strip()
    
    @property
    def id_pregunta(self) -> int:
        """Retorna el ID de la pregunta"""
        return self._id_pregunta
    
    @property
    def es_correcta(self) -> bool:
        """Retorna True si es la respuesta correcta"""
        return self._es_correcta
    
    @es_correcta.setter
    def es_correcta(self, valor: bool):
        """Establece si es la respuesta correcta"""
        self._es_correcta = valor
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la alternativa a un diccionario.
        
        Returns:
            Diccionario con los datos de la alternativa
        """
        return {
            'id_alternativa': self._id,
            'respuesta': self._respuesta,
            'id_pregunta': self._id_pregunta,
            'es_correcta': self._es_correcta,
            'estado_alternativa': 1 if self._es_correcta else 0
        }


# ============================================================================
# CLASE: PARTICIPANTE (JUGADOR_CUESTIONARIO)
# ============================================================================

class Participante:
    """
    Clase que representa la participación de un jugador en un cuestionario.
    Relaciona un jugador (o participante anónimo) con un cuestionario específico.
    """
    
    def __init__(self, id_jugador_cuestionario: Optional[int],
                 id_cuestionario: int, alias: str,
                 id_jugador: Optional[int] = None, puntaje: float = 0.0):
        """
        Inicializa un participante.
        
        Args:
            id_jugador_cuestionario: Identificador único de la participación
            id_cuestionario: ID del cuestionario
            alias: Alias del participante
            id_jugador: ID del jugador registrado (opcional, puede ser anónimo)
            puntaje: Puntaje acumulado del participante
        """
        self._id = id_jugador_cuestionario
        self._id_cuestionario = id_cuestionario
        self._alias = alias
        self._id_jugador = id_jugador
        self._puntaje = puntaje
        self._fecha_participacion = datetime.now()
    
    @property
    def id_jugador_cuestionario(self) -> Optional[int]:
        """Retorna el ID de la participación"""
        return self._id
    
    @property
    def id_cuestionario(self) -> int:
        """Retorna el ID del cuestionario"""
        return self._id_cuestionario
    
    @property
    def alias(self) -> str:
        """Retorna el alias del participante"""
        return self._alias
    
    @alias.setter
    def alias(self, valor: str):
        """Establece el alias del participante"""
        if not valor or len(valor.strip()) < 2:
            raise ValueError("El alias debe tener al menos 2 caracteres")
        if len(valor) > 20:
            raise ValueError("El alias no puede exceder 20 caracteres")
        self._alias = valor.strip()
    
    @property
    def id_jugador(self) -> Optional[int]:
        """Retorna el ID del jugador registrado"""
        return self._id_jugador
    
    @id_jugador.setter
    def id_jugador(self, valor: Optional[int]):
        """Establece el ID del jugador registrado"""
        self._id_jugador = valor
    
    @property
    def puntaje(self) -> float:
        """Retorna el puntaje del participante"""
        return self._puntaje
    
    @puntaje.setter
    def puntaje(self, valor: float):
        """Establece el puntaje del participante"""
        self._puntaje = max(0.0, valor)
    
    def agregar_puntaje(self, puntos: float):
        """
        Agrega puntos al participante.
        
        Args:
            puntos: Puntos a agregar
        """
        self._puntaje += max(0.0, puntos)
    
    @property
    def es_anonimo(self) -> bool:
        """Retorna True si el participante es anónimo"""
        return self._id_jugador is None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el participante a un diccionario.
        
        Returns:
            Diccionario con los datos del participante
        """
        return {
            'id_jugador_cuestionario': self._id,
            'id_cuestionario': self._id_cuestionario,
            'alias': self._alias,
            'id_jugador': self._id_jugador,
            'puntaje': self._puntaje,
            'es_anonimo': self.es_anonimo
        }


# ============================================================================
# CLASE: GRUPO
# ============================================================================

class Grupo:
    """
    Clase que representa un grupo de participantes en un cuestionario grupal.
    Encapsula la información y funcionalidades de un grupo.
    """
    
    ESTADO_ACTIVO = 'A'
    ESTADO_DISUELTO = 'D'
    METODO_VOTACION = 'votacion'
    METODO_CONSENSO = 'consenso'
    METODO_LIDER = 'lider'
    MAX_MIEMBROS = 5
    
    def __init__(self, id_grupo: Optional[int], nombre_grupo: str,
                 id_cuestionario: int, id_lider: int,
                 metodo_evaluacion: str = METODO_VOTACION,
                 estado: str = ESTADO_ACTIVO, puntaje: float = 0.0):
        """
        Inicializa un grupo.
        
        Args:
            id_grupo: Identificador único del grupo
            nombre_grupo: Nombre del grupo
            id_cuestionario: ID del cuestionario
            id_lider: ID del participante líder (id_jugador_cuestionario)
            metodo_evaluacion: Método de evaluación ('votacion', 'consenso', 'lider')
            estado: Estado del grupo ('A' activo, 'D' disuelto)
            puntaje: Puntaje acumulado del grupo
        """
        self._id = id_grupo
        self._nombre_grupo = nombre_grupo
        self._id_cuestionario = id_cuestionario
        self._id_lider = id_lider
        self._metodo_evaluacion = metodo_evaluacion
        self._estado = estado
        self._puntaje = puntaje
        self._fecha_creacion = datetime.now()
        self._miembros: List[int] = []  # Lista de id_jugador_cuestionario
    
    @property
    def id_grupo(self) -> Optional[int]:
        """Retorna el ID del grupo"""
        return self._id
    
    @property
    def nombre_grupo(self) -> str:
        """Retorna el nombre del grupo"""
        return self._nombre_grupo
    
    @nombre_grupo.setter
    def nombre_grupo(self, valor: str):
        """Establece el nombre del grupo"""
        if not valor or len(valor.strip()) < 1:
            raise ValueError("El nombre del grupo no puede estar vacío")
        if len(valor) > 100:
            raise ValueError("El nombre del grupo no puede exceder 100 caracteres")
        self._nombre_grupo = valor.strip()
    
    @property
    def id_cuestionario(self) -> int:
        """Retorna el ID del cuestionario"""
        return self._id_cuestionario
    
    @property
    def id_lider(self) -> int:
        """Retorna el ID del líder"""
        return self._id_lider
    
    @property
    def metodo_evaluacion(self) -> str:
        """Retorna el método de evaluación"""
        return self._metodo_evaluacion
    
    @metodo_evaluacion.setter
    def metodo_evaluacion(self, valor: str):
        """Establece el método de evaluación"""
        if valor not in [self.METODO_VOTACION, self.METODO_CONSENSO, self.METODO_LIDER]:
            raise ValueError("Método de evaluación inválido")
        self._metodo_evaluacion = valor
    
    @property
    def estado(self) -> str:
        """Retorna el estado del grupo"""
        return self._estado
    
    @estado.setter
    def estado(self, valor: str):
        """Establece el estado del grupo"""
        if valor not in [self.ESTADO_ACTIVO, self.ESTADO_DISUELTO]:
            raise ValueError("Estado inválido")
        self._estado = valor
    
    @property
    def puntaje(self) -> float:
        """Retorna el puntaje del grupo"""
        return self._puntaje
    
    @puntaje.setter
    def puntaje(self, valor: float):
        """Establece el puntaje del grupo"""
        self._puntaje = max(0.0, valor)
    
    @property
    def miembros(self) -> List[int]:
        """Retorna la lista de IDs de miembros"""
        return self._miembros.copy()
    
    @property
    def num_miembros(self) -> int:
        """Retorna el número de miembros"""
        return len(self._miembros)
    
    @property
    def tiene_cupo(self) -> bool:
        """Retorna True si el grupo tiene cupo disponible"""
        return len(self._miembros) < self.MAX_MIEMBROS
    
    @property
    def es_activo(self) -> bool:
        """Retorna True si el grupo está activo"""
        return self._estado == self.ESTADO_ACTIVO
    
    def agregar_miembro(self, id_jugador_cuestionario: int):
        """
        Agrega un miembro al grupo.
        
        Args:
            id_jugador_cuestionario: ID del participante a agregar
        """
        if not self.tiene_cupo:
            raise ValueError("El grupo ya tiene el máximo de miembros")
        if id_jugador_cuestionario in self._miembros:
            raise ValueError("El participante ya es miembro del grupo")
        self._miembros.append(id_jugador_cuestionario)
    
    def eliminar_miembro(self, id_jugador_cuestionario: int):
        """
        Elimina un miembro del grupo.
        
        Args:
            id_jugador_cuestionario: ID del participante a eliminar
        """
        if id_jugador_cuestionario == self._id_lider:
            raise ValueError("No se puede eliminar al líder del grupo")
        if id_jugador_cuestionario not in self._miembros:
            raise ValueError("El participante no es miembro del grupo")
        self._miembros.remove(id_jugador_cuestionario)
    
    def es_lider(self, id_jugador_cuestionario: int) -> bool:
        """
        Verifica si un participante es el líder del grupo.
        
        Args:
            id_jugador_cuestionario: ID del participante
            
        Returns:
            True si es el líder
        """
        return id_jugador_cuestionario == self._id_lider
    
    def es_miembro(self, id_jugador_cuestionario: int) -> bool:
        """
        Verifica si un participante es miembro del grupo.
        
        Args:
            id_jugador_cuestionario: ID del participante
            
        Returns:
            True si es miembro
        """
        return id_jugador_cuestionario in self._miembros or self.es_lider(id_jugador_cuestionario)
    
    def disolver(self):
        """Disuelve el grupo (cambia su estado a disuelto)"""
        self._estado = self.ESTADO_DISUELTO
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el grupo a un diccionario.
        
        Returns:
            Diccionario con los datos del grupo
        """
        return {
            'id_grupo': self._id,
            'nombre_grupo': self._nombre_grupo,
            'id_cuestionario': self._id_cuestionario,
            'id_lider': self._id_lider,
            'metodo_evaluacion': self._metodo_evaluacion,
            'estado': self._estado,
            'puntaje': self._puntaje,
            'num_miembros': self.num_miembros,
            'miembros': self._miembros
        }


# ============================================================================
# CLASE: RECOMPENSA
# ============================================================================

class Recompensa:
    """
    Clase que representa una recompensa otorgada a un jugador.
    Encapsula la información de las recompensas del sistema.
    """
    
    TIPO_PUNTOS = 'puntos'
    TIPO_BADGE = 'badge'
    TIPO_LOGRO = 'logro'
    
    def __init__(self, id_recompensa: Optional[int], id_cuestionario: int,
                 id_jugador_cuestionario: int, puntos: int,
                 id_jugador: Optional[int] = None,
                 tipo_recompensa: str = TIPO_PUNTOS):
        """
        Inicializa una recompensa.
        
        Args:
            id_recompensa: Identificador único de la recompensa
            id_cuestionario: ID del cuestionario
            id_jugador_cuestionario: ID de la participación
            puntos: Puntos de recompensa otorgados
            id_jugador: ID del jugador registrado (opcional)
            tipo_recompensa: Tipo de recompensa ('puntos', 'badge', 'logro')
        """
        self._id = id_recompensa
        self._id_cuestionario = id_cuestionario
        self._id_jugador_cuestionario = id_jugador_cuestionario
        self._id_jugador = id_jugador
        self._puntos = puntos
        self._tipo_recompensa = tipo_recompensa
        self._fecha_recompensa = datetime.now()
    
    @property
    def id_recompensa(self) -> Optional[int]:
        """Retorna el ID de la recompensa"""
        return self._id
    
    @property
    def id_cuestionario(self) -> int:
        """Retorna el ID del cuestionario"""
        return self._id_cuestionario
    
    @property
    def id_jugador_cuestionario(self) -> int:
        """Retorna el ID de la participación"""
        return self._id_jugador_cuestionario
    
    @property
    def id_jugador(self) -> Optional[int]:
        """Retorna el ID del jugador registrado"""
        return self._id_jugador
    
    @property
    def puntos(self) -> int:
        """Retorna los puntos de recompensa"""
        return self._puntos
    
    @puntos.setter
    def puntos(self, valor: int):
        """Establece los puntos de recompensa"""
        self._puntos = max(0, valor)
    
    @property
    def tipo_recompensa(self) -> str:
        """Retorna el tipo de recompensa"""
        return self._tipo_recompensa
    
    @tipo_recompensa.setter
    def tipo_recompensa(self, valor: str):
        """Establece el tipo de recompensa"""
        if valor not in [self.TIPO_PUNTOS, self.TIPO_BADGE, self.TIPO_LOGRO]:
            raise ValueError("Tipo de recompensa inválido")
        self._tipo_recompensa = valor
    
    @property
    def fecha_recompensa(self) -> datetime:
        """Retorna la fecha de la recompensa"""
        return self._fecha_recompensa
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la recompensa a un diccionario.
        
        Returns:
            Diccionario con los datos de la recompensa
        """
        return {
            'id_recompensa': self._id,
            'id_cuestionario': self._id_cuestionario,
            'id_jugador_cuestionario': self._id_jugador_cuestionario,
            'id_jugador': self._id_jugador,
            'puntos': self._puntos,
            'tipo_recompensa': self._tipo_recompensa,
            'fecha_recompensa': self._fecha_recompensa.isoformat()
        }


# ============================================================================
# CLASE: RESPUESTA
# ============================================================================

class Respuesta:
    """
    Clase que representa una respuesta individual de un participante a una pregunta.
    Encapsula la información de las respuestas en cuestionarios individuales.
    """
    
    def __init__(self, id_respuesta: Optional[int], id_jugador_cuestionario: int,
                 id_pregunta: int, id_alternativa: int, tiempo_utilizado: int = 0):
        """
        Inicializa una respuesta.
        
        Args:
            id_respuesta: Identificador único de la respuesta
            id_jugador_cuestionario: ID de la participación
            id_pregunta: ID de la pregunta
            id_alternativa: ID de la alternativa seleccionada
            tiempo_utilizado: Tiempo utilizado para responder en segundos
        """
        self._id = id_respuesta
        self._id_jugador_cuestionario = id_jugador_cuestionario
        self._id_pregunta = id_pregunta
        self._id_alternativa = id_alternativa
        self._tiempo_utilizado = tiempo_utilizado
        self._fecha_respuesta = datetime.now()
    
    @property
    def id_respuesta(self) -> Optional[int]:
        """Retorna el ID de la respuesta"""
        return self._id
    
    @property
    def id_jugador_cuestionario(self) -> int:
        """Retorna el ID de la participación"""
        return self._id_jugador_cuestionario
    
    @property
    def id_pregunta(self) -> int:
        """Retorna el ID de la pregunta"""
        return self._id_pregunta
    
    @property
    def id_alternativa(self) -> int:
        """Retorna el ID de la alternativa seleccionada"""
        return self._id_alternativa
    
    @id_alternativa.setter
    def id_alternativa(self, valor: int):
        """Establece el ID de la alternativa seleccionada"""
        self._id_alternativa = valor
    
    @property
    def tiempo_utilizado(self) -> int:
        """Retorna el tiempo utilizado en segundos"""
        return self._tiempo_utilizado
    
    @tiempo_utilizado.setter
    def tiempo_utilizado(self, valor: int):
        """Establece el tiempo utilizado en segundos"""
        self._tiempo_utilizado = max(0, valor)
    
    @property
    def fecha_respuesta(self) -> datetime:
        """Retorna la fecha de la respuesta"""
        return self._fecha_respuesta
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la respuesta a un diccionario.
        
        Returns:
            Diccionario con los datos de la respuesta
        """
        return {
            'id_respuesta': self._id,
            'id_jugador_cuestionario': self._id_jugador_cuestionario,
            'id_pregunta': self._id_pregunta,
            'id_alternativa': self._id_alternativa,
            'tiempo_utilizado': self._tiempo_utilizado,
            'fecha_respuesta': self._fecha_respuesta.isoformat()
        }


# ============================================================================
# CLASE: RESPUESTA GRUPO
# ============================================================================

class RespuestaGrupo:
    """
    Clase que representa una respuesta de un grupo a una pregunta.
    Encapsula la información de las respuestas en cuestionarios grupales.
    """
    
    def __init__(self, id_respuesta_grupo: Optional[int], id_grupo: int,
                 id_pregunta: int, id_alternativa: int, tiempo_utilizado: int = 0):
        """
        Inicializa una respuesta de grupo.
        
        Args:
            id_respuesta_grupo: Identificador único de la respuesta
            id_grupo: ID del grupo
            id_pregunta: ID de la pregunta
            id_alternativa: ID de la alternativa seleccionada
            tiempo_utilizado: Tiempo utilizado para responder en segundos
        """
        self._id = id_respuesta_grupo
        self._id_grupo = id_grupo
        self._id_pregunta = id_pregunta
        self._id_alternativa = id_alternativa
        self._tiempo_utilizado = tiempo_utilizado
        self._fecha_respuesta = datetime.now()
    
    @property
    def id_respuesta_grupo(self) -> Optional[int]:
        """Retorna el ID de la respuesta"""
        return self._id
    
    @property
    def id_grupo(self) -> int:
        """Retorna el ID del grupo"""
        return self._id_grupo
    
    @property
    def id_pregunta(self) -> int:
        """Retorna el ID de la pregunta"""
        return self._id_pregunta
    
    @property
    def id_alternativa(self) -> int:
        """Retorna el ID de la alternativa seleccionada"""
        return self._id_alternativa
    
    @id_alternativa.setter
    def id_alternativa(self, valor: int):
        """Establece el ID de la alternativa seleccionada"""
        self._id_alternativa = valor
    
    @property
    def tiempo_utilizado(self) -> int:
        """Retorna el tiempo utilizado en segundos"""
        return self._tiempo_utilizado
    
    @tiempo_utilizado.setter
    def tiempo_utilizado(self, valor: int):
        """Establece el tiempo utilizado en segundos"""
        self._tiempo_utilizado = max(0, valor)
    
    @property
    def fecha_respuesta(self) -> datetime:
        """Retorna la fecha de la respuesta"""
        return self._fecha_respuesta
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la respuesta de grupo a un diccionario.
        
        Returns:
            Diccionario con los datos de la respuesta
        """
        return {
            'id_respuesta_grupo': self._id,
            'id_grupo': self._id_grupo,
            'id_pregunta': self._id_pregunta,
            'id_alternativa': self._id_alternativa,
            'tiempo_utilizado': self._tiempo_utilizado,
            'fecha_respuesta': self._fecha_respuesta.isoformat()
        }










