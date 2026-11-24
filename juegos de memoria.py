
import pygame
import random

from game_logic import validar_cartas
from game_logic import comprobar_pareja
from game_logic import comprobar_fin_partida
from game_logic import determinar_resultado

pygame.init()

# Configuracion de la ventana
ANCHO = 900
ALTO = 760

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Memoria")

reloj = pygame.time.Clock()

# Colores
FONDO = (18, 25, 50)
AZUL = (45, 100, 190)
AZUL_OSCURO = (30, 55, 110)
VERDE = (40, 170, 100)
ROJO = (210, 65, 65)
BLANCO = (255, 255, 255)
AMARILLO = (255, 210, 60)
GRIS = (100, 110, 130)

# Fuentes
fuente = pygame.font.SysFont("Arial", 28)
fuente_grande = pygame.font.SysFont("Arial", 48)
fuente_carta = pygame.font.SysFont("Arial", 35)
fuente_pequena = pygame.font.SysFont("Arial", 22)

# Configuracion de niveles
niveles = {
    1: [3, 4, 60],
    2: [4, 4, 50],
    3: [4, 5, 40]
}

# Simbolos disponibles
simbolos = [
    "1", "2", "3", "4", "5", "6",
    "A", "B", "C", "D", "E", "F",
    "+", "-", "*", "/", "%",
    "@", "#", "$", "&", "?"
]

# Variables generales
estado = "menu"
nivel = 1
nivel_desbloqueado = 1

jugador = 1

puntaje_jugador1 = 0
puntaje_jugador2 = 0

cartas = []
descubiertas = []
parejas_encontradas = []

filas = 3
columnas = 4

tiempo_limite = 60
tiempo_inicio = 0

esperando = False
tiempo_espera = 0


# Funcion para mostrar texto
def mostrar_texto(texto, fuente_usada, color, x, y):

    imagen = fuente_usada.render(str(texto), True, color)
    pantalla.blit(imagen, (x, y))


# Funcion para crear botones
def crear_boton(texto, x, y, ancho, alto, color):

    rectangulo = pygame.Rect(x, y, ancho, alto)

    pygame.draw.rect(
        pantalla,
        color,
        rectangulo,
        border_radius=12
    )

    imagen = fuente.render(texto, True, BLANCO)

    texto_x = x + (ancho - imagen.get_width()) // 2
    texto_y = y + (alto - imagen.get_height()) // 2

    pantalla.blit(imagen, (texto_x, texto_y))

    return rectangulo


# Preparar un nivel
def preparar_nivel(numero_nivel):

    global filas, columnas, tiempo_limite
    global cartas, descubiertas, parejas_encontradas
    global tiempo_inicio, esperando, jugador, estado

    filas = niveles[numero_nivel][0]
    columnas = niveles[numero_nivel][1]
    tiempo_limite = niveles[numero_nivel][2]

    cantidad_parejas = (filas * columnas) // 2

    seleccion = random.sample(simbolos, cantidad_parejas)

    cartas = seleccion * 2
    random.shuffle(cartas)

    descubiertas = []
    parejas_encontradas = []

    jugador = 1
    esperando = False

    tiempo_inicio = pygame.time.get_ticks()

    estado = "juego"


# Dibujar tablero
def dibujar_tablero():

    ancho_carta = 125
    alto_carta = 100
    espacio = 12

    ancho_total = columnas * ancho_carta + (columnas - 1) * espacio

    inicio_x = (ANCHO - ancho_total) // 2
    inicio_y = 230

    for fila in range(filas):

        for columna in range(columnas):

            numero = fila * columnas + columna

            x = inicio_x + columna * (ancho_carta + espacio)
            y = inicio_y + fila * (alto_carta + espacio)

            rectangulo = pygame.Rect(
                x,
                y,
                ancho_carta,
                alto_carta
            )

            if numero in descubiertas or numero in parejas_encontradas:
                color = VERDE
            else:
                color = AZUL

            pygame.draw.rect(
                pantalla,
                color,
                rectangulo,
                border_radius=12
            )

            if numero in descubiertas or numero in parejas_encontradas:

                imagen = fuente_carta.render(
                    cartas[numero],
                    True,
                    BLANCO
                )

                texto_x = x + (ancho_carta - imagen.get_width()) // 2
                texto_y = y + (alto_carta - imagen.get_height()) // 2

                pantalla.blit(imagen, (texto_x, texto_y))


# Menu principal
def dibujar_menu():

    pantalla.fill(FONDO)

    mostrar_texto(
        "JUEGO DE MEMORIA",
        fuente_grande,
        AMARILLO,
        250,
        120
    )

    mostrar_texto(
        "Dos jugadores - Modo local",
        fuente,
        BLANCO,
        300,
        185
    )

    boton_jugar = crear_boton(
        "JUGAR",
        300, 280, 300, 65,
        AZUL
    )

    boton_opciones = crear_boton(
        "OPCIONES",
        300, 380, 300, 65,
        AZUL_OSCURO
    )

    boton_salir = crear_boton(
        "SALIR",
        300, 480, 300, 65,
        ROJO
    )

    return boton_jugar, boton_opciones, boton_salir


