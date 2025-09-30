import json
import os
from automata_afd import AutomataAFD

class AutomataLogic:
    """
    Clase que maneja la lógica central de la aplicación de simulación de AFD.
    
    Actúa como el "cerebro" o "controlador" del programa, interactuando con la
    clase AutomataAFD para definir, evaluar, guardar y cargar los autómatas.
    Esta clase desacopla la interfaz gráfica (GUI) de la lógica del modelo
    matemático del autómata.
    """
    def __init__(self):
        """
        Inicializa la clase con una instancia de AutomataAFD.
        
        Atributos:
            automata (AutomataAFD): Una instancia del modelo de autómata que se
                                   gestionará a lo largo del ciclo de vida de la aplicación.
        """
        self.automata = AutomataAFD()

    def definir_automata(self, states, alphabet, initial_state, acceptance_states, transitions):
        """
        Define un autómata y delega la validación de sus componentes a la clase AutomataAFD.

        Args:
            states (list): Lista de estados.
            alphabet (list): Lista de símbolos del alfabeto.
            initial_state (str): El estado inicial.
            acceptance_states (list): Lista de estados de aceptación.
            transitions (list): Lista de transiciones.

        Returns:
            str: Un mensaje indicando que el autómata se definió correctamente.
                 La validación de errores se maneja mediante excepciones en AutomataAFD.
        """
        self.automata.definir_automata(states, alphabet, transitions, initial_state, acceptance_states)
        return "Autómata definido correctamente."

    def evaluar_cadena(self, chain):
        """
        Evalúa si una cadena es aceptada por el autómata.

        Args:
            chain (str): La cadena a evaluar.

        Returns:
            tuple: Una tupla con tres elementos:
                   - str: "ACEPTADA" o "RECHAZADA", o None si no hay autómata definido.
                   - list: El historial del recorrido, o None.
                   - str: Un mensaje descriptivo del resultado o del error.
        """
        if not self.automata.estado_inicial:
            return None, None, "Define un autómata primero."
        return self.automata.evaluar_cadena(chain)

    def generar_cadenas(self):
        """
        Genera una lista de cadenas que pertenecen al lenguaje del autómata.

        Returns:
            str: Una cadena de texto formateada con las cadenas válidas encontradas,
                 o un mensaje de advertencia si no hay un autómata definido.
        """
        if not self.automata.estado_inicial:
            return "Define un autómata primero."
        chains = self.automata.generar_cadenas_lenguaje(10)
        return "Cadenas Válidas:\n" + "\n".join(chains)

    def guardar_automata(self, file_path):
        """
        Guarda el autómata actual en un archivo JSON.

        Args:
            file_path (str): La ruta del archivo donde se guardará el autómata.

        Returns:
            str: Un mensaje indicando el resultado de la operación (éxito o error),
                 o una advertencia si no hay autómata para guardar.
        """
        if not self.automata.estado_inicial:
            return "Define un autómata para poder guardarlo."
        
        # Recibe el estado de éxito y el mensaje/error de AutomataAFD.
        success, message = self.automata.guardar_a_json(file_path)
        return message # Retorna el mensaje de éxito o error.

    def cargar_automata(self, file_path):
        """
        Carga un autómata desde un archivo JSON.

        Args:
            file_path (str): La ruta del archivo JSON a cargar.

        Returns:
            tuple: Una tupla con dos elementos:
                   - str: Un mensaje de estado ("Autómata cargado." o un mensaje de error).
                   - dict or None: El diccionario con los datos del autómata si la carga fue exitosa, de lo contrario None.
        """
        # Recibe True/False y los datos/mensaje de error de AutomataAFD.
        success, result = self.automata.cargar_de_json(file_path)
        
        if success:
            # Si es exitoso, devuelve el mensaje de éxito y el diccionario de datos.
            return "Autómata cargado.", result
        else:
            # Si falla, devuelve el mensaje de error y None.
            return result, None