import sys
from collections import deque

def posicionJugador(content):
  jugador_pos = None
  for linea in content:
    if "W" not in linea:
      jugador_pos = tuple(map(int, linea.split(",")))
      break
  return jugador_pos

def posicionCajas(content):
  cajas_pos = []
  i = 0
  while i < len(content) - 1:
    if "W" not in content[i]:
      caja_pos = tuple(map(int, content[i + 1].split(",")))
      cajas_pos.append(caja_pos)
    i += 1
  return cajas_pos
  
def leerMapa(content):
  contentM = [linea.strip() for linea in content]
  filas = len(contentM)
  columnas = max(len(linea) for linea in contentM)
  mapa = []
  cajas_faltantes = 0
  estado_inicial = []
  estado_meta = []
  jugador_pos = posicionJugador(content)
  cajas_pos = posicionCajas(content)
  if jugador_pos is None:
    sys.exit("no hay jugador")
  cajas = len(cajas_pos)
  estado_inicial.append(jugador_pos)
  estado_inicial.append(cajas_pos)
  for i in range(filas - (cajas + 1)):
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
        estado_meta.append([i,j])
      else:
        fila.append(0)  # camino
    mapa.append(fila)
  return mapa, estado_inicial, estado_meta, cajas_faltantes, cajas


def busqueda_preferente_por_amplitud(estado_inicial, profundidad_maxima):
    cola = deque([(estado_inicial, 0)])
    visitados = set()
    while cola:
        estado_actual, profundidad_actual = cola.popleft()
        if estado_actual.es_estado_meta():
            return estado_actual.solucion()
        if profundidad_actual >= profundidad_maxima:
            continue
        for hijo in estado_actual.expandir():
            if hijo not in visitados:
                visitados.add(hijo)
                cola.append((hijo, profundidad_actual + 1))
    return None