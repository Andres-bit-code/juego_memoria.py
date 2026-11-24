# Juego de Memoria
## Descripción del proyecto
El Juego de Memoria es un programa desarrollado en Python utilizando la biblioteca Pygame.
El proyecto permite que dos jugadores participen en una misma computadora, buscando parejas de cartas iguales.
El juego cuenta con tres niveles de dificultad. Cada nivel aumenta la cantidad de cartas y presenta un tiempo límite para completar la partida.
## Objetivo
Desarrollar un juego de memoria que permita practicar la lógica de programación mediante condiciones, funciones, variables y estructuras de decisión.
## Características
- Modo local para dos jugadores.
- Menú principal.
- Sección de opciones e instrucciones.
- Tres niveles de dificultad.
- Sistema de puntos para cada jugador.
- Control del tiempo.
- Desbloqueo progresivo de niveles.
- Pantallas de victoria y derrota.
## Tecnologías utilizadas
- Python.
- Pygame.
- RAPTOR.
- Visual Studio Code.
## Estructura del proyecto
ProyectoJuego/
- juego.py
- game_logic.py
- README.md
- LICENSE
- diseno/
  - DF1_Menu.rap
  - DF2_Validacion.rap
  - DF3_FinPartida.rap
## Cómo ejecutar el proyecto
1. Instalar Python.
2. Instalar Pygame utilizando el siguiente comando:
   python -m pip install pygame
3. Abrir la carpeta del proyecto en Visual Studio Code.
4. Ejecutar el archivo juego.py.
## Funcionamiento
Los dos jugadores participan por turnos. Cada uno selecciona dos cartas intentando encontrar una pareja igual.
Cuando un jugador encuentra una pareja, obtiene un punto y conserva su turno. Si las cartas son diferentes, se ocultan y el turno pasa al otro jugador.
El objetivo es encontrar todas las parejas antes de que termine el tiempo.
## Autores
Proyecto desarrollado por los integrantes del grupo de trabajo.
## Licencia
Consultar el archivo LICENSE para conocer las condiciones de uso del proyecto.