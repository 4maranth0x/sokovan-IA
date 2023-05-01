from collections import deque
import os

def leerMapa():
    mapa = input("¿Qué nivel jugaré? ")
    #nivel_ruta = os.path.join("nivelesAqui", mapa)
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
        mapa.append(fila)
    
    # Leer las posiciones del jugador y las cajas después del mapa
    caja1_pos_str = content[-1].split(',')
    caja1_pos = (int(caja1_pos_str[0]), int(caja1_pos_str[1]))
    cajas_pos.append(caja1_pos)
    if "," in content[-3]:
        jugador_pos_str = content[-3].split(',')
        caja2_pos_str = content[-2].split(',')
        caja2_pos = (int(caja2_pos_str[0]), int(caja2_pos_str[1]))
        cajas_pos.append(caja2_pos)
    else:
        jugador_pos_str = content[-2].split(',')
    jugador_pos = (int(jugador_pos_str[0]), int(jugador_pos_str[1]))
    if jugador_pos is None:
        return None, None, None, None, None # no hay jugador
    cajas = len(cajas_pos)
    return mapa, jugador_pos, cajas_pos, cajasEnObjetivo, cajas

nivel = leerMapa()

def mover_jugador(mapa, jugador_pos, cajas_pos, direccion):
    # definir cambios en fila y columna para cada dirección
    cambios = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }
    fila_jugador, col_jugador = jugador_pos
    # calcular la posición a la que se quiere mover el jugador
    fila_nueva = fila_jugador + cambios[direccion][0]
    col_nueva = col_jugador + cambios[direccion][1]
    # si la posición a la que se quiere mover es una pared, no se puede mover
    if mapa[fila_nueva][col_nueva] == 1:
        return mapa, jugador_pos, cajas_pos
    # si hay una caja en la posición a la que se quiere mover
    if (fila_nueva, col_nueva) in cajas_pos:
        # calcular la posición detrás de la caja
        fila_caja_nueva = fila_nueva + cambios[direccion][0]
        col_caja_nueva = col_nueva + cambios[direccion][1]
        # si la posición detrás de la caja es una pared o ya hay una caja ahí, no se puede mover
        if mapa[fila_caja_nueva][col_caja_nueva] == 1 or (fila_caja_nueva, col_caja_nueva) in cajas_pos:
            return mapa, jugador_pos, cajas_pos
        # mover la caja y actualizar su posición en la lista de posiciones de cajas
        cajas_pos.remove((fila_nueva, col_nueva))
        cajas_pos.append((fila_caja_nueva, col_caja_nueva))
    # mover el jugador y actualizar su posición
    jugador_pos = (fila_nueva, col_nueva)
    # actualizar el mapa
    mapa[fila_jugador][col_jugador] = 0
    mapa[fila_nueva][col_nueva] = 3
    for caja_pos in cajas_pos:
        mapa[caja_pos[0]][caja_pos[1]] = 2
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


def bfs(mapa, jugador_pos, cajas_pos, cajasEnObjetivo):
    visitados = set()
    cola = deque([(jugador_pos, cajas_pos, [])])
    while cola:
        pos_jugador, pos_cajas, movimientos = cola.popleft()
        if all(caja in cajasEnObjetivo for caja in pos_cajas):
            return movimientos # Todas las cajas están en los objetivos
        if (pos_jugador, pos_cajas) in visitados:
            continue
        visitados.add((pos_jugador, pos_cajas))
        for movimiento in ["U", "D", "L", "R"]:
            nuevo_mapa, nuevo_pos_jugador, nuevo_pos_cajas = mover_jugador(mapa, pos_jugador, pos_cajas, movimiento)
            if (nuevo_pos_jugador, nuevo_pos_cajas) not in visitados:
                cola.append((nuevo_pos_jugador, nuevo_pos_cajas, movimientos + [movimiento]))

def iddfs(mapa, jugador_pos, cajas_pos, cajasEnObjetivo):
    for profundidad_maxima in range(1, 100):
        resultado = dfs_limitado(mapa, jugador_pos, cajas_pos, cajasEnObjetivo, profundidad_maxima)
        if resultado is not None:
            return resultado

def dfs_limitado(mapa, jugador_pos, cajas_pos, cajasEnObjetivo, profundidad_maxima):
    visitados = set()
    pila = [(jugador_pos, cajas_pos, [])]
    while pila:
        pos_jugador, pos_cajas, movimientos = pila.pop()
        if all(caja in cajasEnObjetivo for caja in pos_cajas):
            return movimientos # Todas las cajas están en los objetivos
        if (pos_jugador, pos_cajas) in visitados:
            continue
        