# Menu de opciones
def dibujar_opciones():

    pantalla.fill(FONDO)

    mostrar_texto(
        "OPCIONES",
        fuente_grande,
        AMARILLO,
        340,
        100
    )

    mostrar_texto(
        "Instrucciones del juego:",
        fuente,
        BLANCO,
        260,
        230
    )

    mostrar_texto(
        "1. Participan dos jugadores humanos.",
        fuente_pequena,
        BLANCO,
        260,
        290
    )

    mostrar_texto(
        "2. Cada jugador debe encontrar parejas.",
        fuente_pequena,
        BLANCO,
        260,
        330
    )

    mostrar_texto(
        "3. Si encuentra una pareja, suma un punto.",
        fuente_pequena,
        BLANCO,
        260,
        370
    )

    mostrar_texto(
        "4. Si falla, pasa el turno al otro jugador.",
        fuente_pequena,
        BLANCO,
        260,
        410
    )

    mostrar_texto(
        "5. Completa el nivel antes de que termine el tiempo.",
        fuente_pequena,
        BLANCO,
        260,
        450
    )

    boton_volver = crear_boton(
        "VOLVER",
        300, 550, 300, 65,
        AZUL
    )

    return boton_volver


# Seleccion de niveles
def dibujar_niveles():

    pantalla.fill(FONDO)

    mostrar_texto(
        "SELECCIONA UN NIVEL",
        fuente_grande,
        AMARILLO,
        200,
        100
    )

    botones = []

    for numero in range(1, 4):

        x = 150 + (numero - 1) * 210

        if numero <= nivel_desbloqueado:

            color = VERDE
            texto = "NIVEL " + str(numero)

        else:

            color = GRIS
            texto = "BLOQUEADO"

        boton = crear_boton(
            texto,
            x, 300, 180, 90,
            color
        )

        botones.append(boton)

        mostrar_texto(
            str(niveles[numero][0]) + " x " +
            str(niveles[numero][1]) + " cuadros",
            fuente_pequena,
            BLANCO,
            x + 5,
            410
        )

        mostrar_texto(
            str(niveles[numero][2]) + " segundos",
            fuente_pequena,
            AMARILLO,
            x + 15,
            445
        )

    boton_volver = crear_boton(
        "VOLVER",
        300, 570, 300, 65,
        AZUL_OSCURO
    )

    return botones, boton_volver


# Pantalla del juego
def dibujar_juego(tiempo_restante):

    pantalla.fill(FONDO)

    mostrar_texto(
        "JUEGO DE MEMORIA",
        fuente_grande,
        AMARILLO,
        250,
        20
    )

    mostrar_texto(
        "Nivel: " + str(nivel),
        fuente,
        BLANCO,
        70,
        110
    )

    mostrar_texto(
        "Tiempo: " + str(tiempo_restante),
        fuente,
        AMARILLO,
        370,
        110
    )

    mostrar_texto(
        "Jugador 1: " + str(puntaje_jugador1),
        fuente,
        BLANCO,
        70,
        160
    )

    mostrar_texto(
        "Jugador 2: " + str(puntaje_jugador2),
        fuente,
        BLANCO,
        610,
        160
    )

    mostrar_texto(
        "Turno del jugador " + str(jugador),
        fuente,
        AMARILLO,
        330,
        195
    )

    dibujar_tablero()


# Bucle principal
jugando = True

