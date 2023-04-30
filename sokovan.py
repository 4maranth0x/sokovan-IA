import os

#Lee el mapa que se le entrega en el input y lo asume como mapa
def leerMapa():    
    mapa = input("¿Qué nivel jugaré?")
    nivel_ruta = os.path.join("nivelesAqui", mapa)
    with open(f"nivelesAqui/{mapa}.txt", "r") as file:
        content = file.readlines()
    content = [linea.strip().split() for linea in content]
    # Mapear los caracteres especiales a sus valores numéricos
    bloque_mapeo = {'W': 1, 'X': 2, '0': 0}
    jugador_pos = None
    cajas_pos = []
    for i in range(len(content)):
        for j in range(len(content[i])):
            if content[i][j] == '1':
                if jugador_pos is not None:
                    return None, None, None # hay más de un jugador
                jugador_pos = (i, j)
            elif content[i][j].isdigit() and int(content[i][j]) > 1:
                caja_pos = (i, j)
                cajas_pos.append(caja_pos)
            content[i][j] = bloque_mapeo[content[i][j]]
    if jugador_pos is None:
        return None, None, None # no hay jugador
    return content, jugador_pos, cajas_pos

nivel = leerMapa()

def contar_cajas(ruta_archivo):
    with open(ruta_archivo, "r") as file:
        content = file.readlines()
    numCajas = sum([1 for linea in content if "," in linea]) - 1
    return numCajas if numCajas > 0 else None

numCajas = contar_cajas(nivel)

posicion_caja_n = [i for i in range(len(nivel)) for j in range(len(nivel[i])) if isinstance(nivel[i][j], list) and nivel[i][j][0] == numCajas][0:2]
posicion_caja_1 = [i for i in range(len(nivel)) for j in range(len(nivel[i])) if isinstance(nivel[i][j], list) and nivel[i][j][0] == 1][0:2]

#Analiza los movimientos que el jugador/IA tiene disponibles a su alrededor y genera una lista con ellos 

def movimientosDisponibles(nivel, jugador_pos):
    movimientos = []
    filas = len(nivel)
    columnas = len(nivel[0])
    fila_jugador, columna_jugador = jugador_pos

    if fila_jugador > 0 and nivel[fila_jugador-1][columna_jugador] == 0:
        movimientos.append('U')
    if fila_jugador < filas-1 and nivel[fila_jugador+1][columna_jugador] == 0:
        movimientos.append('D')
    if columna_jugador > 0 and nivel[fila_jugador][columna_jugador-1] == 0:
        movimientos.append('L')
    if columna_jugador < columnas-1 and nivel[fila_jugador][columna_jugador+1] == 0:
        movimientos.append('R')
    
    return movimientos


#Jerarquía con la que preferirá ir si puede realizar dos o más movimientos en un punto
def jerarquia():
    return ['U', 'D', 'L', 'R']

#compara jerarquia con movimientos y si el primer elemento de jerarquía está en movimientos, entonces elige ese elemento.
def elegirMovimiento(movimientos_posibles, jerarquia):
    for movimiento in jerarquia:
        if movimiento in movimientos_posibles:
            return movimiento
    print("No puedo moverme. Help")
    return None

def resolverNivel():
    # Leer el mapa
    nivel, jugador_pos, cajas_pos = leerMapa()
    if nivel is None:
        print("Error: El archivo de nivel es inválido.")
        return

    # Contar cajas y definir el estado del juego
    numCajas = contar_cajas(nivel)
    cajasEnObjetivo = 0
    restantes = numCajas

    # Resolver el nivel
    movimientos = []
    while cajasEnObjetivo < numCajas:
        # Mostrar el nivel y preguntar por el siguiente movimiento
        leerMapa(nivel, jugador_pos, cajas_pos)
        movimientos_posibles = movimientosDisponibles(nivel, jugador_pos[0], jugador_pos[1])
        movimiento = elegirMovimiento(movimientos_posibles, ["U", "D", "L", "R", ""])
        if movimiento is None:
            print("No hay movimientos disponibles.")
            break

        # Mover el jugador y actualizar la posición de las cajas
        if movimiento != "":
            movimientos.append(movimiento)
        nivel, jugador_pos, cajas_pos, caja_empujada = elegirMovimiento(nivel, jugador_pos, cajas_pos, movimiento)

        # Actualizar el estado del juego
        if caja_empujada:
            if nivel[caja_empujada[0]][caja_empujada[1]] == 2:
                cajasEnObjetivo += 1
                restantes -= 1

    # Imprimir los movimientos usados
    print(movimientos)