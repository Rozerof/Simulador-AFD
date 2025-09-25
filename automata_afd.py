import json
from collections import deque

class AutomataAFD:
    """
    Clase que representa un Autómata Finito Determinista (AFD).
    
    Esta clase es un modelo matemático que simula el comportamiento de un AFD.
    Contiene todos sus componentes (estados, alfabeto, etc.) y los métodos
    necesarios para realizar simulaciones, como evaluar cadenas o generar el lenguaje.
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
        Define los cinco componentes de un AFD y realiza validaciones para asegurar
        que la definición sea correcta y válida.

        Args:
            estados (list): Una lista de cadenas de texto que representan los estados.
            alfabeto (list): Una lista de cadenas de texto que representan los símbolos del alfabeto.
            transiciones (list): Una lista de tuplas (estado_origen, simbolo, estado_destino).
            estado_inicial (str): El estado por donde comienza la simulación.
            estados_aceptacion (list): Una lista de estados que, si se alcanzan al
                                       final de una cadena, la hacen "aceptada".
        
        Raises:
            TypeError: Si alguno de los componentes no es del tipo de dato esperado.
            ValueError: Si la definición del autómata no cumple las reglas de un AFD.
        """
        if not all(isinstance(e, str) for e in estados):
            raise TypeError("Los estados deben ser cadenas de texto.")
        if not all(isinstance(s, str) for s in alfabeto):
            raise TypeError("Los símbolos del alfabeto deben ser cadenas de texto.")
        if not isinstance(estado_inicial, str):
            raise TypeError("El estado inicial debe ser una cadena de texto.")
        if not all(isinstance(e, str) for e in estados_aceptacion):
            raise TypeError("Los estados de aceptación deben ser cadenas de texto.")

        # Validación de que el estado inicial y de aceptación sean parte de los estados definidos.
        if estado_inicial not in estados:
            raise ValueError("El estado inicial debe ser uno de los estados definidos.")
        if not set(estados_aceptacion).issubset(set(estados)):
            raise ValueError("Todos los estados de aceptación deben ser parte del conjunto de estados.")
        
        # El símbolo '*' está reservado para la cadena vacía y no puede ser parte del alfabeto.
        if '*' in alfabeto:
            raise ValueError("El símbolo '*' está reservado para la cadena vacía y no puede ser parte del alfabeto.")

        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = set(estados_aceptacion)
        # Se construye una tabla de transiciones para un acceso más rápido.
        self.transiciones = self._crear_tabla_transiciones(transiciones)

    def _crear_tabla_transiciones(self, lista_transiciones):
        """
        Método auxiliar para construir la tabla de transiciones a partir de una lista de tuplas.
        Esta tabla permite buscar el siguiente estado de forma eficiente usando diccionarios anidados.
        
        Args:
            lista_transiciones (list): Una lista de tuplas (estado_origen, simbolo, estado_destino).
        
        Returns:
            dict: Un diccionario anidado que representa la tabla de transiciones.
        """
        tabla = {}
        for origen, simbolo, destino in lista_transiciones:
            # Validar que los estados y símbolos existan en el autómata.
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
        Procesa una cadena de entrada, moviéndose de estado en estado, y determina
        si es aceptada o rechazada por el AFD.

        Args:
            cadena (str): La cadena que se va a evaluar. Usa '*' para la cadena vacía.
        
        Returns:
            tuple: Una tupla con (resultado, recorrido, mensaje).
                   - resultado (str): "ACEPTADA" o "RECHAZADA".
                   - recorrido (list): Una lista de tuplas que muestra la ruta de la simulación.
                   - mensaje (str): Una descripción del resultado de la evaluación.
        """
        # Caso especial para la cadena vacía
        if cadena == '*':
            if self.estado_inicial in self.estados_aceptacion:
                return "ACEPTADA", [(self.estado_inicial, None)], "La cadena vacía es aceptada porque el estado inicial es de aceptación."
            else:
                return "RECHAZADA", [(self.estado_inicial, None)], "La cadena vacía es rechazada porque el estado inicial no es de aceptación."
        
        estado_actual = self.estado_inicial
        historial_recorrido = [(estado_actual, None)]

        for simbolo in cadena:
            # Si un símbolo de la cadena no está en el alfabeto del autómata, la cadena es rechazada.
            if simbolo not in self.alfabeto:
                return "RECHAZADA", historial_recorrido, f"Error: El símbolo '{simbolo}' no pertenece al alfabeto."
            
            try:
                # Se busca la transición para el estado actual y el símbolo.
                estado_actual = self.transiciones[estado_actual][simbolo]
                historial_recorrido.append((estado_actual, simbolo))
            except KeyError:
                # Si no hay una transición definida, la cadena es rechazada.
                return "RECHAZADA", historial_recorrido, f"Proceso detenido: No hay transición definida desde el estado '{estado_actual}' con el símbolo '{simbolo}'."
        
        # Una vez que la cadena ha sido procesada, se verifica si el estado final es de aceptación.
        if estado_actual in self.estados_aceptacion:
            return "ACEPTADA", historial_recorrido, f"Proceso finalizado. El estado final es '{estado_actual}', que es un estado de aceptación."
        else:
            return "RECHAZADA", historial_recorrido, f"Proceso finalizado. El estado final es '{estado_actual}', que NO es un estado de aceptación."

    def generar_cadenas_lenguaje(self, num_cadenas=10):
        """
        Genera las primeras 'num_cadenas' que pertenecen al lenguaje del autómata.
        Utiliza una búsqueda en anchura (BFS) para encontrar las cadenas más cortas primero.

        Args:
            num_cadenas (int): El número de cadenas que se desea generar.
        
        Returns:
            list: Una lista de cadenas de texto que son aceptadas por el autómata.
        """
        if not self.estado_inicial:
            return []

        cadenas_validas = []
        
        # Si el estado inicial es de aceptación, la cadena vacía es la primera en el lenguaje.
        if self.estado_inicial in self.estados_aceptacion:
            cadenas_validas.append("*")
        
        cola = deque([(self.estado_inicial, "")])
        visitados = set([(self.estado_inicial, "")])
        
        while cola and len(cadenas_validas) < num_cadenas:
            estado_actual, cadena = cola.popleft()

            # Exploramos todas las transiciones posibles desde el estado actual.
            if estado_actual in self.transiciones:
                # Las transiciones se ordenan para obtener un orden de generación consistente.
                for simbolo, estado_siguiente in sorted(self.transiciones[estado_actual].items()):
                    nueva_cadena = cadena + simbolo
                    if (estado_siguiente, nueva_cadena) not in visitados:
                        visitados.add((estado_siguiente, nueva_cadena))
                        cola.append((estado_siguiente, nueva_cadena))
                        
                        # Si el nuevo estado es de aceptación, la cadena generada es válida.
                        if estado_siguiente in self.estados_aceptacion and nueva_cadena != "":
                            cadenas_validas.append(nueva_cadena)
        
        return cadenas_validas

    def guardar_a_json(self, nombre_archivo):
        """
        Guarda la definición del autómata en un archivo JSON.

        Args:
            nombre_archivo (str): El nombre del archivo donde se guardará el autómata.
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
            print(f"Autómata guardado exitosamente en '{nombre_archivo}'")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    def cargar_de_json(self, nombre_archivo):
        """
        Carga la definición de un autómata desde un archivo JSON.

        Args:
            nombre_archivo (str): El nombre del archivo desde donde se cargará el autómata.
        
        Returns:
            bool: True si la carga fue exitosa, False en caso contrario.
        """
        try:
            with open(nombre_archivo, 'r') as f:
                data = json.load(f)
            
            # Se asignan los datos cargados a los atributos del objeto.
            self.estados = set(data.get("estados", []))
            self.alfabeto = set(data.get("alfabeto", []))
            self.estado_inicial = data.get("estado_inicial")
            self.estados_aceptacion = set(data.get("estados_aceptacion", []))
            self.transiciones = data.get("transiciones", {})
            print(f"Autómata cargado exitosamente desde '{nombre_archivo}'")
            return True
        except FileNotFoundError:
            print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Error: El archivo '{nombre_archivo}' tiene un formato JSON inválido.")
            return False
        except KeyError as e:
            print(f"Error: Archivo JSON incompleto. Falta la clave {e}.")
            return False