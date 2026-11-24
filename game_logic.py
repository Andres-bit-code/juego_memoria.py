def validar_cartas(cartas, descubiertas, parejas_encontradas):

    if len(descubiertas) != 2:
        return False

    carta1 = descubiertas[0]
    carta2 = descubiertas[1]

    if carta1 == carta2:
        return False

    if carta1 in parejas_encontradas:
        return False

    if carta2 in parejas_encontradas:
        return False

    return True


# Funcion para comprobar si se encontro una pareja
def comprobar_pareja(cartas, descubiertas):

    if cartas[descubiertas[0]] == cartas[descubiertas[1]]:
        return True
    else:
        return False


# Funcion para comprobar si termino la partida
def comprobar_fin_partida(cartas, parejas_encontradas):

    if len(parejas_encontradas) == len(cartas):
        return True
    else:
        return False

# Funcion para determinar el resultado de la partida
def determinar_resultado(puntaje_jugador1, puntaje_jugador2, tiempo_restante, partida_terminada):

    if tiempo_restante <= 0 and not partida_terminada:
        return "derrota"

    if not partida_terminada:
        return "continua"

    if puntaje_jugador1 > puntaje_jugador2:
        return "gana_jugador1"

    if puntaje_jugador2 > puntaje_jugador1:
        return "gana_jugador2"

    return "empate"

# Prueba de funcionamiento

cartas = ["A", "B", "A", "B"]
descubiertas = [0, 2]
parejas_encontradas = []

print("Validar cartas:", validar_cartas(cartas, descubiertas, parejas_encontradas))

print("Comprobar pareja:", comprobar_pareja(cartas, descubiertas))

parejas_encontradas = [0, 2]

print("Partida terminada:", comprobar_fin_partida(cartas, parejas_encontradas))

print("Resultado:", determinar_resultado(2, 1, 20, True))
