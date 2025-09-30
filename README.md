# Simulador Interactivo de Autómatas Finitos Deterministas (AFD)

Este proyecto es un simulador de escritorio desarrollado en Python que permite la definición, visualización y evaluación de Autómatas Finitos Deterministas (AFD). Su objetivo es brindar una herramienta educativa e intuitiva para experimentar con la teoría de autómatas.

## Características

-   **Definición de AFD:** Permite ingresar los cinco componentes de un autómata (estados, alfabeto, estado inicial, estados de aceptación y transiciones) a través de una interfaz gráfica amigable.
-   **Validación en Tiempo Real:** El sistema valida la consistencia del autómata al momento de su definición, notificando al usuario sobre errores lógicos (ej. estados no definidos, transiciones duplicadas).
-   **Evaluación de Cadenas:** Determina si una cadena pertenece al lenguaje del autómata, mostrando un recorrido detallado paso a paso de la simulación.
-   **Generación de Cadenas:** Produce una lista de cadenas válidas y aceptadas por el autómata, comenzando por las más cortas.
-   **Gestión de Archivos:** Permite guardar la definición de un autómata en un archivo `JSON` y cargarlo posteriormente para continuar trabajando.

## Requisitos

-   Python 3.x (incluye la librería `tkinter` por defecto).

No se requieren librerías externas para ejecutar la aplicación.

## Instalación y Uso

1.  Asegúrate de tener Python 3 instalado.
2.  Clona o descarga este repositorio en tu máquina local.
3.  Abre una terminal o símbolo del sistema.
4.  Navega hasta el directorio raíz del proyecto.
5.  Ejecuta la aplicación con el siguiente comando:

```bash
python gui.py
```

## Estructura del Proyecto

El código se diseñó siguiendo el Principio de Responsabilidad Única (SRP), separando la lógica de la interfaz gráfica y del modelo de datos.

-   `gui.py`: Contiene la clase `AutomataGUI`, responsable de construir y gestionar toda la interfaz gráfica de usuario (Vista/Controlador). Utiliza la librería `tkinter`.
-   `automata_logic.py`: Contiene la clase `AutomataLogic`, que actúa como intermediaria entre la interfaz y el modelo del autómata. Maneja la lógica de la aplicación.
-   `automata_afd.py`: Contiene la clase `AutomataAFD`, que es la representación matemática del autómata (Modelo). Implementa toda la funcionalidad principal, como la validación, evaluación y generación de cadenas.

## Créditos

Desarrollado por:
-   Maria Medina
-   Silvia Rodriguez
