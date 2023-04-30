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
posicion_caja_n = [i for i in range(len(nivel)) for j in range(len(nivel[i])) if isinstance(nivel[i][j], list) and nivel[i][j][0] == n][0:2]
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

