import json
import os
from automata_afd import AutomataAFD

class AutomataLogic:
    """
    Clase que maneja la lógica central de la aplicación de simulación de AFD.
    
    Actúa como el "cerebro" del programa, interactuando con la clase AutomataAFD
    para definir, evaluar, guardar y cargar los autómatas. Esta clase separa la
    lógica de la aplicación de la interfaz de usuario.
    """
    def __init__(self):
        """
        Inicializa la clase con una instancia de AutomataAFD.
        """
        self.automata = AutomataAFD()

    def definir_automata(self, states, alphabet, initial_state, acceptance_states, transitions):
        """
        Define un autómata y delega la validación de sus componentes a la clase AutomataAFD.
        
        Args:
            states (list): Lista de estados del autómata.
            alphabet (list): Lista de símbolos del alfabeto.
            initial_state (str): Estado inicial.
            acceptance_states (list): Lista de estados de aceptación.
            transitions (list): Lista de transiciones en formato (origen, simbolo, destino).
            
        Returns:
            str: Un mensaje de éxito.
        """
        # La validación detallada se realiza dentro de la clase AutomataAFD.
        self.automata.definir_automata(states, alphabet, transitions, initial_state, acceptance_states)
        return "Autómata definido correctamente."

    def evaluar_cadena(self, chain):
        """
        Evalúa si una cadena es aceptada por el autómata.
        
        Args:
            chain (str): La cadena a evaluar.
            
        Returns:
            tuple: El resultado de la evaluación, el recorrido y un mensaje.
        """
        if not self.automata.estado_inicial:
            return None, None, "Define un autómata primero."
        return self.automata.evaluar_cadena(chain)

    def generar_cadenas(self):
        """
        Genera una lista de cadenas que pertenecen al lenguaje del autómata.
        
        Returns:
            str: Un mensaje que contiene las cadenas válidas, o un mensaje de error.
        """
        if not self.automata.estado_inicial:
            return "Define un autómata primero."
        chains = self.automata.generar_cadenas_lenguaje(10)
        return "Cadenas Válidas:\n" + "\n".join(chains)

    def guardar_automata(self, file_path):
        """
        Guarda el autómata actual en un archivo JSON.
        
        Args:
            file_path (str): La ruta del archivo para guardar el autómata.
            
        Returns:
            str: Un mensaje de éxito o de error.
        """
        if not self.automata.estado_inicial:
            return "Define un autómata para poder guardarlo."
        self.automata.guardar_a_json(file_path)
        return "Autómata guardado."

    def cargar_automata(self, file_path):
        """
        Carga un autómata desde un archivo JSON.
        
        Args:
            file_path (str): La ruta del archivo para cargar el autómata.
            
        Returns:
            str: Un mensaje de éxito o de error.
        """
        if self.automata.cargar_de_json(file_path):
            return "Autómata cargado."
        else:
            return "Error al cargar autómata."