
def leerMapa(content):
  contentM = [linea.strip() for linea in content]
  filas = len(contentM)
  columnas = max(len(linea) for linea in contentM)
  mapa = []
  cajas_faltantes = 0
  jugador_pos = posicionJugador(content)
  cajas_pos = posicionCajas(content)
  if jugador_pos is None:
    return None, None, None, None  # no hay jugador
  cajas = len(cajas_pos)
  for i in range(filas-(cajas+1)):
    fila = []
    for j in range(columnas):
      if j >= len(contentM[i]):
        fila.append(1)  # fuera del mapa
      elif contentM[i][j] == 'W':
        fila.append(1)  # pared
      elif contentM[i][j] == '0':
        fila.append(0)  # camino
      elif contentM[i][j] == 'X':
        fila.append(2)  # objetivo
        cajas_faltantes += 1
      else:
        fila.append(0)  # camino
    mapa.append(fila)
  return mapa, jugador_pos, cajas_pos, cajas_faltantes, cajas

def posicionJugador(content):
    jugador_pos = None
    for linea in content:
        if "W" not in linea:
            jugador_pos = tuple(map(int, linea.split(",")))
            break
    return jugador_pos


def posicionCajas(content):
  cajas_pos=[]
  i = 0
  while i < len(content)-1:
    if "W" not in content[i]:
      caja_pos = tuple(map(int, content[i+1].split(",")))
      cajas_pos.append(caja_pos)
    i += 1
  return cajas_pos


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

def inicio():
    mapa = input("¿Qué nivel jugaré? ")
    with open(f"nivelesAqui/{mapa}.txt", "r") as file:
        content = file.readlines()
    matriz, pos_jugador, pos_cajas, cajas_faltantes, cajas = leerMapa(content)
    if matriz is None:
        return None, None, None, None
    pos_jugador = posicionJugador(content)
    pos_cajas = posicionCajas(content)
    return matriz, pos_jugador, pos_cajas, cajas_faltantes, cajas

inicio()


def movimientosPosibles(nivel):
    pos_jugador = None
    casillas_disponibles = []
    for i in range(len(nivel)):
        for j in range(len(nivel[i])):
            if nivel[i][j] == 1:
                continue # pared
            elif nivel[i][j] == 0 or nivel[i][j] == 2:
                if pos_jugador is None:
                    pos_jugador = (i, j)
                else:
                    # hay más de un jugador
                    return None
            elif nivel[i][j] == 'P':
                pos_jugador = (i, j)
            elif nivel[i][j] == 'C':
                pos_caja = (i, j)
                direccion = posicionCajas(nivel, pos_caja, pos_jugador)
                if direccion is not None:
                    siguiente_pos = mover_jugador(nivel, pos_jugador, direccion)
                    if siguiente_pos is not None and nivel[siguiente_pos[0]][siguiente_pos[1]] in [0,2]:
                        casillas_disponibles.append((siguiente_pos, direccion))
                        
    if pos_jugador is None:
        # no hay jugador
        return None
    movimientos = []
    if pos_jugador[0] > 0 and nivel[pos_jugador[0]-1][pos_jugador[1]] in [0,2]:
        casillaU = (pos_jugador[0]-1, pos_jugador[1])
        movimientos.append((casillaU, "U"))
    if pos_jugador[0] < len(nivel)-1 and nivel[pos_jugador[0]+1][pos_jugador[1]] in [0,2]:
        casillaD = (pos_jugador[0]+1, pos_jugador[1])
        movimientos.append((casillaD, "D"))
    if pos_jugador[1] < len(nivel[0])-1 and nivel[pos_jugador[0]][pos_jugador[1]+1] in [0,2]:
        casillaR = (pos_jugador[0], pos_jugador[1]+1)
        movimientos.append((casillaR, "R"))
    if pos_jugador[1] > 0 and nivel[pos_jugador[0]][pos_jugador[1]-1] in [0,2]:
        casillaL = (pos_jugador[0], pos_jugador[1]-1)
        movimientos.append((casillaL, "L"))
        
    movimientos.extend(casillas_disponibles)
    
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
                