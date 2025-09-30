import json
from collections import deque

class AutomataAFD:
    """
    Clase que representa un Autómata Finito Determinista (AFD).

    Esta clase es un modelo matemático que simula el comportamiento de un AFD.
    Contiene todos sus componentes (estados, alfabeto, transiciones, etc.) y los
    métodos necesarios para definirlo, validarlo y realizar simulaciones.
    """
    def __init__(self):
        """
        Inicializa un nuevo objeto AutomataAFD con sus componentes vacíos.
        """
        self.estados = set()
        self.alfabeto = set()
        self.transiciones = {}
        self.estado_inicial = None
        self.estados_aceptacion = set()

    def definir_automata(self, estados, alfabeto, transiciones, estado_inicial, estados_aceptacion):
        """
        Define los cinco componentes de un AFD y realiza validaciones iniciales.

        Args:
            estados (list[str]): Una lista de cadenas que representan los estados.
            alfabeto (list[str]): Una lista de cadenas que representan los símbolos del alfabeto.
            transiciones (list[tuple]): Una lista de tuplas, donde cada tupla representa
                                        una transición en el formato (origen, simbolo, destino).
            estado_inicial (str): La cadena que representa el estado inicial.
            estados_aceptacion (list[str]): Una lista de cadenas que representan los estados de aceptación.

        Raises:
            TypeError: Si los componentes no son del tipo esperado (cadenas de texto).
            ValueError: Si hay inconsistencias lógicas (ej. estado inicial no en estados,
                        símbolo '*' en el alfabeto, etc.).
        """
        if not all(isinstance(e, str) for e in estados):
            raise TypeError("Los estados deben ser cadenas de texto.")
        if not all(isinstance(s, str) for s in alfabeto):
            raise TypeError("Los símbolos del alfabeto deben ser cadenas de texto.")
        if not isinstance(estado_inicial, str):
            raise TypeError("El estado inicial debe ser una cadena de texto.")
        if not all(isinstance(e, str) for e in estados_aceptacion):
            raise TypeError("Los estados de aceptación deben ser cadenas de texto.")

        if estado_inicial not in estados:
            raise ValueError("El estado inicial debe ser uno de los estados definidos.")
        if not set(estados_aceptacion).issubset(set(estados)):
            raise ValueError("Todos los estados de aceptación deben ser parte del conjunto de estados.")
        
        if '*' in alfabeto:
            raise ValueError("El símbolo '*' está reservado para la cadena vacía y no puede ser parte del alfabeto.")

        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = set(estados_aceptacion)
        self.transiciones = self._crear_tabla_transiciones(transiciones)

    def _crear_tabla_transiciones(self, lista_transiciones):
        """
        Método auxiliar para construir la tabla de transiciones a partir de una lista.

        Este método convierte una lista de tuplas de transición en un diccionario anidado
        para un acceso eficiente, validando cada transición en el proceso.

        Args:
            lista_transiciones (list[tuple]): Lista de tuplas (origen, simbolo, destino).

        Returns:
            dict: Un diccionario que representa la tabla de transiciones.
                  Formato: {estado_origen: {simbolo: estado_destino}}.

        Raises:
            ValueError: Si un estado o símbolo en una transición no existe, o si se define
                        una transición duplicada para un mismo estado y símbolo.
        """
        tabla = {}
        for origen, simbolo, destino in lista_transiciones:
            if origen not in self.estados:
                raise ValueError(f"Estado de origen '{origen}' no definido.")
            if simbolo not in self.alfabeto:
                raise ValueError(f"Símbolo de transición '{simbolo}' no definido en el alfabeto.")
            if destino not in self.estados:
                raise ValueError(f"Estado de destino '{destino}' no definido.")
            
            if origen not in tabla:
                tabla[origen] = {}
            if simbolo in tabla[origen]:
                raise ValueError(f"Transición duplicada para el estado '{origen}' con el símbolo '{simbolo}'.")
            tabla[origen][simbolo] = destino
        return tabla

    def evaluar_cadena(self, cadena):
        """
        Procesa una cadena de entrada y determina si es aceptada por el AFD.

        Simula el recorrido del autómata estado por estado para la cadena dada.

        Args:
            cadena (str): La cadena de símbolos a evaluar. Se usa '*' para la cadena vacía.

        Returns:
            tuple: Una tupla con tres elementos:
                   - str: "ACEPTADA" o "RECHAZADA".
                   - list: El historial del recorrido, una lista de tuplas (estado, simbolo).
                   - str: Un mensaje descriptivo del resultado o del error encontrado.
        """
        if cadena == '*':
            if self.estado_inicial in self.estados_aceptacion:
                return "ACEPTADA", [(self.estado_inicial, None)], "La cadena vacía es aceptada porque el estado inicial es de aceptación."
            else:
                return "RECHAZADA", [(self.estado_inicial, None)], "La cadena vacía es rechazada porque el estado inicial no es de aceptación."
        
        estado_actual = self.estado_inicial
        historial_recorrido = [(estado_actual, None)]

        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                return "RECHAZADA", historial_recorrido, f"Error: El símbolo '{simbolo}' no pertenece al alfabeto."
            
            try:
                estado_actual = self.transiciones[estado_actual][simbolo]
                historial_recorrido.append((estado_actual, simbolo))
            except KeyError:
                return "RECHAZADA", historial_recorrido, f"Proceso detenido: No hay transición definida desde el estado '{estado_actual}' con el símbolo '{simbolo}'."
        
        if estado_actual in self.estados_aceptacion:
            return "ACEPTADA", historial_recorrido, f"Proceso finalizado. El estado final es '{estado_actual}', que es un estado de aceptación."
        else:
            return "RECHAZADA", historial_recorrido, f"Proceso finalizado. El estado final es '{estado_actual}', que NO es un estado de aceptación."

    def generar_cadenas_lenguaje(self, num_cadenas=10):
        """
        Genera las primeras 'num_cadenas' que pertenecen al lenguaje,
        utilizando un algoritmo de búsqueda en anchura (BFS) para encontrar las más cortas.

        Args:
            num_cadenas (int, optional): El número máximo de cadenas a generar.
                                         Por defecto es 10.

        Returns:
            list[str]: Una lista de cadenas aceptadas por el autómata, ordenadas por
                       longitud (de menor a mayor). Incluye '*' si la cadena vacía es válida.
        """
        if not self.estado_inicial:
            return []

        cadenas_validas = []
        
        if self.estado_inicial in self.estados_aceptacion:
            cadenas_validas.append("*")
        
        cola = deque([(self.estado_inicial, "")])
        visitados = set([(self.estado_inicial, "")])
        
        while cola and len(cadenas_validas) < num_cadenas:
            estado_actual, cadena = cola.popleft()

            if estado_actual in self.transiciones:
                for simbolo, estado_siguiente in sorted(self.transiciones[estado_actual].items()):
                    nueva_cadena = cadena + simbolo
                    if (estado_siguiente, nueva_cadena) not in visitados:
                        visitados.add((estado_siguiente, nueva_cadena))
                        cola.append((estado_siguiente, nueva_cadena))
                        
                        if estado_siguiente in self.estados_aceptacion and nueva_cadena != "":
                            cadenas_validas.append(nueva_cadena)
        
        return cadenas_validas

    def guardar_a_json(self, nombre_archivo):
        """
        Guarda la definición del autómata en un archivo JSON.

        Args:
            nombre_archivo (str): La ruta completa del archivo donde se guardará el autómata.

        Returns:
            tuple: Una tupla (bool, str) donde el primer elemento indica si la operación
                   fue exitosa y el segundo es un mensaje de estado.
        """
        data = {
            "estados": list(self.estados),
            "alfabeto": list(self.alfabeto),
            "estado_inicial": self.estado_inicial,
            "estados_aceptacion": list(self.estados_aceptacion),
            "transiciones": self.transiciones
        }
        try:
            with open(nombre_archivo, 'w') as f:
                json.dump(data, f, indent=4)
            return True, "Autómata guardado exitosamente."
        except Exception as e:
            return False, f"Error al guardar el archivo: {e}"

    def cargar_de_json(self, nombre_archivo):
        """
        Carga la definición de un autómata desde un archivo JSON.

        Actualiza el estado interno del objeto con los datos del archivo.

        Args:
            nombre_archivo (str): La ruta del archivo JSON a cargar.

        Returns:
            tuple: Una tupla (bool, result) donde:
                   - bool: True si la carga fue exitosa, False en caso contrario.
                   - result: El diccionario con los datos cargados si fue exitoso, o un
                             mensaje de error (str) si falló.
        """
        try:
            with open(nombre_archivo, 'r') as f:
                data = json.load(f)
            
            # Asignación de los datos al objeto (actualización del estado interno)
            self.estados = set(data.get("estados", []))
            self.alfabeto = set(data.get("alfabeto", []))
            self.estado_inicial = data.get("estado_inicial")
            self.estados_aceptacion = set(data.get("estados_aceptacion", []))
            self.transiciones = data.get("transiciones", {})

            # Retorna True junto con el diccionario de datos para que la GUI se actualice.
            return True, data
        except FileNotFoundError:
            return False, f"Error: El archivo '{nombre_archivo}' no fue encontrado."
        except json.JSONDecodeError:
            return False, f"Error: El archivo '{nombre_archivo}' tiene un formato JSON inválido."
        except KeyError as e:
            return False, f"Error: Archivo JSON incompleto. Falta la clave {e}."