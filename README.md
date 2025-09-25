Simulador Interactivo de Autómatas Finitos Deterministas (AFD)
----------------------------
Este proyecto es un simulador interactivo que permite la definición, visualización y evaluación de Autómatas Finitos Deterministas (AFD).
Su objetivo es brindar una herramienta para crear autómatas, visualizar su representación gráfica y comprobar si cadenas de entrada son aceptadas o rechazadas.
----------------------------
Características

Definición de AFD: Permite ingresar los cinco componentes fundamentales de un autómata.

Evaluación de cadenas: Determina si una cadena pertenece al lenguaje, mostrando el recorrido paso a paso.

Generación de cadenas: Produce ejemplos de cadenas aceptadas por el autómata.

Gestión de archivos: Guarda y carga definiciones en formato JSON.

Visualización gráfica: Genera una representación del autómata utilizando Graphviz.
----------------------------
Requisitos

Python 3.x

Módulos de Python: Pillow, graphviz

Graphviz (software externo para la visualización de grafos)

Instalación y Configuración

Instalar dependencias de Python
pip install Pillow graphviz

Instalar Graphviz
----------------------------
Windows:
Descargar el instalador desde https://graphviz.org/download/

Durante la instalación, seleccionar la opción para agregar Graphviz al PATH del sistema.
----------------------------
macOS (con Homebrew):
brew install graphviz
----------------------------
Linux (Ubuntu/Debian):
sudo apt-get install graphviz

Nota: Después de la instalación es recomendable reiniciar la terminal para que los cambios en el PATH se apliquen correctamente.
----------------------------
Estructura del Proyecto

El código se diseñó siguiendo el Principio de Responsabilidad Única (SRP), separando la lógica de la interfaz:

proyecto_afd/

gui.py # Interfaz gráfica (AutomataGUI)

automata_logic.py # Lógica principal del simulador

automata_afd.py # Definición del modelo matemático del AFD
----------------------------
Uso del Simulador

Abrir una terminal o símbolo del sistema.

Navegar hasta el directorio del proyecto.

Ejecutar la aplicación con el siguiente comando:

python gui.py
----------------------------
Créditos

Hecho por: 
Maria Medina
Silvia Rodriguez