while jugando:

    reloj.tick(60)

    # MENU PRINCIPAL
    if estado == "menu":

        botones = dibujar_menu()

    # OPCIONES
    elif estado == "opciones":

        boton_volver = dibujar_opciones()

    # SELECCION DE NIVELES
    elif estado == "niveles":

        botones_niveles, boton_volver = dibujar_niveles()

    # JUEGO
    elif estado == "juego":

        tiempo_actual = pygame.time.get_ticks()

        segundos_pasados = (tiempo_actual - tiempo_inicio) // 1000

        tiempo_restante = tiempo_limite - segundos_pasados

        if tiempo_restante < 0:
            tiempo_restante = 0

        dibujar_juego(tiempo_restante)

        # Comprobar tiempo
        if tiempo_restante == 0:
            estado = "derrota"

        # Comprobar parejas
        if comprobar_fin_partida(cartas, parejas_encontradas):
            estado = "victoria"

        # Ocultar cartas incorrectas
        if esperando:

            if tiempo_actual - tiempo_espera >= 1000:

                descubiertas = []
                esperando = False

                if jugador == 1:
                    jugador = 2
                else:
                    jugador = 1

        # Comprobar parejas seleccionadas
        if len(descubiertas) == 2 and not esperando:

            if validar_cartas(cartas, descubiertas, parejas_encontradas):

                if comprobar_pareja(cartas, descubiertas):

                    parejas_encontradas.extend(descubiertas)

                    if jugador == 1:
                        puntaje_jugador1 += 1
                    else:
                        puntaje_jugador2 += 1

                    descubiertas = []

                else:

                    esperando = True
                    tiempo_espera = tiempo_actual

    # VICTORIA
    elif estado == "victoria":

        pantalla.fill(FONDO)

        mostrar_texto(
            "¡NIVEL COMPLETADO!",
            fuente_grande,
            VERDE,
            240,
            130
        )

        resultado = determinar_resultado(
            puntaje_jugador1,
            puntaje_jugador2,
            0,
            True
        )

        if resultado == "gana_jugador1":

            mensaje = "GANA EL JUGADOR 1"

        elif resultado == "gana_jugador2":

            mensaje = "GANA EL JUGADOR 2"

        else:

            mensaje = "EMPATE"

        mostrar_texto(
            mensaje,
            fuente,
            AMARILLO,
            330,
            220
        )

        mostrar_texto(
            "Jugador 1: " + str(puntaje_jugador1),
            fuente,
            BLANCO,
            300,
            300
        )

        mostrar_texto(
            "Jugador 2: " + str(puntaje_jugador2),
            fuente,
            BLANCO,
            300,
            350
        )

        if nivel < 3:

            mostrar_texto(
                "Presiona ESPACIO para continuar",
                fuente,
                BLANCO,
                230,
                470
            )

        else:

            mostrar_texto(
                "¡HAS COMPLETADO TODOS LOS NIVELES!",
                fuente,
                AMARILLO,
                150,
                470
            )

        boton_menu = crear_boton(
            "MENU PRINCIPAL",
            300, 550, 300, 65,
            AZUL
        )

    # DERROTA
    elif estado == "derrota":

        pantalla.fill(FONDO)

        mostrar_texto(
            "¡SE ACABO EL TIEMPO!",
            fuente_grande,
            ROJO,
            220,
            180
        )

        mostrar_texto(
            "No completaron el nivel.",
            fuente,
            BLANCO,
            300,
            270
        )

        boton_reintentar = crear_boton(
            "REINTENTAR",
            300, 370, 300, 65,
            VERDE
        )

        boton_menu = crear_boton(
            "MENU PRINCIPAL",
            300, 470, 300, 65,
            AZUL
        )

    # EVENTOS
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            jugando = False

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:

                if estado == "juego":
                    estado = "niveles"
                elif estado == "menu":
                    jugando = False
                else:
                    estado = "menu"

            if evento.key == pygame.K_SPACE:

                if estado == "victoria" and nivel < 3:

                    nivel += 1

                    if nivel > nivel_desbloqueado:
                        nivel_desbloqueado = nivel

                    preparar_nivel(nivel)

        if evento.type == pygame.MOUSEBUTTONDOWN:

            if evento.button == 1:

                # Botones del menu
                if estado == "menu":

                    boton_jugar, boton_opciones, boton_salir = botones

                    if boton_jugar.collidepoint(evento.pos):

                        estado = "niveles"

                    elif boton_opciones.collidepoint(evento.pos):

                        estado = "opciones"

                    elif boton_salir.collidepoint(evento.pos):

                        jugando = False

                # Boton volver de opciones
                elif estado == "opciones":

                    if boton_volver.collidepoint(evento.pos):
                        estado = "menu"

                # Seleccion de niveles
                elif estado == "niveles":

                    if boton_volver.collidepoint(evento.pos):

                        estado = "menu"

                    else:

                        for numero in range(1, 4):

                            if botones_niveles[numero - 1].collidepoint(evento.pos):

                                if numero <= nivel_desbloqueado:

                                    nivel = numero
                                    preparar_nivel(nivel)

                # Seleccion de cartas
                elif estado == "juego":

                    if not esperando and len(descubiertas) < 2:

                        ancho_carta = 125
                        alto_carta = 100
                        espacio = 12

                        ancho_total = columnas * ancho_carta + (columnas - 1) * espacio

                        inicio_x = (ANCHO - ancho_total) // 2
                        inicio_y = 230

                        for fila in range(filas):

                            for columna in range(columnas):

                                numero = fila * columnas + columna

                                x = inicio_x + columna * (ancho_carta + espacio)
                                y = inicio_y + fila * (alto_carta + espacio)

                                rectangulo = pygame.Rect(
                                    x,
                                    y,
                                    ancho_carta,
                                    alto_carta
                                )

                                if rectangulo.collidepoint(evento.pos):

                                    if (
                                        numero not in descubiertas
                                        and numero not in parejas_encontradas
                                    ):

                                        descubiertas.append(numero)

                # Botones de victoria
                elif estado == "victoria":

                    if boton_menu.collidepoint(evento.pos):

                        estado = "menu"

                # Botones de derrota
                elif estado == "derrota":

                    if boton_reintentar.collidepoint(evento.pos):

                        preparar_nivel(nivel)

                    elif boton_menu.collidepoint(evento.pos):

                        estado = "menu"

    pygame.display.update()

pygame.quit()
