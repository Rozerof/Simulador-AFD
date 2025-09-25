import json
import os
from automata_afd import AutomataAFD

class AutomataLogic:
    """
    Clase que maneja la lógica central de la aplicación de simulación de AFD.
    
    Actúa como el "cerebro" del programa, interactuando con la clase AutomataAFD
    para definir, evaluar, guardar y cargar los autómatas. 
    """
    def __init__(self):
        """
        Inicializa la clase con una instancia de AutomataAFD.
        """
        self.automata = AutomataAFD()

    def definir_automata(self, states, alphabet, initial_state, acceptance_states, transitions):
        """
        Define un autómata y delega la validación de sus componentes a la clase AutomataAFD.
        """
        self.automata.definir_automata(states, alphabet, transitions, initial_state, acceptance_states)
        return "Autómata definido correctamente."

    def evaluar_cadena(self, chain):
        """
        Evalúa si una cadena es aceptada por el autómata.
        """
        if not self.automata.estado_inicial:
            return None, None, "Define un autómata primero."
        return self.automata.evaluar_cadena(chain)

    def generar_cadenas(self):
        """
        Genera una lista de cadenas que pertenecen al lenguaje del autómata.
        """
        if not self.automata.estado_inicial:
            return "Define un autómata primero."
        chains = self.automata.generar_cadenas_lenguaje(10)
        return "Cadenas Válidas:\n" + "\n".join(chains)

    def guardar_automata(self, file_path):
        """
        Guarda el autómata actual en un archivo JSON.
        """
        if not self.automata.estado_inicial:
            return "Define un autómata para poder guardarlo."
        
        # Recibe el estado de éxito y el mensaje/error de AutomataAFD.
        success, message = self.automata.guardar_a_json(file_path)
        return message # Retorna el mensaje de éxito o error.

    def cargar_automata(self, file_path):
        """
        Carga un autómata desde un archivo JSON.
        
        Retorna: Una tupla con el mensaje de estado (str) y los datos cargados (dict o None).
        """
        # Recibe True/False y los datos/mensaje de error de AutomataAFD.
        success, result = self.automata.cargar_de_json(file_path)
        
        if success:
            # Si es exitoso, devuelve el mensaje de éxito y el diccionario de datos.
            return "Autómata cargado.", result
        else:
            # Si falla, devuelve el mensaje de error y None.
            return result, None