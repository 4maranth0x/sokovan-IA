from collections import deque
import os

def inicio():
    mapa = input("¿Qué nivel jugaré? ")
    matriz, jugador_pos, cajas_pos, cajasEnObjetivo, cajas = leerMapa(mapa)
    if matriz is None:
        return None, None, None, None
    pos_jugador = posicionJugador(mapa)
    pos_cajas = posicionCajas(mapa)
    return matriz, pos_jugador, pos_cajas, cajasEnObjetivo, cajas
    

def leerMapa():
    with open(f"nivelesAqui/{mapa}.txt", "r") as file:
        content = file.readlines()
    content = [linea.strip() for linea in content]
    filas = len(content)
    columnas = max(len(linea) for linea in content)
    mapa = []
    jugador_pos = None
    cajas_pos = []
    cajasEnObjetivo = 0
    for i in range(filas):
        fila = []
        for j in range(columnas):
            if j >= len(content[i]):
                fila.append(1) # fuera del mapa
            elif content[i][j] == 'W':
                fila.append(1) # pared
            elif content[i][j] == '0':
                fila.append(0) # camino
            elif content[i][j] == 'X':
                fila.append(2) # objetivo
                cajasEnObjetivo += 1
            else:
                fila.append(0) # camino
                if content[i][j] == 'P':
                    if jugador_pos is not None:
                        return None, None, None # hay más de un jugador
                    jugador_pos = (i, j)
                elif content[i][j] == 'C':
                    caja_pos = (i, j)
                    cajas_pos.append(caja_pos)
        mapa.append(fila)
    if jugador_pos is None:
        return None, None, None, None # no hay jugador
    cajas = len(cajas_pos)
    return mapa, jugador_pos, cajas_pos, cajasEnObjetivo, cajas

def posicionJugador():
    with open(f"nivelesAqui/{mapa}.txt", "r") as file:
        content = file.readlines()
    jugador_pos = None
    for linea in content:
        if "P" in linea:
            jugador_pos = tuple(map(int, linea.split(",")))
            break
    return jugador_pos


def posicionCajas():
    with open(f"nivelesAqui/{mapa}.txt", "r") as file:
        content = file.readlines()
    cajas_pos = []
    for linea in content:
        if "C" in linea:
            caja_pos = tuple

nivel = leerMapa()
posJugador = posicionJugador()
posCajas = posicionCajas()


def mover_jugador(mapa, jugador_pos, cajas_pos, direccion):
    # definir cambios en fila y columna para cada dirección
    cambios = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    } 
    # calcular la posición a la que se quiere mover el jugador
    fila_nueva, col_nueva = jugador_pos[0] + cambios[direccion][0], jugador_pos[1] + cambios[direccion][1]
    # si la posición a la que se quiere mover es una pared, no se puede mover
    if mapa[fila_nueva][col_nueva] == 1:
        return mapa, jugador_pos, cajas_pos
    # si hay una caja en la posición a la que se quiere mover
    if (fila_nueva, col_nueva) in cajas_pos:
        # calcular la posición detrás de la caja
        fila_caja_nueva, col_caja_nueva = fila_nueva + cambios[direccion][0], col_nueva + cambios[direccion][1]
        # si la posición detrás de la caja es una pared o ya hay una caja ahí, no se puede mover
        if mapa[fila_caja_nueva][col_caja_nueva] == 1 or (fila_caja_nueva, col_caja_nueva) in cajas_pos:
            return mapa, jugador_pos, cajas_pos
        # mover la caja y actualizar su posición en la lista de posiciones de cajas
        cajas_pos.remove((fila_nueva, col_nueva))
        cajas_pos.append((fila_caja_nueva, col_caja_nueva))
    # mover el jugador y actualizar su posición
    jugador_pos = (fila_nueva, col_nueva)
    # actualizar el mapa
    mapa[jugador_pos[0]][jugador_pos[1]] = 3
    mapa[jugador_pos[0] - cambios[direccion][0]][jugador_pos[1] - cambios[direccion][1]] = 0
    for fila, col in cajas_pos:
        mapa[fila][col] = 2
    return mapa, jugador_pos, cajas_pos


def obtener_movimientos(mapa, pos):
    movimientos = []
    filas, columnas = len(mapa), len(mapa[0])
    x, y = pos
    
    # Movimiento hacia arriba
    if x > 0 and mapa[x-1][y] != 1:
        movimientos.append((x-1, y, "U"))
    
    # Movimiento hacia abajo
    if x < filas-1 and mapa[x+1][y] != 1:
        movimientos.append((x+1, y, "D"))
    
    # Movimiento hacia la izquierda
    if y > 0 and mapa[x][y-1] != 1:
        movimientos.append((x, y-1, "L"))
    
    # Movimiento hacia la derecha
    if y < columnas-1 and mapa[x][y+1] != 1:
        movimientos.append((x, y+1, "R"))
    
    return movimientos


def dfs():
    mapa, jugador_pos, cajas_pos, cajasEnObjetivo, cajas = leerMapa()
    if mapa is None:
        print("Error: mapa no válido")
        return None
    visitados = set()
    pila = [(jugador_pos, cajas_pos)]
    while pila:
        pos_jugador, pos_cajas = pila.pop()
        if all(caja in cajasEnObjetivo for caja in pos_cajas):
            return [] # Todas las cajas están en los objetivos
        if (pos_jugador, pos_cajas) in visitados:
            continue
        visitados.add((pos_jugador, pos_cajas))
        for movimiento in ["U", "D", "L", "R"]:
            nuevo_mapa, nuevo_pos_jugador, nuevo_pos_cajas = mover_jugador(mapa, pos_jugador, pos_cajas, movimiento)
            if (nuevo_pos_jugador, nuevo_pos_cajas) not in visitados:
                pila.append((nuevo_pos_jugador, nuevo_pos_cajas, movimiento))
                