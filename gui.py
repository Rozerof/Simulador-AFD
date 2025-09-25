import tkinter as tk
from tkinter import ttk, filedialog
import os
from automata_logic import AutomataLogic

class AutomataGUI:
    """
    Clase principal responsable de la Interfaz Gráfica de Usuario (GUI) del simulador de AFD.

    Esta clase es la "Vista" y el "Controlador" de la interfaz, gestionando la 
    creación de todos los widgets y delegando la lógica de procesamiento a la instancia de AutomataLogic.
    """
    def __init__(self, master):
        """
        Inicializa la ventana principal de la aplicación y sus componentes.
        """
        self.master = master
        master.title("Simulador Interactivo de AFD")
        master.geometry("800x600")

        # Inicializa la clase de lógica para el manejo de datos y operaciones.
        self.automata_logic = AutomataLogic()
        
        # --- Configuración del Contenedor Principal y Scrollbar ---
        self.main_container = ttk.Frame(master, padding="10")
        self.main_container.pack(fill="both", expand=True)

        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(0, weight=1)
        
        input_container = ttk.Frame(self.main_container, padding="10")
        input_container.grid(row=0, column=0, sticky="nsew")
        
        # El Canvas permite el scroll vertical del frame de entrada.
        self.input_canvas = tk.Canvas(input_container)
        self.input_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(input_container, orient="vertical", command=self.input_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.input_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame interior donde se ubican todos los widgets de entrada.
        self.input_frame = ttk.Frame(self.input_canvas)
        self.input_canvas.create_window((0, 0), window=self.input_frame, anchor="nw")
        self.input_frame.bind("<Configure>", self.on_frame_configure)

        self.create_input_widgets() 
        self.load_example_automata() 

    
    def on_frame_configure(self, event):
        """
        Ajusta la región de desplazamiento del canvas cuando el frame interior cambia de tamaño.
        """
        self.input_canvas.configure(scrollregion=self.input_canvas.bbox("all"))
        self.input_canvas.itemconfig(self.input_canvas.create_window(0, 0, window=self.input_frame, anchor="nw"), width=self.input_canvas.winfo_width())

    
    def create_input_widgets(self):
        """
        Crea y posiciona todos los widgets (entradas, etiquetas, botones) de la interfaz.
        """
        # --- Sección de Definición de Autómata ---
        input_section = ttk.LabelFrame(self.input_frame, text="Definir Autómata", padding="10")
        input_section.pack(fill="x", pady=10)

        # Campos de entrada para la definición del AFD
        ttk.Label(input_section, text="Estados (ej: q0, q1):").pack(fill="x")
        self.states_entry = ttk.Entry(input_section)
        self.states_entry.pack(fill="x")
        
        ttk.Label(input_section, text="Alfabeto (ej: a, b):").pack(fill="x", pady=(10, 0))
        self.alphabet_entry = ttk.Entry(input_section)
        self.alphabet_entry.pack(fill="x")

        ttk.Label(input_section, text="Estado Inicial:").pack(fill="x", pady=(10, 0))
        self.initial_state_entry = ttk.Entry(input_section)
        self.initial_state_entry.pack(fill="x")

        ttk.Label(input_section, text="Estados de Aceptación (ej: q1):").pack(fill="x", pady=(10, 0))
        self.acceptance_states_entry = ttk.Entry(input_section)
        self.acceptance_states_entry.pack(fill="x")

        ttk.Label(input_section, text="Transiciones (ej: q0 a q1). No use el símbolo '*':").pack(fill="x", pady=(10, 0))
        self.transitions_text = tk.Text(input_section, height=5)
        self.transitions_text.pack(fill="x")
        
        define_button = ttk.Button(input_section, text="Definir Autómata", command=self.define_automata_from_gui)
        define_button.pack(fill="x", pady=10)

        # --- Sección de Acciones (Evaluar y Generar) ---
        action_section = ttk.LabelFrame(self.input_frame, text="Acciones", padding="10")
        action_section.pack(fill="x", pady=10)

        ttk.Label(action_section, text="Cadena a evaluar (usa '*' para la vacía):").pack(fill="x")
        self.chain_entry = ttk.Entry(action_section)
        self.chain_entry.pack(fill="x")
        ttk.Button(action_section, text="Evaluar Cadena", command=self.evaluate_chain).pack(fill="x", pady=5)
        
        # --- Recorrido de la Evaluación con Scrollbar ---
        ttk.Label(action_section, text="Recorrido de la evaluación:").pack(fill="x", pady=(10,0))
        
        eval_frame = ttk.Frame(action_section)
        eval_frame.pack(fill="both", expand=True)
        
        eval_scrollbar = ttk.Scrollbar(eval_frame)
        eval_scrollbar.pack(side="right", fill="y")

        self.evaluation_text = tk.Text(eval_frame, height=10, state='disabled', yscrollcommand=eval_scrollbar.set)
        self.evaluation_text.pack(side="left", fill="both", expand=True)

        eval_scrollbar.config(command=self.evaluation_text.yview)
        # --- Fin Recorrido de la Evaluación ---

        ttk.Button(action_section, text="Generar Cadenas", command=self.generate_chains).pack(fill="x", pady=5)

        # --- Sección de Gestión de Archivos ---
        file_section = ttk.LabelFrame(self.input_frame, text="Gestión de Archivos", padding="10")
        file_section.pack(fill="x", pady=10)
        ttk.Button(file_section, text="Guardar Autómata", command=self.save_automata).pack(fill="x", pady=5)
        ttk.Button(file_section, text="Cargar Autómata", command=self.load_automata).pack(fill="x", pady=5)
        
        # Etiqueta para mensajes de error o éxito
        self.output_label = ttk.Label(self.input_frame, text="", foreground="blue")
        self.output_label.pack(fill="x", pady=10)

    
    def define_automata_from_gui(self):
        """
        Recopila los datos de la GUI y llama a la lógica para definir y validar el autómata.
        Actualiza el mensaje de salida según el éxito o el error de la operación.
        """
        try:
            # Recopilación de datos y pre-procesamiento (separación por comas, eliminación de espacios)
            states = [s.strip() for s in self.states_entry.get().split(',') if s.strip()]
            alphabet = [s.strip() for s in self.alphabet_entry.get().split(',') if s.strip()]
            initial_state = self.initial_state_entry.get().strip()
            acceptance_states = [s.strip() for s in self.acceptance_states_entry.get().split(',') if s.strip()]
            transitions_str = self.transitions_text.get("1.0", tk.END).strip().split('\n')
            transitions = [tuple(t.strip().split()) for t in transitions_str if t.strip()]

            # Delegación a la capa de lógica (AutomataLogic)
            message = self.automata_logic.definir_automata(states, alphabet, initial_state, acceptance_states, transitions)
            self.output_label.config(text=message, foreground="green")
        except Exception as e:
            # Muestra errores de validación
            self.output_label.config(text=f"Error al definir: {e}", foreground="red")

    
    def evaluate_chain(self):
        """
        Recopila la cadena de la GUI, llama a la lógica para su evaluación y formatea el resultado.
        Muestra el recorrido paso a paso y el resultado final.
        """
        chain = self.chain_entry.get().strip()
        result, recorrido, message = self.automata_logic.evaluar_cadena(chain)
        
        self.evaluation_text.config(state='normal')
        self.evaluation_text.delete('1.0', tk.END)

        # 1. Comprobación de estado no inicializado o error de ejecución irrecuperable
        if result is None or "Error" in message or "Proceso detenido" in message:
            self.output_label.config(text=message, foreground="red")
            self.evaluation_text.config(state='disabled')
            return

        self.evaluation_text.insert(tk.END, f"Evaluando la cadena: \"{chain}\"\n")
        
        # Muestra el recorrido de la simulación
        if chain == '*':
            self.evaluation_text.insert(tk.END, "1. La cadena es vacía. El recorrido no tiene transiciones.\n")
        else:
            for i, (estado, simbolo) in enumerate(recorrido):
                if i == 0:
                    self.evaluation_text.insert(tk.END, f"1. Iniciando en el estado ({estado}).\n")
                else:
                    estado_anterior = recorrido[i-1][0]
                    self.evaluation_text.insert(tk.END, f"{i}. Desde el estado ({estado_anterior}) con el símbolo '{simbolo}' se transita al estado ({estado}).\n")
        
        # Muestra el resultado final en el cuadro de recorrido
        self.evaluation_text.insert(tk.END, "\nProceso finalizado.\n")
        self.evaluation_text.insert(tk.END, f"Resultado: La cadena \"{chain}\" es {result}.\n")
        self.evaluation_text.insert(tk.END, f"Mensaje: {message}\n")
        
        # 2. Actualiza la etiqueta de salida (output_label) con el resultado y color
        if result == "ACEPTADA":
            self.output_label.config(text=message, foreground="green")
        else:
            # Si el resultado es RECHAZADA, muestra el resultado en rojo.
            self.output_label.config(text=message, foreground="red")
            
        self.evaluation_text.config(state='disabled')

    
    def generate_chains(self):
        """
        Llama al método de la lógica para generar cadenas válidas y muestra el resultado en la etiqueta de salida.
        """
        message = self.automata_logic.generar_cadenas()
        if "Define un autómata" in message:
            self.output_label.config(text=message, foreground="red")
        else:
            self.output_label.config(text=message, foreground="blue")

    
    def save_automata(self):
        """
        Abre el diálogo de guardar archivo y delega la operación de guardado a la lógica.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            message = self.automata_logic.guardar_automata(file_path)
            self.output_label.config(text=message, foreground="green")

    
    def load_automata(self):
        """
        Abre el diálogo de abrir archivo, llama a la lógica para cargar, y si es exitoso, 
        ACTUALIZA todos los campos de texto de la GUI con los datos cargados.
        """
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            # Recibe el mensaje de estado y los datos cargados (si es exitoso)
            message, loaded_data = self.automata_logic.cargar_automata(file_path)
            
            # Comprobación de éxito: solo si el mensaje es el de éxito Y se recibieron datos.
            if message == "Autómata cargado." and loaded_data:
                
                # --- LIMPIAR E INSERTAR DATOS ---
                
                # 1. Limpiar todos los campos
                self.states_entry.delete(0, tk.END)
                self.alphabet_entry.delete(0, tk.END)
                self.initial_state_entry.delete(0, tk.END)
                self.acceptance_states_entry.delete(0, tk.END)
                self.transitions_text.delete("1.0", tk.END)
                
                # 2. Insertar los datos del diccionario cargado
                self.states_entry.insert(0, ", ".join(loaded_data['estados']))
                self.alphabet_entry.insert(0, ", ".join(loaded_data['alfabeto']))
                self.initial_state_entry.insert(0, loaded_data['estado_inicial'])
                self.acceptance_states_entry.insert(0, ", ".join(loaded_data['estados_aceptacion']))
                
                # 3. Formatear las transiciones para el widget Text
                transitions_lines = []
                for origen, transiciones in loaded_data['transiciones'].items():
                    for simbolo, destino in transiciones.items():
                        transitions_lines.append(f"{origen} {simbolo} {destino}")
                
                self.transitions_text.insert(tk.END, "\n".join(transitions_lines))
                
                # 4. Mostrar mensaje de éxito
                self.output_label.config(text=message, foreground="green")
            else:
                # Mostrar mensaje de error (incluido si el archivo está mal o no existe)
                self.output_label.config(text=message, foreground="red")

    
    def load_example_automata(self):
        """
        Carga un autómata predefinido en los campos de entrada de la GUI para facilitar las pruebas.
        """
        self.states_entry.insert(0, "q0, q1, q2")
        self.alphabet_entry.insert(0, "a, b")
        self.initial_state_entry.insert(0, "q0")
        self.acceptance_states_entry.insert(0, "q0, q2")
        self.transitions_text.insert(tk.END, "q0 a q1\nq0 b q0\nq1 a q1\nq1 b q2\nq2 a q2\nq2 b q2")
        self.define_automata_from_gui()

if __name__ == '__main__':
    # Punto de entrada principal de la aplicación GUI
    root = tk.Tk()
    app = AutomataGUI(root)
    root.mainloop()